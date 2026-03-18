from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
from queue import Queue
import threading
from typing import Optional
from uuid import uuid4

from api.schemas import ImageTo3DParams
from services.image_to_3d_service import image_to_3d_service, model_dump


ROOT_DIR = Path(__file__).resolve().parent.parent
JOBS_DIR = ROOT_DIR / "tmp" / "api_jobs"


@dataclass
class JobRecord:
    job_id: str
    status: str
    job_dir: Path
    input_filename: str
    params: ImageTo3DParams
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    result: Optional[dict] = None


class JobManager:
    def __init__(self) -> None:
        self._jobs: dict[str, JobRecord] = {}
        self._lock = threading.Lock()
        self._queue: Queue[str] = Queue()
        self._worker: threading.Thread | None = None

    def start(self) -> None:
        JOBS_DIR.mkdir(parents=True, exist_ok=True)
        if self._worker is None:
            self._worker = threading.Thread(target=self._run_worker, name="image-to-3d-worker", daemon=True)
            self._worker.start()

    def create_job(self, image_bytes: bytes, filename: str, params: ImageTo3DParams) -> JobRecord:
        job_id = uuid4().hex
        job_dir = JOBS_DIR / job_id
        job_dir.mkdir(parents=True, exist_ok=False)

        suffix = Path(filename or "input.png").suffix or ".png"
        input_filename = f"input{suffix.lower()}"
        input_path = job_dir / input_filename
        input_path.write_bytes(image_bytes)

        request_payload = {
            "job_id": job_id,
            "input_filename": input_filename,
            "params": model_dump(params),
        }
        with open(job_dir / "request.json", "w", encoding="utf-8") as fp:
            json.dump(request_payload, fp, ensure_ascii=False, indent=2)

        job = JobRecord(
            job_id=job_id,
            status="queued",
            job_dir=job_dir,
            input_filename=input_filename,
            params=params,
        )
        with self._lock:
            self._jobs[job_id] = job

        self._write_status(job)
        self._queue.put(job_id)
        return job

    def get_job(self, job_id: str) -> Optional[JobRecord]:
        with self._lock:
            return self._jobs.get(job_id)

    def queue_size(self) -> int:
        return self._queue.qsize()

    def artifact_path(self, job_id: str) -> Optional[Path]:
        job = self.get_job(job_id)
        if job is None or job.status != "completed":
            return None
        path = job.job_dir / "output.glb"
        if not path.exists():
            return None
        return path

    def _run_worker(self) -> None:
        while True:
            job_id = self._queue.get()
            job = self.get_job(job_id)
            if job is None:
                self._queue.task_done()
                continue

            try:
                job.status = "running"
                job.started_at = datetime.now(timezone.utc)
                self._write_status(job)

                result = image_to_3d_service.run(
                    image_path=job.job_dir / job.input_filename,
                    params=job.params,
                    output_dir=job.job_dir,
                )

                job.status = "completed"
                job.completed_at = datetime.now(timezone.utc)
                job.result = result
                self._write_status(job)
            except Exception as exc:
                job.status = "failed"
                job.completed_at = datetime.now(timezone.utc)
                job.error = str(exc)
                self._write_status(job)
            finally:
                self._queue.task_done()

    def _write_status(self, job: JobRecord) -> None:
        payload = {
            "job_id": job.job_id,
            "status": job.status,
            "created_at": job.created_at.isoformat(),
            "started_at": job.started_at.isoformat() if job.started_at else None,
            "completed_at": job.completed_at.isoformat() if job.completed_at else None,
            "error": job.error,
            "result": job.result,
        }
        with open(job.job_dir / "status.json", "w", encoding="utf-8") as fp:
            json.dump(payload, fp, ensure_ascii=False, indent=2)


job_manager = JobManager()


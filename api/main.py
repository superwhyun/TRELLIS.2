from __future__ import annotations

import json

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import ValidationError

from api.jobs import job_manager
from api.schemas import HealthResponse, ImageTo3DParams, JobStatusResponse, JobSubmissionResponse
from services.model_registry import model_registry


app = FastAPI(title="TRELLIS.2 API", version="0.1.0")


def validate_image_params(params_raw: str | None) -> ImageTo3DParams:
    if not params_raw:
        return ImageTo3DParams()
    try:
        payload = json.loads(params_raw)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail=f"Invalid JSON in params: {exc.msg}") from exc

    try:
        if hasattr(ImageTo3DParams, "model_validate"):
            return ImageTo3DParams.model_validate(payload)
        return ImageTo3DParams.parse_obj(payload)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc


@app.on_event("startup")
def startup_event() -> None:
    model_registry.preload_image_to_3d()
    job_manager.start()


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        image_to_3d_model_loaded=model_registry.image_to_3d_loaded,
        queue_size=job_manager.queue_size(),
    )


@app.post("/v1/image-to-3d/jobs", response_model=JobSubmissionResponse)
async def create_image_to_3d_job(
    image: UploadFile = File(...),
    params: str | None = Form(None),
) -> JobSubmissionResponse:
    image_bytes = await image.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Image upload is empty")

    job = job_manager.create_job(
        image_bytes=image_bytes,
        filename=image.filename or "input.png",
        params=validate_image_params(params),
    )
    return JobSubmissionResponse(
        job_id=job.job_id,
        status=job.status,
        status_url=f"/v1/jobs/{job.job_id}",
        artifact_url=f"/v1/jobs/{job.job_id}/artifact",
    )


@app.get("/v1/jobs/{job_id}", response_model=JobStatusResponse)
def get_job(job_id: str) -> JobStatusResponse:
    job = job_manager.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    artifact_url = None
    if job.status == "completed" and job_manager.artifact_path(job_id) is not None:
        artifact_url = f"/v1/jobs/{job_id}/artifact"

    return JobStatusResponse(
        job_id=job.job_id,
        status=job.status,
        created_at=job.created_at,
        started_at=job.started_at,
        completed_at=job.completed_at,
        error=job.error,
        artifact_url=artifact_url,
        result=job.result,
    )


@app.get("/v1/jobs/{job_id}/artifact")
def download_artifact(job_id: str) -> FileResponse:
    artifact_path = job_manager.artifact_path(job_id)
    if artifact_path is None:
        raise HTTPException(status_code=404, detail="Artifact is not ready")
    return FileResponse(path=artifact_path, filename=artifact_path.name, media_type="model/gltf-binary")


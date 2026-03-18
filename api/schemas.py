from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class ImageTo3DParams(BaseModel):
    resolution: Literal["512", "1024", "1536"] = "1024"
    seed: int = Field(default=0, ge=0, le=2147483647)
    randomize_seed: bool = True
    decimation_target: int = Field(default=500000, ge=100000, le=1000000)
    texture_size: int = Field(default=2048, ge=1024, le=4096)
    ss_guidance_strength: float = 7.5
    ss_guidance_rescale: float = Field(default=0.7, ge=0.0, le=1.0)
    ss_sampling_steps: int = Field(default=12, ge=1, le=50)
    ss_rescale_t: float = Field(default=5.0, ge=1.0, le=6.0)
    shape_slat_guidance_strength: float = 7.5
    shape_slat_guidance_rescale: float = Field(default=0.5, ge=0.0, le=1.0)
    shape_slat_sampling_steps: int = Field(default=12, ge=1, le=50)
    shape_slat_rescale_t: float = Field(default=3.0, ge=1.0, le=6.0)
    tex_slat_guidance_strength: float = 1.0
    tex_slat_guidance_rescale: float = Field(default=0.0, ge=0.0, le=1.0)
    tex_slat_sampling_steps: int = Field(default=12, ge=1, le=50)
    tex_slat_rescale_t: float = Field(default=3.0, ge=1.0, le=6.0)


class JobSubmissionResponse(BaseModel):
    job_id: str
    status: str
    status_url: str
    artifact_url: str


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    artifact_url: Optional[str] = None
    result: Optional[dict] = None


class HealthResponse(BaseModel):
    status: str
    image_to_3d_model_loaded: bool
    queue_size: int


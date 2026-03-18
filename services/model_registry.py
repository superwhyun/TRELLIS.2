from __future__ import annotations

import threading

from trellis2.pipelines import Trellis2ImageTo3DPipeline


class ModelRegistry:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._image_pipeline: Trellis2ImageTo3DPipeline | None = None

    def preload_image_to_3d(self) -> Trellis2ImageTo3DPipeline:
        with self._lock:
            if self._image_pipeline is None:
                pipeline = Trellis2ImageTo3DPipeline.from_pretrained("microsoft/TRELLIS.2-4B")
                pipeline.cuda()
                self._image_pipeline = pipeline
            return self._image_pipeline

    @property
    def image_to_3d_loaded(self) -> bool:
        return self._image_pipeline is not None

    def get_image_to_3d(self) -> Trellis2ImageTo3DPipeline:
        if self._image_pipeline is None:
            raise RuntimeError("Image-to-3D pipeline is not loaded")
        return self._image_pipeline


model_registry = ModelRegistry()


from __future__ import annotations

import json
import os
from pathlib import Path

os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

import numpy as np
from PIL import Image
import torch

import o_voxel

from api.schemas import ImageTo3DParams
from services.model_registry import model_registry


MAX_SEED = np.iinfo(np.int32).max
PIPELINE_TYPE_BY_RESOLUTION = {
    "512": "512",
    "1024": "1024_cascade",
    "1536": "1536_cascade",
}


def model_dump(model: ImageTo3DParams) -> dict:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


class ImageTo3DService:
    def run(self, image_path: Path, params: ImageTo3DParams, output_dir: Path) -> dict:
        pipeline = model_registry.get_image_to_3d()
        output_dir.mkdir(parents=True, exist_ok=True)

        image = Image.open(image_path).convert("RGBA")
        processed_image = pipeline.preprocess_image(image)
        processed_image_path = output_dir / "processed.png"
        processed_image.save(processed_image_path)

        seed = int(np.random.randint(0, MAX_SEED)) if params.randomize_seed else params.seed

        with torch.inference_mode():
            outputs, latents = pipeline.run(
                processed_image,
                seed=seed,
                preprocess_image=False,
                sparse_structure_sampler_params={
                    "steps": params.ss_sampling_steps,
                    "guidance_strength": params.ss_guidance_strength,
                    "guidance_rescale": params.ss_guidance_rescale,
                    "rescale_t": params.ss_rescale_t,
                },
                shape_slat_sampler_params={
                    "steps": params.shape_slat_sampling_steps,
                    "guidance_strength": params.shape_slat_guidance_strength,
                    "guidance_rescale": params.shape_slat_guidance_rescale,
                    "rescale_t": params.shape_slat_rescale_t,
                },
                tex_slat_sampler_params={
                    "steps": params.tex_slat_sampling_steps,
                    "guidance_strength": params.tex_slat_guidance_strength,
                    "guidance_rescale": params.tex_slat_guidance_rescale,
                    "rescale_t": params.tex_slat_rescale_t,
                },
                pipeline_type=PIPELINE_TYPE_BY_RESOLUTION[params.resolution],
                return_latent=True,
            )

            mesh = outputs[0]
            mesh.simplify(16777216)
            _, _, res = latents
            glb = o_voxel.postprocess.to_glb(
                vertices=mesh.vertices,
                faces=mesh.faces,
                attr_volume=mesh.attrs,
                coords=mesh.coords,
                attr_layout=pipeline.pbr_attr_layout,
                grid_size=res,
                aabb=[[-0.5, -0.5, -0.5], [0.5, 0.5, 0.5]],
                decimation_target=params.decimation_target,
                texture_size=params.texture_size,
                remesh=True,
                remesh_band=1,
                remesh_project=0,
                use_tqdm=False,
            )

        glb_path = output_dir / "output.glb"
        glb.export(glb_path, extension_webp=True)

        result = {
            "seed": seed,
            "resolution": params.resolution,
            "glb_filename": glb_path.name,
            "processed_image_filename": processed_image_path.name,
            "params": model_dump(params),
        }
        with open(output_dir / "result.json", "w", encoding="utf-8") as fp:
            json.dump(result, fp, ensure_ascii=False, indent=2)

        del outputs
        del latents
        del mesh
        del glb
        torch.cuda.empty_cache()

        return result


image_to_3d_service = ImageTo3DService()


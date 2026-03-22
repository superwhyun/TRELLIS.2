![](assets/teaser.webp)

# Native and Compact Structured Latents for 3D Generation

<a href="https://arxiv.org/abs/2512.14692"><img src="https://img.shields.io/badge/Paper-Arxiv-b31b1b.svg" alt="Paper"></a>
<a href="https://huggingface.co/microsoft/TRELLIS.2-4B"><img src="https://img.shields.io/badge/Hugging%20Face-Model-yellow" alt="Hugging Face"></a>
<a href="https://huggingface.co/spaces/microsoft/TRELLIS.2"><img src="https://img.shields.io/badge/Hugging%20Face-Demo-blueviolet"></a>
<a href="https://microsoft.github.io/TRELLIS.2"><img src="https://img.shields.io/badge/Project-Website-blue" alt="Project Page"></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green" alt="License"></a>

https://github.com/user-attachments/assets/63b43a7e-acc7-4c81-a900-6da450527d8f

*(Compressed version due to GitHub size limits. See the full-quality video on our project page!)*

**TRELLIS.2** is a state-of-the-art large 3D generative model (4B parameters) designed for high-fidelity **image-to-3D** generation. It leverages a novel "field-free" sparse voxel structure termed **O-Voxel** to reconstruct and generate arbitrary 3D assets with complex topologies, sharp features, and full PBR materials.


## ✨ Features

### 1. High Quality, Resolution & Efficiency
Our 4B-parameter model generates high-resolution fully textured assets with exceptional fidelity and efficiency using vanilla DiTs. It utilizes a Sparse 3D VAE with 16× spatial downsampling to encode assets into a compact latent space.

| Resolution | Total Time* | Breakdown (Shape + Mat) |
| :--- | :--- | :--- |
| **512³** | **~3s** | 2s + 1s |
| **1024³** | **~17s** | 10s + 7s |
| **1536³** | **~60s** | 35s + 25s |

<small>*Tested on NVIDIA H100 GPU.</small>

### 2. Arbitrary Topology Handling
The **O-Voxel** representation breaks the limits of iso-surface fields. It robustly handles complex structures without lossy conversion:
*   ✅ **Open Surfaces** (e.g., clothing, leaves)
*   ✅ **Non-manifold Geometry**
*   ✅ **Internal Enclosed Structures**

### 3. Rich Texture Modeling
Beyond basic colors, TRELLIS.2 models arbitrary surface attributes including **Base Color, Roughness, Metallic, and Opacity**, enabling photorealistic rendering and transparency support.

### 4. Minimalist Processing
Data processing is streamlined for instant conversions that are fully **rendering-free** and **optimization-free**.
*   **< 10s** (Single CPU): Textured Mesh → O-Voxel
*   **< 100ms** (CUDA): O-Voxel → Textured Mesh


## 🗺️ Roadmap

- [x] Paper release
- [x] Release image-to-3D inference code
- [x] Release pretrained checkpoints (4B)
- [x] Hugging Face Spaces demo
- [x] Release shape-conditioned texture generation inference code
- [x] Release training code


## 🛠️ Installation

### Prerequisites
- **System**: The code is currently tested only on **Linux**.
- **Hardware**: An NVIDIA GPU with at least 24GB of memory is necessary. The code has been verified on NVIDIA A100 and H100 GPUs.  
- **Software**:   
  - The [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit-archive) is needed to compile certain packages. Recommended version is 12.4.  
  - [Conda](https://docs.anaconda.com/miniconda/install/#quick-command-line-install) is recommended for managing dependencies.  
  - Python version 3.8 or higher is required. 

### Installation Steps
1. Clone the repo:
    ```sh
    git clone -b main https://github.com/microsoft/TRELLIS.2.git --recursive
    cd TRELLIS.2
    ```

2. Install the dependencies:
    
    **Before running the following command there are somethings to note:**
    - By adding `--new-env`, a new conda environment named `trellis2` will be created. If you want to use an existing conda environment, please remove this flag.
    - By default the `trellis2` environment will use pytorch 2.6.0 with CUDA 12.4. If you want to use a different version of CUDA, you can remove the `--new-env` flag and manually install the required dependencies. Refer to [PyTorch](https://pytorch.org/get-started/previous-versions/) for the installation command.
    - If you have multiple CUDA Toolkit versions installed, `CUDA_HOME` should be set to the correct version before running the command. For example, if you have CUDA Toolkit 12.4 and 13.0 installed, you can run `export CUDA_HOME=/usr/local/cuda-12.4` before running the command.
    - By default, the code uses the `flash-attn` backend for attention. For GPUs do not support `flash-attn` (e.g., NVIDIA V100), you can install `xformers` manually and set the `ATTN_BACKEND` environment variable to `xformers` before running the code. See the [Minimal Example](#minimal-example) for more details.
    - The installation may take a while due to the large number of dependencies. Please be patient. If you encounter any issues, you can try to install the dependencies one by one, specifying one flag at a time.
    - If you encounter any issues during the installation, feel free to open an issue or contact us.
    
    Create a new conda environment named `trellis2` and install the dependencies:
    ```sh
    . ./setup.sh --new-env --basic --flash-attn --nvdiffrast --nvdiffrec --cumesh --o-voxel --flexgemm
    ```
    The detailed usage of `setup.sh` can be found by running `. ./setup.sh --help`.
    ```sh
    Usage: setup.sh [OPTIONS]
    Options:
        -h, --help              Display this help message
        --new-env               Create a new conda environment
        --basic                 Install basic dependencies
        --flash-attn            Install flash-attention
        --cumesh                Install cumesh
        --o-voxel               Install o-voxel
        --flexgemm              Install flexgemm
        --nvdiffrast            Install nvdiffrast
        --nvdiffrec             Install nvdiffrec
    ```

### Docker 설치 및 실행 가이드

로컬에 Conda 환경을 직접 구성하지 않고 실행하려면 저장소에 포함된 `Dockerfile`과 `docker-compose.yml`을 사용할 수 있습니다. 현재 Docker 구성은 `app.py` 기반의 Gradio 웹 데모 실행을 기준으로 되어 있으며, 컨테이너 시작 후 `7860` 포트로 서비스가 열립니다.

#### 사전 요구사항

- Linux 환경
- NVIDIA GPU 및 최신 드라이버
- Docker Engine
- Docker Compose Plugin (`docker compose`)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
- Hugging Face 모델 다운로드를 위한 `HF_TOKEN`

`docker-compose.yml`은 GPU 사용을 전제로 작성되어 있으므로, Docker에서 GPU가 노출되는지 먼저 확인하는 것이 좋습니다.

```sh
docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi
```

#### 1. 환경 변수 준비

예시 파일을 복사한 뒤 Hugging Face 토큰을 입력합니다.

```sh
cp .env.example .env
```

`.env` 파일:

```sh
HF_TOKEN=hf_your_token_here
```

`HF_TOKEN`은 `docker-compose.yml`에서 컨테이너 내부의 `HF_TOKEN` 및 `HUGGING_FACE_HUB_TOKEN`으로 전달되며, 최초 실행 시 모델 다운로드에 사용됩니다.

#### 2. Docker 이미지 빌드

```sh
docker compose build
```

빌드에는 CUDA, PyTorch, `flash-attn`, `nvdiffrast`, `nvdiffrec`, `CuMesh`, `FlexGEMM`, `o-voxel` 설치가 포함되므로 시간이 오래 걸릴 수 있습니다.

필요하면 직접 이미지 이름을 지정해 빌드할 수도 있습니다.

```sh
docker build -t trellis2:latest .
```

#### 3. 웹 데모 실행

```sh
docker compose up
```

백그라운드 실행:

```sh
docker compose up -d
```

실행 후 브라우저에서 아래 주소로 접속합니다.

```text
http://localhost:7860
```
Clipboard image paste in the Gradio image input only works in a secure context, which typically means `https` or `localhost`. If you access the demo over plain `http` on a remote IP or hostname, regular file upload still works, but clipboard paste is blocked by the browser.

이 Compose 설정은 다음과 같이 동작합니다.

- 컨테이너 이름: `trellis2`
- 포트 매핑: `7860:7860`
- Hugging Face 캐시 볼륨 유지: `hf-cache`
- 임시 결과물 저장용 볼륨: `trellis-tmp`
- 공유 메모리 크기: `16gb`
- GPU 전체 사용: `NVIDIA_VISIBLE_DEVICES=all`

#### 4. 자주 쓰는 Docker 명령

로그 확인:

```sh
docker compose logs -f
```

중지 및 정리:

```sh
docker compose down
```

이미지 재빌드 후 다시 실행:

```sh
docker compose up -d --build
```

컨테이너 내부 셸 접속:

```sh
docker exec -it trellis2 bash
```

#### 5. 참고 사항

- 첫 실행 시 모델과 관련 의존성을 내려받기 때문에 시작 시간이 길 수 있습니다.
- `HF_TOKEN`이 없거나 잘못된 경우 Compose 실행 단계에서 오류가 발생합니다.
- 기본 실행 명령은 `python app.py`이며, 다른 스크립트를 실행하려면 `docker run` 또는 `docker compose run`으로 별도 명령을 지정하면 됩니다.
- 캐시는 Docker 볼륨에 저장되므로 컨테이너를 다시 만들어도 모델을 다시 받지 않을 수 있습니다.

## 📦 Pretrained Weights

The pretrained model **TRELLIS.2-4B** is available on Hugging Face. Please refer to the model card there for more details.

| Model | Parameters | Resolution | Link |
| :--- | :--- | :--- | :--- |
| **TRELLIS.2-4B** | 4 Billion | 512³ - 1536³ | [Hugging Face](https://huggingface.co/microsoft/TRELLIS.2-4B) |


## 🚀 Usage

### 1. Image to 3D Generation

#### Minimal Example

Here is an [example](example.py) of how to use the pretrained models for 3D asset generation.

```python
import os
os.environ['OPENCV_IO_ENABLE_OPENEXR'] = '1'
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"  # Can save GPU memory
import cv2
import imageio
from PIL import Image
import torch
from trellis2.pipelines import Trellis2ImageTo3DPipeline
from trellis2.utils import render_utils
from trellis2.renderers import EnvMap
import o_voxel

# 1. Setup Environment Map
envmap = EnvMap(torch.tensor(
    cv2.cvtColor(cv2.imread('assets/hdri/forest.exr', cv2.IMREAD_UNCHANGED), cv2.COLOR_BGR2RGB),
    dtype=torch.float32, device='cuda'
))

# 2. Load Pipeline
pipeline = Trellis2ImageTo3DPipeline.from_pretrained("microsoft/TRELLIS.2-4B")
pipeline.cuda()

# 3. Load Image & Run
image = Image.open("assets/example_image/T.png")
mesh = pipeline.run(image)[0]
mesh.simplify(16777216) # nvdiffrast limit

# 4. Render Video
video = render_utils.make_pbr_vis_frames(render_utils.render_video(mesh, envmap=envmap))
imageio.mimsave("sample.mp4", video, fps=15)

# 5. Export to GLB
glb = o_voxel.postprocess.to_glb(
    vertices            =   mesh.vertices,
    faces               =   mesh.faces,
    attr_volume         =   mesh.attrs,
    coords              =   mesh.coords,
    attr_layout         =   mesh.layout,
    voxel_size          =   mesh.voxel_size,
    aabb                =   [[-0.5, -0.5, -0.5], [0.5, 0.5, 0.5]],
    decimation_target   =   1000000,
    texture_size        =   4096,
    remesh              =   True,
    remesh_band         =   1,
    remesh_project      =   0,
    verbose             =   True
)
glb.export("sample.glb", extension_webp=True)
```

Upon execution, the script generates the following files:
 - `sample.mp4`: A video visualizing the generated 3D asset with PBR materials and environmental lighting.
 - `sample.glb`: The extracted PBR-ready 3D asset in GLB format.

**Note:** The `.glb` file is exported in `OPAQUE` mode by default. Although the alpha channel is preserved within the texture map, it is not active initially. To enable transparency, import the asset into your 3D software and manually connect the texture's alpha channel to the material's opacity or alpha input.

#### Web Demo

[app.py](app.py) provides a simple web demo for image to 3D asset generation. you can run the demo with the following command:
```sh
python app.py
```

Then, you can access the demo at the address shown in the terminal.
Clipboard image paste in the Gradio image input only works in a secure context, which typically means `https` or `localhost`. If you access the demo over plain `http` on a remote IP or hostname, regular file upload still works, but clipboard paste is blocked by the browser.

### 2. PBR Texture Generation

Please refer to the [example_texturing.py](example_texturing.py) for an example of how to generate PBR textures for a given 3D shape. Also, you can use the [app_texturing.py](app_texturing.py) to run a web demo for PBR texture generation.

### 3. API Server

웹 UI 대신 HTTP API로 호출하려면 API 전용 서버를 사용할 수 있습니다. 기존 `app.py`는 그대로 두고, 별도의 `FastAPI` 서버가 이미지 업로드와 비동기 작업 큐를 처리합니다.

#### API 서버 실행

```sh
docker compose -f docker-compose.api.yml up -d --build
```

실행 후 API는 아래 주소로 노출됩니다.

```text
http://localhost:8000
```

헬스 체크:

```sh
curl http://localhost:8000/health
```

응답 예시:

```json
{
  "status": "ok",
  "image_to_3d_model_loaded": true,
  "queue_size": 0
}
```

#### 현재 API 서버 동작 방식

- 서버 시작 시 `image-to-3d` 모델을 미리 로드하고, 백그라운드 작업 스레드를 함께 시작합니다.
- 생성 요청이 들어오면 업로드 이미지를 즉시 처리하지 않고, 작업 디렉터리를 만든 뒤 큐에 적재합니다.
- 작업 디렉터리는 `tmp/api_jobs/<JOB_ID>/` 아래에 생성됩니다.
- 각 작업 디렉터리에는 `input.*`, `request.json`, `status.json`이 먼저 저장되고, 작업 완료 시 `processed.png`, `result.json`, `output.glb`가 추가됩니다.
- 현재 워커는 1개이므로 작업은 단일 GPU 기준으로 직렬 처리됩니다.
- 작업 상태는 `queued`, `running`, `completed`, `failed` 중 하나입니다.

즉, API 사용 흐름은 `생성 요청 -> job_id 수신 -> 상태 조회 폴링 -> 완료 후 GLB 다운로드` 순서입니다.

#### 이미지 → 3D 작업 생성

이미지 파일과 파라미터 JSON을 함께 전송합니다. `params`를 생략하면 기본값이 사용됩니다.

```sh
curl -X POST http://localhost:8000/v1/image-to-3d/jobs \
  -F "image=@assets/example_image/T.png" \
  -F 'params={
    "resolution":"1024",
    "randomize_seed":true,
    "texture_size":2048,
    "decimation_target":500000
  }'
```

요청 형식:

- `Content-Type`: `multipart/form-data`
- 필수 필드: `image`
- 선택 필드: `params` (JSON 문자열)

`params`에서 현재 받을 수 있는 주요 값:

- `resolution`: `"512" | "1024" | "1536"`
- `seed`: `0` 이상 정수
- `randomize_seed`: `true/false`
- `decimation_target`: `100000` ~ `1000000`
- `texture_size`: `1024` ~ `4096`
- `ss_*`, `shape_slat_*`, `tex_slat_*`: 각 샘플러 세부 파라미터

동작 방식:

- 업로드 파일이 비어 있으면 `400 Image upload is empty`
- `params`가 JSON 형식이 아니면 `400 Invalid JSON in params`
- `params` 값 범위나 타입이 잘못되면 `422`
- 정상 요청이면 서버는 이미지를 `tmp/api_jobs/<JOB_ID>/input.*`로 저장하고, 요청 파라미터를 `request.json`에 기록한 뒤 바로 `queued` 상태를 반환합니다.

응답 예시:

```json
{
  "job_id": "9c7f4d5d8d574d4f9c1f2f20f5560f18",
  "status": "queued",
  "status_url": "/v1/jobs/9c7f4d5d8d574d4f9c1f2f20f5560f18",
  "artifact_url": "/v1/jobs/9c7f4d5d8d574d4f9c1f2f20f5560f18/artifact"
}
```

참고:

- 생성 응답의 `artifact_url`은 미리 내려오지만, 실제 파일이 준비되기 전까지 해당 URL은 `404 Artifact is not ready`를 반환합니다.
- 실제 다운로드 가능 여부는 상태 조회 응답의 `artifact_url` 포함 여부로 확인하는 것이 안전합니다.

#### 작업 상태 조회

```sh
curl http://localhost:8000/v1/jobs/<JOB_ID>
```

응답 필드:

- `job_id`
- `status`
- `created_at`
- `started_at`
- `completed_at`
- `error`
- `artifact_url`
- `result`

상태별 의미:

- `queued`: 큐에 들어갔고 아직 처리 전
- `running`: 워커가 실제 생성 작업 수행 중
- `completed`: `output.glb` 생성 완료
- `failed`: 생성 중 예외 발생, `error` 필드에 메시지 포함

완료 예시:

```json
{
  "job_id": "9c7f4d5d8d574d4f9c1f2f20f5560f18",
  "status": "completed",
  "created_at": "2026-03-18T03:12:10.123456+00:00",
  "started_at": "2026-03-18T03:12:11.012345+00:00",
  "completed_at": "2026-03-18T03:13:42.987654+00:00",
  "error": null,
  "artifact_url": "/v1/jobs/9c7f4d5d8d574d4f9c1f2f20f5560f18/artifact",
  "result": {
    "seed": 187654321,
    "resolution": "1024",
    "glb_filename": "output.glb",
    "processed_image_filename": "processed.png",
    "params": {
      "resolution": "1024",
      "seed": 0,
      "randomize_seed": true,
      "decimation_target": 500000,
      "texture_size": 2048
    }
  }
}
```

추가 동작:

- 존재하지 않는 작업 ID는 `404 Job not found`
- 완료 전에는 `artifact_url`이 `null`
- 완료 시 `result`에는 실제 사용된 `seed`, 전처리 이미지 파일명, 최종 파라미터가 포함됩니다.

#### GLB 다운로드

```sh
curl -L http://localhost:8000/v1/jobs/<JOB_ID>/artifact -o output.glb
```

동작 방식:

- 완료된 작업이고 `tmp/api_jobs/<JOB_ID>/output.glb`가 존재하면 GLB 파일을 그대로 내려줍니다.
- 작업이 아직 끝나지 않았거나 결과 파일이 없으면 `404 Artifact is not ready`
- 응답 파일명은 기본적으로 `output.glb`입니다.

#### 현재 API 범위

- 이미지 → 3D 작업 생성
- 단일 GPU 기준 직렬 작업 큐
- 작업 상태 조회
- 최종 GLB 다운로드

텍스처링 API는 아직 추가하지 않았으며, 현재는 이미지 → 3D 생성 경로만 API로 제공합니다.


## 🏋️ Training

We provide the full training codebase, enabling users to train **TRELLIS.2** from scratch or fine-tune it on custom datasets.

### 1. Data Preparation

Before training, raw 3D assets must be converted into the **O-Voxel** representation. This process includes mesh conversion, compact structured latent generation, and metadata preparation.

> 📂 **Please refer to [data_toolkit/README.md](data_toolkit/README.md) for detailed instructions on data preprocessing and dataset organization.**

### 2. Running Training

Training is managed through the `train.py` script, which accepts multiple command-line arguments to configure experiments:

* `--config`: Path to the experiment configuration file.
* `--output_dir`: Directory for training outputs.
* `--load_dir`: Directory to load checkpoints from (defaults to `output_dir`).
* `--ckpt`: Checkpoint step to resume from (defaults to the latest).
* `--data_dir`: Dataset path or a JSON string specifying dataset locations.
* `--auto_retry`: Number of automatic retries upon failure.
* `--tryrun`: Perform a dry run without actual training.
* `--profile`: Enable training profiling.
* `--num_nodes`: Number of nodes for distributed training.
* `--node_rank`: Rank of the current node.
* `--num_gpus`: Number of GPUs per node (defaults to all available GPUs).
* `--master_addr`: Master node address for distributed training.
* `--master_port`: Port for distributed training communication.


### SC-VAE Training


To train the shape SC-VAE, run:

```sh
python train.py \
  --config configs/scvae/shape_vae_next_dc_f16c32_fp16.json \
  --output_dir results/shape_vae_next_dc_f16c32_fp16 \
  --data_dir "{\"ObjaverseXL_sketchfab\": {\"base\": \"datasets/ObjaverseXL_sketchfab\", \"mesh_dump\": \"datasets/ObjaverseXL_sketchfab/mesh_dumps\", \"dual_grid\": \"datasets/ObjaverseXL_sketchfab/dual_grid_256\", \"asset_stats\": \"datasets/ObjaverseXL_sketchfab/asset_stats\"}}"
```

This command trains the shape SC-VAE on the **Objaverse-XL** dataset using the `shape_vae_next_dc_f16c32_fp16.json` configuration. Training outputs will be saved to `results/shape_vae_next_dc_f16c32_fp16`.

The dataset is specified as a JSON string, where each dataset entry includes:

* `base`: Root directory of the dataset.
* `mesh_dump`: Directory containing preprocessed mesh dumps.
* `dual_grid`: Directory with precomputed dual-grid representations.
* `asset_stats`: Directory containing precomputed asset statistics.

To fine-tune the model at a higher resolution, use the `shape_vae_next_dc_f16c32_fp16_ft_512.json` configuration. Remember to update the `finetune_ckpt` field and adjust the dataset paths accordingly.


To train the texture SC-VAE, run:

```sh
python train.py \
  --config configs/scvae/tex_vae_next_dc_f16c32_fp16.json \
  --output_dir results/tex_vae_next_dc_f16c32_fp16 \
  --data_dir "{\"ObjaverseXL_sketchfab\": {\"base\": \"datasets/ObjaverseXL_sketchfab\", \"pbr_dump\": \"datasets/ObjaverseXL_sketchfab/pbr_dumps\", \"pbr_voxel\": \"datasets/ObjaverseXL_sketchfab/pbr_voxels_256\", \"asset_stats\": \"datasets/ObjaverseXL_sketchfab/asset_stats\"}}"
```


### Flow Model Training

To train the sparse structure flow model, run:

```sh
python train.py \
  --config configs/gen/ss_flow_img_dit_1_3B_64_bf16.json \
  --output_dir results/ss_flow_img_dit_1_3B_64_bf16 \
  --data_dir "{\"ObjaverseXL_sketchfab\": {\"base\": \"datasets/ObjaverseXL_sketchfab\", \"ss_latent\": \"datasets/ObjaverseXL_sketchfab/ss_latents/ss_enc_conv3d_16l8_fp16_64\", \"render_cond\": \"datasets/ObjaverseXL_sketchfab/renders_cond\"}}"
```

This command trains the sparse-structure flow model on the **Objaverse-XL** dataset using the specified configuration file. Outputs are saved to `results/ss_flow_img_dit_1_3B_64_bf16`.

The dataset configuration includes:

* `base`: Root dataset directory.
* `ss_latent`: Directory containing precomputed sparse-structure latents.
* `render_cond`: Directory containing conditional rendering images.


The second- and third-stage flow models for shape and texture generation can be trained using the following configurations:

* Shape flow: `slat_flow_img2shape_dit_1_3B_512_bf16.json`
* Texture flow: `slat_flow_imgshape2tex_dit_1_3B_512_bf16.json`

Example commands:

```sh
# Shape flow model
python train.py \
  --config configs/gen/slat_flow_img2shape_dit_1_3B_512_bf16.json \
  --output_dir results/slat_flow_img2shape_dit_1_3B_512_bf16 \
  --data_dir "{\"ObjaverseXL_sketchfab\": {\"base\": \"datasets/ObjaverseXL_sketchfab\", \"shape_latent\": \"datasets/ObjaverseXL_sketchfab/shape_latents/shape_enc_next_dc_f16c32_fp16_512\", \"render_cond\": \"datasets/ObjaverseXL_sketchfab/renders_cond\"}}"

# Texture flow model
python train.py \
  --config configs/gen/slat_flow_imgshape2tex_dit_1_3B_512_bf16.json \
  --output_dir results/slat_flow_imgshape2tex_dit_1_3B_512_bf16 \
  --data_dir "{\"ObjaverseXL_sketchfab\": {\"base\": \"datasets/ObjaverseXL_sketchfab\", \"shape_latent\": \"datasets/ObjaverseXL_sketchfab/shape_latents/shape_enc_next_dc_f16c32_fp16_512\", \"pbr_latent\": \"datasets/ObjaverseXL_sketchfab/pbr_latents/tex_enc_next_dc_f16c32_fp16_512\", \"render_cond\": \"datasets/ObjaverseXL_sketchfab/renders_cond\"}}"
```

Higher-resolution fine-tuning can be performed by updating the `finetune_ckpt` field in the following configuration files and adjusting the dataset paths accordingly:

* `slat_flow_img2shape_dit_1_3B_512_bf16_ft1024.json`
* `slat_flow_imgshape2tex_dit_1_3B_512_bf16_ft1024.json`


## 🧩 Related Packages

TRELLIS.2 is built upon several specialized high-performance packages developed by our team:

*   **[O-Voxel](o-voxel):** 
    Core library handling the logic for converting between textured meshes and the O-Voxel representation, ensuring instant bidirectional transformation.
*   **[FlexGEMM](https://github.com/JeffreyXiang/FlexGEMM):** 
    Efficient sparse convolution implementation based on Triton, enabling rapid processing of sparse voxel structures.
*   **[CuMesh](https://github.com/JeffreyXiang/CuMesh):** 
    CUDA-accelerated mesh utilities used for high-speed post-processing, remeshing, decimation, and UV-unwrapping.


## ⚖️ License

This model and code are released under the **[MIT License](LICENSE)**.

Please note that certain dependencies operate under separate license terms:

- [**nvdiffrast**](https://github.com/NVlabs/nvdiffrast): Utilized for rendering generated 3D assets. This package is governed by its own [License](https://github.com/NVlabs/nvdiffrast/blob/main/LICENSE.txt).

- [**nvdiffrec**](https://github.com/NVlabs/nvdiffrec): Implements the split-sum renderer for PBR materials. This package is governed by its own [License](https://github.com/NVlabs/nvdiffrec/blob/main/LICENSE.txt).

## 📚 Citation

If you find this model useful for your research, please cite our work:

```bibtex
@article{
    xiang2025trellis2,
    title={Native and Compact Structured Latents for 3D Generation},
    author={Xiang, Jianfeng and Chen, Xiaoxue and Xu, Sicheng and Wang, Ruicheng and Lv, Zelong and Deng, Yu and Zhu, Hongyuan and Dong, Yue and Zhao, Hao and Yuan, Nicholas Jing and Yang, Jiaolong},
    journal={Tech report},
    year={2025}
}
```

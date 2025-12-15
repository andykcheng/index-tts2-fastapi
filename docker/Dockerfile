FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HF_ENDPOINT=https://hf-mirror.com

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    git-lfs

# Set work directory
WORKDIR /app

RUN git lfs install
RUN git clone https://github.com/andykcheng/index-tts2-fastapi.git
WORKDIR /app/index-tts2-fastapi
RUN uv sync
RUN uv tool install "huggingface-hub"
RUN uv run hf download IndexTeam/IndexTTS-2 --local-dir=checkpoints

# Expose port
EXPOSE 8000

# Run the application
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

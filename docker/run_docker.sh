#!/bin/bash

docker run -d \
  --name index-tts \
  --gpus all \
  -p 8804:8000 \
  -e NVIDIA_VISIBLE_DEVICES=all \
  -v "$(pwd)/voice_files:/app/index-tts2-fastapi/voice_files" \
  andychenghk/indextts2-fastapi:latest

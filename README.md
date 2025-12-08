# Project 
This is a fork of the index-tts v2, with add trancoding and api for easy access and installation

# Installation
git clone 
uv sync
uv tool install "huggingface-hub[cli,hf_xet]"
hf download IndexTeam/IndexTTS-2 --local-dir=checkpoints
uv run uvicorn main:app
# IndexTTS FastAPI Server

This is a FastAPI-based server for IndexTTS v2, providing Text-to-Speech (TTS) generation with transcoding and API access. It supports generating audio in WAV and Opus formats, with options for direct file downloads or base64-encoded JSON responses.

## Server Structure

The server is organized as follows:

- **`main.py`**: Main FastAPI application with TTS endpoints
- **`indextts/`**: Core TTS inference package
  - `infer_v2.py`: IndexTTS2 inference engine
  - `gpt/`: GPT-based model components
  - `s2mel/`: Speech-to-mel spectrogram conversion
  - `utils/`: Utility functions for text processing, checkpoints, etc.
  - `BigVGAN/`: Vocoder for waveform generation
- **`checkpoints/`**: Model checkpoints and configuration files
- **`voice_files/`**: Voice prompt audio files for zero-shot TTS
- **`outputs/`**: Temporary directory for generated audio files
- **`webui.py`**: Gradio web interface (optional)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd index-tts-fastapi
   ```

2. Install dependencies using uv:
   ```bash
   uv sync
   ```

3. Install Hugging Face CLI tool:
   ```bash
   uv tool install "huggingface-hub[cli,hf_xet]"
   ```

4. Download the model checkpoints:
   ```bash
   hf download IndexTeam/IndexTTS-2 --local-dir=checkpoints
   ```

5. (Optional) For web UI support:
   ```bash
   uv sync --extra webui
   ```

## Starting the Server

### Basic Server
```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

### With Reload (Development)
```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

The server provides the following endpoints:

### POST `/generate-opus`
Generates audio in Opus format and returns it as a file download.

**Request Body:**
```json
{
  "text": "Hello, world!",
  "voice_id": "voice_01",
  "bitrate": 128
}
```

**Parameters:**
- `text` (string, required): Text to convert to speech
- `voice_id` (string, optional): Voice identifier (default: "voice_01"). Must correspond to a file in `voice_files/{voice_id}.wav`
- `bitrate` (integer, optional): Opus bitrate in kbps (default: 128)

**Response:** Binary Opus file download

**Example:**
```bash
curl -X POST "http://localhost:8000/generate-opus" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello world", "voice_id": "voice_01", "bitrate": 128}' \
     -o output.opus
```

### POST `/generate-wav`
Generates audio in WAV format and returns it as a file download.

**Request Body:**
```json
{
  "text": "Hello, world!",
  "voice_id": "voice_01"
}
```

**Parameters:** Same as `/generate-opus` (bitrate parameter is ignored for WAV)

**Response:** Binary WAV file download

**Example:**
```bash
curl -X POST "http://localhost:8000/generate-wav" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello world", "voice_id": "voice_01"}' \
     -o output.wav
```

### POST `/generate-opus-json`
Generates audio in Opus format and returns base64-encoded data in JSON.

**Request Body:** Same as `/generate-opus`

**Response:**
```json
{
  "data": "base64-encoded-audio-data",
  "length": 12345
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/generate-opus-json" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello world", "voice_id": "voice_01", "bitrate": 128}' \
     -o response.json
```

### POST `/generate-wav-json`
Generates audio in WAV format and returns base64-encoded data in JSON.

**Request Body:** Same as `/generate-wav`

**Response:** Same format as `/generate-opus-json`

**Example:**
```bash
curl -X POST "http://localhost:8000/generate-wav-json" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello world", "voice_id": "voice_01"}' \
     -o response.json
```

### GET `/`
Returns this documentation as HTML.

## Voice Files

Voice prompts should be placed in the `voice_files/` directory with the naming convention `{voice_id}.wav`. For example:
- `voice_files/voice_01.wav`
- `voice_files/voice_02.wav`

The `voice_id` parameter in API requests should match the filename without the `.wav` extension.

## Configuration

The TTS engine is configured in `main.py` with the following default settings:
- Model config: `checkpoints/config.yaml`
- Model directory: `checkpoints/`
- FP16: Disabled
- CUDA kernel: Disabled
- DeepSpeed: Disabled

These can be modified by editing the `IndexTTS2` initialization in `main.py`.

## Error Handling

The server returns HTTP 500 errors with descriptive messages for:
- Model initialization failures
- Invalid voice files
- TTS inference errors
- File processing errors

## Dependencies

Key dependencies include:
- FastAPI: Web framework
- IndexTTS: Core TTS engine
- PyTorch: Machine learning framework
- Transformers: Hugging Face transformers
- Librosa: Audio processing
- FFmpeg: Audio transcoding

See `pyproject.toml` for the complete dependency list.

## License

This project is licensed under the Bilibili IndexTTS license. See `LICENSE` and `LICENSE_ZH.txt` for details.
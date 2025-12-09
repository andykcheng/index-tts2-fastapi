import os
import uuid
import subprocess
import io
import base64
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse, HTMLResponse
from pydantic import BaseModel
# from pydub import AudioSegment  <-- Removed pydub
from indextts.infer_v2 import IndexTTS2
import yaml
# before loading the model, change the file checkpoints/config.yaml to set max_text_tokens to 30 for faster inference on short texts
with open("checkpoints/config.yaml", 'r') as f:
    config = yaml.safe_load(f)
    config['gpt']['max_text_tokens'] = 30
with open("checkpoints/config.yaml", 'w') as f:
    yaml.dump(config, f)
    
app = FastAPI(title="IndexTTS Opus Server")

# Ensure output directory exists
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load model globally once at startup
print("Loading IndexTTS Model...")
try:
    tts_engine = IndexTTS2(
        cfg_path="checkpoints/config.yaml", 
        model_dir="checkpoints", 
        use_fp16=True, 
        use_cuda_kernel=True, 
        use_deepspeed=True,
        use_accel=True
    )
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    tts_engine = None

# Define the request structure
class TTSRequest(BaseModel):
    text: str
    voice_id: str = "voice_01"  # Default voice file
    bitrate: int = 128  # in kbps
    
# helper to delete files after sending
def remove_file(path: str):
    try:
        os.remove(path)
    except Exception as e:
        print(f"Error deleting file {path}: {e}")

@app.post("/generate-opus")
async def generate_audio_opus(request: TTSRequest, background_tasks: BackgroundTasks):
    # Generate unique filenames to prevent collisions between users
    request_id = str(uuid.uuid4())
    # Use absolute paths inside outputs folder
    wav_filename = os.path.abspath(os.path.join(OUTPUT_DIR, f"temp_{request_id}.wav"))
    opus_filename = os.path.abspath(os.path.join(OUTPUT_DIR, f"output_{request_id}.opus"))

    try:
        if tts_engine is None:
            raise HTTPException(status_code=500, detail="TTS Engine not initialized")

        # Run Inference
        tts_engine.infer(
            spk_audio_prompt=f'voice_files/{request.voice_id}.wav', 
            text=request.text, 
            output_path=wav_filename, 
            verbose=True
        )
        
        # Convert WAV to Opus with specified bitrate using ffmpeg command
        subprocess.run([
            'ffmpeg', '-i', wav_filename, '-b:a', f'{request.bitrate}k', opus_filename
        ], check=True)
        
        # Remove temp WAV file
        os.remove(wav_filename)
        
        # Read Opus file into memory
        with open(opus_filename, 'rb') as f:
            data = f.read()
        
        # Remove Opus file
        os.remove(opus_filename)
        
        return StreamingResponse(io.BytesIO(data), media_type='audio/opus', headers={"Content-Disposition": f"attachment; filename=output_{request_id}.opus"})
    except Exception as e:
        print(f"Error during TTS processing: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-wav")
async def generate_audio_wav(request: TTSRequest, background_tasks: BackgroundTasks):
    # Generate unique filenames to prevent collisions between users
    request_id = str(uuid.uuid4())
    # Use absolute paths inside outputs folder
    wav_filename = os.path.abspath(os.path.join(OUTPUT_DIR, f"output_{request_id}.wav"))

    try:
        if tts_engine is None:
            raise HTTPException(status_code=500, detail="TTS Engine not initialized")

        # Run Inference
        tts_engine.infer(
            spk_audio_prompt=f'voice_files/{request.voice_id}.wav', 
            text=request.text, 
            output_path=wav_filename, 
            verbose=True
        )
        
        # Read WAV file into memory
        with open(wav_filename, 'rb') as f:
            data = f.read()
        
        # Remove WAV file
        os.remove(wav_filename)
        
        return StreamingResponse(io.BytesIO(data), media_type='audio/wav', headers={"Content-Disposition": f"attachment; filename=output_{request_id}.wav"})
    except Exception as e:
        print(f"Error during TTS processing: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-opus-json")
async def generate_audio_opus_json(request: TTSRequest, background_tasks: BackgroundTasks):
    # Generate unique filenames to prevent collisions between users
    request_id = str(uuid.uuid4())
    # Use absolute paths inside outputs folder
    wav_filename = os.path.abspath(os.path.join(OUTPUT_DIR, f"temp_{request_id}.wav"))
    opus_filename = os.path.abspath(os.path.join(OUTPUT_DIR, f"output_{request_id}.opus"))

    try:
        if tts_engine is None:
            raise HTTPException(status_code=500, detail="TTS Engine not initialized")

        # Run Inference
        tts_engine.infer(
            spk_audio_prompt=f'voice_files/{request.voice_id}.wav', 
            text=request.text, 
            output_path=wav_filename, 
            verbose=True
        )
        
        # Convert WAV to Opus with specified bitrate using ffmpeg command
        subprocess.run([
            'ffmpeg', '-i', wav_filename, '-b:a', f'{request.bitrate}k', opus_filename
        ], check=True)
        
        # Remove temp WAV file
        os.remove(wav_filename)
        
        # Read Opus file into memory
        with open(opus_filename, 'rb') as f:
            data = f.read()
        
        # Remove Opus file
        os.remove(opus_filename)
        
        # Encode to base64
        encoded_data = base64.b64encode(data).decode('utf-8')
        
        return JSONResponse({"data": encoded_data, "length": len(encoded_data)})
    except Exception as e:
        print(f"Error during TTS processing: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-wav-json")
async def generate_audio_wav_json(request: TTSRequest, background_tasks: BackgroundTasks):
    # Generate unique filenames to prevent collisions between users
    request_id = str(uuid.uuid4())
    # Use absolute paths inside outputs folder
    wav_filename = os.path.abspath(os.path.join(OUTPUT_DIR, f"output_{request_id}.wav"))

    try:
        if tts_engine is None:
            raise HTTPException(status_code=500, detail="TTS Engine not initialized")

        # Run Inference
        tts_engine.infer(
            spk_audio_prompt=f'voice_files/{request.voice_id}.wav', 
            text=request.text, 
            output_path=wav_filename, 
            verbose=True
        )
        
        # Read WAV file into memory
        with open(wav_filename, 'rb') as f:
            data = f.read()
        
        # Remove WAV file
        os.remove(wav_filename)
        
        # Encode to base64
        encoded_data = base64.b64encode(data).decode('utf-8')
        
        return JSONResponse({"data": encoded_data, "length": len(encoded_data)})
    except Exception as e:
        print(f"Error during TTS processing: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_root():
    readme = """
# IndexTTS FastAPI Server

This server provides Text-to-Speech (TTS) generation using the IndexTTS model.

## Endpoints

### POST /generate-opus
Generates audio in Opus format and returns the file as a download.

- **Parameters** (JSON body):
  - `text` (str): The text to convert to speech.
  - `voice_id` (str, optional): Voice file identifier (default: "voice_01"). Files are located in `voice_files/{voice_id}.wav`.
  - `bitrate` (int, optional): Bitrate for Opus encoding in kbps (default: 128).

- **Response**: Binary Opus file download.

- **Example**:
  ```
  curl -X POST "http://localhost:8000/generate-opus" \\
       -H "Content-Type: application/json" \\
       -d '{"text": "Hello world", "voice_id": "voice_01", "bitrate": 128}' \\
       -o output.opus
  ```

### POST /generate-wav
Generates audio in WAV format and returns the file as a download.

- **Parameters** (JSON body): Same as /generate-opus.

- **Response**: Binary WAV file download.

- **Example**:
  ```
  curl -X POST "http://localhost:8000/generate-wav" \\
       -H "Content-Type: application/json" \\
       -d '{"text": "Hello world", "voice_id": "voice_01"}' \\
       -o output.wav
  ```

### POST /generate-opus-json
Generates audio in Opus format and returns base64-encoded data in JSON.

- **Parameters** (JSON body): Same as /generate-opus.

- **Response**: JSON with `{"data": "<base64_string>", "length": <int>}`.

- **Example**:
  ```
  curl -X POST "http://localhost:8000/generate-opus-json" \\
       -H "Content-Type: application/json" \\
       -d '{"text": "Hello world", "voice_id": "voice_01", "bitrate": 128}' \\
       -o response.json
  ```

### POST /generate-wav-json
Generates audio in WAV format and returns base64-encoded data in JSON.

- **Parameters** (JSON body): Same as /generate-opus.

- **Response**: JSON with `{"data": "<base64_string>", "length": <int>}`.

- **Example**:
  ```
  curl -X POST "http://localhost:8000/generate-wav-json" \\
       -H "Content-Type: application/json" \\
       -d '{"text": "Hello world", "voice_id": "voice_01"}' \\
       -o response.json
  ```

## Notes
- Ensure the server has access to `voice_files/` directory with voice prompt files.
- The model is loaded at startup from `checkpoints/`.
- Errors are returned as HTTP 500 with details.
"""
    return HTMLResponse(content=f"<pre>{readme}</pre>", media_type="text/html")




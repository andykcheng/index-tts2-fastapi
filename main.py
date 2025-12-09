import os
import uuid
import ffmpeg
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
# from pydub import AudioSegment  <-- Removed pydub
from indextts.infer_v2 import IndexTTS2
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
        use_fp16=False, 
        use_cuda_kernel=False, 
        use_deepspeed=False
    )
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    tts_engine = None

# Define the request structure
class TTSRequest(BaseModel):
    text: str
    voice_id: str = "default"  # Optional, if the engine supports multiple voices

# helper to delete files after sending
def remove_file(path: str):
    try:
        os.remove(path)
    except Exception as e:
        print(f"Error deleting file {path}: {e}")

@app.post("/generate-opus")
async def generate_audio(request: TTSRequest, background_tasks: BackgroundTasks):
    # 1. Generate unique filenames to prevent collisions between users
    request_id = str(uuid.uuid4())
    # Use absolute paths inside outputs folder
    wav_filename = os.path.abspath(os.path.join(OUTPUT_DIR, f"temp_{request_id}.wav"))
    opus_filename = os.path.abspath(os.path.join(OUTPUT_DIR, f"output_{request_id}.opus"))

    try:
        if tts_engine is None:
            raise HTTPException(status_code=500, detail="TTS Engine not initialized")

        # 2. Run Inference
        tts_engine.infer(
            spk_audio_prompt='examples/voice_01.wav', 
            text=request.text, 
            output_path=wav_filename, 
            verbose=True
        )

       
        return JSONResponse(content={"message": "TTS processing completed."})

    except Exception as e:
        print(f"Error during TTS processing: {e}")
        # output the stack trace for debugging
        import traceback
        traceback.print_exc()
        
        # Cleanup if something crashed midway
        raise HTTPException(status_code=500, detail=str(e))




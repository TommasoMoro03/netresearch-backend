from fastapi import APIRouter, UploadFile, File, HTTPException
from openai import OpenAI
import shutil
import os
import tempfile
from app.core.config import settings

router = APIRouter(prefix="/api/audio", tags=["Audio"])

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Transcribe an uploaded audio file using OpenAI Whisper.
    """
    # Create a temporary file to store the upload
    # We use delete=False so we can close it before passing to OpenAI, then delete manually
    with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as temp_file:
        temp_filename = temp_file.name
        
    try:
        # Write uploaded content to temp file
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Initialize OpenAI client with explicit key from settings
        # This avoids using the env var which might be overwritten by llm_factory
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Transcribe
        with open(temp_filename, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
            
        return {"text": transcript.text}
        
    except Exception as e:
        print(f"Transcription error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to transcribe audio: {str(e)}")
        
    finally:
        # Cleanup
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

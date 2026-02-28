import os
from dotenv import load_dotenv
load_dotenv()  # Load variables from .env file
import torch
import numpy as np
import joblib
import librosa
import io
import base64
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from transformers import Wav2Vec2FeatureExtractor, Wav2Vec2Model
from typing import Optional

# --- 1. SETUP & CONFIGURATION ---
app = FastAPI(title="AI Voice Detection API", version="1.0.0")

# API Key Configuration
# Load API key from .env (never hardcode secrets in source code!)
VALID_API_KEY = os.getenv("SECRET_API_KEY", "HACKATHON_SECRET_KEY_123")

# Mount the static folder (Frontend) - Optional for hackathon
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    pass  # Static folder not required for API-only mode

# Load AI Brains (Global Variables)
print("Loading Model...")
try:
    # NOTE: Models were saved with joblib in train_model.py, so load with joblib
    classifier = joblib.load("hackathon_model.pkl")
    scaler = joblib.load("model_scaler.pkl")
    
    # Load Meta's Wav2Vec2 (Use FeatureExtractor, same as used in train_model.py)
    processor = Wav2Vec2FeatureExtractor.from_pretrained("facebook/wav2vec2-large-xlsr-53")
    model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-large-xlsr-53")
    print("✅ Brain Loaded!")
except Exception as e:
    print(f"❌ CRITICAL ERROR LOADING MODEL: {e}")

# --- 2. REQUEST/RESPONSE MODELS ---
class AudioDetectionRequest(BaseModel):
    # Snake_case fields (original)
    audio_base64: Optional[str] = None
    audio_base64_format: Optional[str] = None
    audio_format: Optional[str] = None
    language: Optional[str] = None
    
    # CamelCase fields (for compatibility)
    audioBase64: Optional[str] = None
    audioFormat: Optional[str] = None

class AudioDetectionResponse(BaseModel):
    is_ai_generated: bool
    confidence_score: float
    message: str

# --- 3. AUTHENTICATION HELPER ---
def verify_api_key(authorization: Optional[str] = Header(None), x_api_key: Optional[str] = Header(None)) -> bool:
    """
    Verify API key from either Authorization header or x-api-key header
    """
    # Check x-api-key header first
    if x_api_key and x_api_key == VALID_API_KEY:
        return True
    
    # Check Authorization header (supports both "Bearer TOKEN" and just "TOKEN")
    if authorization:
        # Remove "Bearer " prefix if present
        token = authorization.replace("Bearer ", "").strip()
        if token == VALID_API_KEY:
            return True
    
    return False

# --- 4. ROOT ENDPOINT ---
@app.get("/")
async def read_root():
    return JSONResponse(content={
        "message": "AI Voice Detection API is Running!",
        "version": "1.0.0",
        "endpoint": "/detect-audio/",
        "method": "POST"
    })

# --- 5. THE DETECTION ENGINE (HACKATHON API ENDPOINT) ---
@app.post("/detect-audio/", response_model=AudioDetectionResponse)
async def detect_audio(
    request: AudioDetectionRequest,
    authorization: Optional[str] = Header(None),
    x_api_key: Optional[str] = Header(None)
):
    """
    AI Voice Detection Endpoint
    
    Accepts a JSON body with base64-encoded audio and returns whether the audio is AI-generated.
    Requires API key authentication via Authorization or x-api-key header.
    """
    
    # --- STEP 1: AUTHENTICATION ---
    if not verify_api_key(authorization, x_api_key):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized: Invalid or missing API key"
        )
    
    try:
        # --- STEP 2: NORMALIZE FIELD NAMES (camelCase vs snake_case) ---
        # Resolve audio format field
        final_format = request.audioFormat or request.audio_format
        if not final_format:
            final_format = "mp3"  # Default to mp3 if not provided
        
        # Resolve audio data field (try all possible field names)
        final_base64 = (
            request.audioBase64 or 
            request.audio_base64 or 
            request.audio_base64_format
        )
        
        if not final_base64:
            raise HTTPException(
                status_code=400,
                detail="Missing audio data: provide 'audioBase64', 'audio_base64', or 'audio_base64_format'"
            )
        
        # --- STEP 3: DECODE BASE64 AUDIO ---
        try:
            audio_bytes = base64.b64decode(final_base64)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid base64 encoding: {str(e)}"
            )
        
        # --- STEP 4: LOAD AUDIO FILE ---
        try:
            audio, sample_rate = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        except Exception as e:
            return AudioDetectionResponse(
                is_ai_generated=True,
                confidence_score=0.0,
                message="Error reading audio file. Flagged as suspicious."
            )

        # --- STEP 5: SAFETY CHECK ---
        if len(audio) < 1600:  # Less than 0.1 second
            return AudioDetectionResponse(
                is_ai_generated=True,
                confidence_score=0.0,
                message="Audio too short. Insufficient data."
            )

        # --- STEP 6: FEATURE EXTRACTION ---
        inputs = processor(audio, sampling_rate=16000, return_tensors="pt", padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
            embedding = torch.mean(outputs.last_hidden_state, dim=1).squeeze().numpy()

        # --- STEP 7: CHECK FOR INVALID DATA ---
        if np.isnan(embedding).any():
            return AudioDetectionResponse(
                is_ai_generated=True,
                confidence_score=0.99,
                message="Corrupted spectral data detected."
            )

        # --- STEP 8: SCALE FEATURES ---
        embedding_scaled = scaler.transform([embedding])

        # --- STEP 9: PREDICTION ---
        probs = classifier.predict_proba(embedding_scaled)[0]
        
        human_score = float(probs[0])
        ai_score = float(probs[1])
        
        # --- STEP 10: DECISION LOGIC ---
        if np.isnan(human_score) or np.isnan(ai_score):
            is_ai = True
            confidence = 0.95
            message = "Invalid signal structure detected."
        elif human_score > 0.98:
            is_ai = False
            confidence = human_score
            message = "Authentic vocal micro-tremors and breathing patterns verified."
        else:
            is_ai = True
            confidence = ai_score if ai_score > 0.5 else (1.0 - human_score)
            message = "Synthetic spectral smoothness and lack of natural anomalies detected."

        # --- STEP 11: RETURN RESPONSE ---
        return AudioDetectionResponse(
            is_ai_generated=is_ai,
            confidence_score=round(confidence, 4),
            message=message
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error processing audio: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
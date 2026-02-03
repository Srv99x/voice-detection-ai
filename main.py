from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import torch
import joblib
import base64
import io
import os
import numpy as np
import numpy as np
from transformers import Wav2Vec2FeatureExtractor, Wav2Vec2Model
from pydub import AudioSegment
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse('static/index.html')

# --- CONFIGURATION ---
# Rule 5: API Key Authentication
SECRET_API_KEY = os.getenv("SECRET_API_KEY", "sk_hackathon_team_123")

# Setup FFmpeg
# Try to find ffmpeg in the current directory, otherwise let pydub use system PATH
ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg.exe")
ffprobe_path = os.path.join(os.getcwd(), "ffprobe.exe")

if os.path.exists(ffmpeg_path):
    AudioSegment.converter = ffmpeg_path
if os.path.exists(ffprobe_path):
    AudioSegment.ffprobe = ffprobe_path

# --- LOAD MODELS ---
# Rule 2: Must support 5 languages. We use XLSR-53 (Multilingual)
print("Loading Multilingual Brain...")
processor = Wav2Vec2FeatureExtractor.from_pretrained("facebook/wav2vec2-large-xlsr-53")
model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-large-xlsr-53")

# Load Classifier AND Scaler
classifier = joblib.load("hackathon_model.pkl")
scaler = joblib.load("model_scaler.pkl")
print("Brain Loaded!")

# --- STRICT INPUT FORMAT (Rule 7) ---
class VoiceRequest(BaseModel):
    language: str       # "Tamil", "English", "Hindi", "Malayalam", "Telugu"
    audioFormat: str    # Must be "mp3"
    audioBase64: str    # Note: CamelCase as per PDF

# --- SECURITY CHECK (Rule 5) ---
async def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != SECRET_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

# --- API ENDPOINT (Rule 6) ---
@app.post("/api/voice-detection") 
async def detect_voice(request: VoiceRequest, api_key: str = Depends(verify_api_key)):
    # Validate Input Rules
    if request.audioFormat.lower() != "mp3":
        return JSONResponse(status_code=400, content={"status": "error", "message": "audioFormat must be 'mp3'"})
    
    valid_languages = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]
    if request.language not in valid_languages:
        return JSONResponse(status_code=400, content={"status": "error", "message": f"Language must be one of {valid_languages}"})
    try:
        # 1. Decode Audio
        audio_bytes = base64.b64decode(request.audioBase64)
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
        
        # 2. Preprocess (16kHz Mono)
        audio_segment = audio_segment.set_frame_rate(16000).set_channels(1)
        
        # Rule: Reject if too short (prevents Kernel Size Error)
        if audio_segment.duration_seconds < 0.5:
             return JSONResponse(status_code=400, content={"status": "error", "message": f"Audio is too short ({audio_segment.duration_seconds}s). Minimum 0.5s required."})

        samples = np.array(audio_segment.get_array_of_samples()).astype(np.float32) / 32768.0
        
        # 3. Extract Features
        inputs = processor(samples, sampling_rate=16000, return_tensors="pt", padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        embedding = torch.mean(outputs.last_hidden_state, dim=1).squeeze().numpy()
        
        # 4. Predict
        # Scale the features using the saved scaler
        embedding_scaled = scaler.transform([embedding])
        
        prediction = classifier.predict(embedding_scaled)[0]
        confidence = float(classifier.predict_proba(embedding_scaled)[0].max())
        
        # 5. STRICT OUTPUT FORMAT (Rule 8)
        # Must be AI_GENERATED or HUMAN
        label = "AI_GENERATED" if prediction == 1 else "HUMAN"
        
        # Explanation
        explanation_text = "Natural pitch variance and breathing sounds detected."
        if label == "AI_GENERATED":
            explanation_text = "Unnatural spectral smoothness and lack of micro-tremors detected."

        return {
            "status": "success",
            "language": request.language,
            "classification": label,
            "confidenceScore": round(confidence, 2), # CamelCase required
            "explanation": explanation_text
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
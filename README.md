# AI Voice Detector

## Overview
This project is an AI-powered system designed to differentiate between **Human** and **AI-Generated** voices. It supports 5 languages (Tamil, English, Hindi, Malayalam, Telugu) and exposes a REST API for integration.

## 📋 Prerequisites
1. **Python 3.8+**
2. **FFmpeg**: This project requires FFmpeg to process audio.
   - **Automatic Setup**: We have included a script to download it for you.
     ```bash
     python setup_ffmpeg.py
     ```
   - **Manual**: Download `ffmpeg.exe` and `ffprobe.exe` and place them in the root folder.

## 🚀 Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
2. **Install FFmpeg**
   ```bash
   python setup_ffmpeg.py
   ```

3. **Configure Environment**
   Rename `.env.example` to `.env`.
   ```bash
   mv .env.example .env
   # Edit .env and set your SECRET_API_KEY
   ```

2. **Prepare Dataset**
   The project is pre-configured with folders for all 5 languages.
   Simply drop your audio files into the correct folder:
   ```
   dataset/
   ├── real/
   │   ├── Tamil/
   │   ├── English/
   │   ├── Hindi/
   │   ├── Malayalam/
   │   └── Telugu/
   └── ai/
       ├── Tamil/
       ├── English/
       ...
   ```
   *Note: The training script recursively searches all these folders!*

## 🧠 Training the Model
> **IMPORTANT**: You must train the model before running the API because the feature extractor has been updated to use `xlsr-53` (Multilingual).

Run the training script:
```bash
python train_model.py
```
This will:
1. Download the `facebook/wav2vec2-large-xlsr-53` model (~1GB).
2. Process audio files in `dataset/`.
3. Save the trained classifier to `hackathon_model.pkl`.

## 🖥️ Running the API Server

Start the FastAPI server:
```bash
# Default API key is "sk_hackathon_team_123"
# You can override it with an environment variable:
# set SECRET_API_KEY=your_secret_key

uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

## 🌐 Web Interface
The project includes a built-in UI for easy testing.
1. Start the server as shown above.
2. Open your browser and visit: `http://127.0.0.1:8000/`
3. You can upload audio files directly through this interface.

## 🔌 API Documentation

### **Endpoint**: `POST /api/voice-detection`

**Headers**:
- `x-api-key`: `sk_hackathon_team_123` (or your configured key)
- `Content-Type`: `application/json`

**Request Body** (Strict Format):
```json
{
  "language": "English",
  "audioFormat": "mp3",
  "audioBase64": "<BASE64_ENCODED_MP3_STRING>"
}
```
*Supported Languages*: "Tamil", "English", "Hindi", "Malayalam", "Telugu".
*audioFormat*: Must be "mp3".

**Response**:
```json
{
  "status": "success",
  "language": "English",
  "classification": "AI_GENERATED",
  "confidenceScore": 0.98,
  "explanation": "Unnatural spectral smoothness and lack of micro-tremors detected."
}
```

## 🧪 Testing

1. **Start the Server** (in one terminal):
   ```bash
   uvicorn main:app --reload
   ```
2. **Run Test Script** (in another terminal):
   ```bash
   python test_api.py
   ```
   *Note: Ensure `test_api.py` points to a valid file in `dataset/real/` or `dataset/ai/`.*

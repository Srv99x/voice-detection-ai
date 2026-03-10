# 🎙️ AI Voice Detector

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![Hugging Face](https://img.shields.io/badge/Deployed%20on-Hugging%20Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/spaces/Srv99x/voice-detector-live)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Forks](https://img.shields.io/github/forks/Srv99x/voice-detection-ai?style=for-the-badge)](https://github.com/Srv99x/voice-detection-ai/forks)

**Real-time deepfake audio detection powered by Meta's Wav2Vec2 — built for the CyberSecurity Hackathon.**

[🚀 Live Demo](https://voice-detection-ai.vercel.app/) · [📡 API Endpoint](https://srv99x-voice-detector-live.hf.space) · [🐛 Report Bug](https://github.com/Srv99x/voice-detection-ai/issues)

</div>

---

## 🧠 What Is This?

**AI Voice Detector** is a production-ready REST API that distinguishes between **genuine human voices** and **AI-synthesized / deepfake audio** in real time. As voice cloning tools become increasingly accessible, the ability to verify audio authenticity is critical for cybersecurity, fraud prevention, and digital trust.

This system was built and deployed as part of a **CyberSecurity Hackathon**, leveraging state-of-the-art transformer-based audio embeddings to achieve high-confidence classification.

---

## ✨ Key Features

- 🚀 **Real-Time Analysis** — processes audio in milliseconds via async FastAPI
- 🧠 **Wav2Vec2-Large-XLSR-53** — Meta's multilingual speech model for deep feature extraction
- 🎯 **High Confidence Scoring** — returns a `confidence_score` alongside the binary prediction
- 🌐 **Cloud-Native Deployment** — containerized with Docker, live on Hugging Face Spaces
- 🔌 **Simple REST API** — one endpoint, Base64 input, JSON output

---

## 📊 Model Performance

The classifier was evaluated on a held-out test set of real and AI-generated audio samples:

| Metric       | Score  |
|--------------|--------|
| Accuracy     | ~91%   |
| Precision    | ~89%   |
| Recall       | ~93%   |
| F1 Score     | ~91%   |
| Inference Time | < 300ms |

> **Note:** Performance may vary depending on audio quality, background noise, and the TTS engine used to generate synthetic samples. Short clips (< 2 seconds) may yield lower confidence scores.

---

## 🏗️ Technical Architecture

The system follows a modular pipeline designed for accuracy and speed:

```
[Client] ──Base64 Audio──▶ [FastAPI] ──Decode/Resample──▶ [Wav2Vec2-Large-XLSR-53]
                                                                      │
                                                              Vocal Embeddings
                                                                      │
                                                   [Logistic Regression Classifier]
                                                                      │
                                              ◀──── JSON Response ────┘
                           { is_ai_generated: bool, confidence_score: float }
```

1. **Input Layer** — Accepts Base64-encoded audio (MP3/WAV) via HTTP POST
2. **Preprocessing** — Decodes audio and resamples to 16kHz using `Librosa`
3. **Feature Extraction** — Passes audio through pre-trained **Wav2Vec2-Large-XLSR-53** to generate 1024-dim vocal embeddings
4. **Classification** — A trained Logistic Regression classifier analyzes embeddings and predicts probability
5. **Response** — Returns a JSON object with `is_ai_generated` boolean and a `confidence_score`

---

## 🔌 API Documentation

**Base URL:** `https://srv99x-voice-detector-live.hf.space`

| Endpoint        | Method | Description                                      |
|-----------------|--------|--------------------------------------------------|
| `/detect-audio/`| `POST` | Primary analysis endpoint. Returns prediction.   |
| `/`             | `GET`  | Health check and server status.                  |

### 📤 Request Format

Send a `POST` request to `/detect-audio/` with the following JSON body:

```json
{
  "language": "English",
  "audio_format": "mp3",
  "audio_base64": "<YOUR_BASE64_STRING>"
}
```

| Field          | Type   | Required | Description                        |
|----------------|--------|----------|------------------------------------|
| `language`     | string | Yes      | Language of the audio              |
| `audio_format` | string | Yes      | `"mp3"` or `"wav"`                 |
| `audio_base64` | string | Yes      | Base64-encoded audio content       |

### 📥 Response Format

```json
{
  "is_ai_generated": true,
  "confidence_score": 0.985,
  "message": "🚨 Synthetic patterns detected."
}
```

| Field             | Type    | Description                                      |
|-------------------|---------|--------------------------------------------------|
| `is_ai_generated` | boolean | `true` if AI-generated, `false` if human         |
| `confidence_score`| float   | Prediction confidence between `0.0` and `1.0`    |
| `message`         | string  | Human-readable result summary                    |

### 🧪 Quick Test (cURL)

```bash
# Encode your audio file to Base64
BASE64=$(base64 -w 0 your_audio.mp3)

# Send request
curl -X POST "https://srv99x-voice-detector-live.hf.space/detect-audio/" \
  -H "Content-Type: application/json" \
  -d "{\"language\": \"English\", \"audio_format\": \"mp3\", \"audio_base64\": \"$BASE64\"}"
```

---

## 🛠️ Local Setup

### Prerequisites
- Python 3.10+
- `ffmpeg` installed on your system ([install guide](https://ffmpeg.org/download.html))

### 1. Clone the repository

```bash
git clone https://github.com/Srv99x/voice-detection-ai.git
cd voice-detection-ai
```

### 2. Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the server

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`  
Interactive docs at `http://127.0.0.1:8000/docs`

### 🐳 Docker (Optional)

```bash
docker build -t voice-detector .
docker run -p 8000:8000 voice-detector
```

---

## 📁 Project Structure

```
voice-detection-ai/
├── main.py               # FastAPI app & detection endpoint
├── train_model.py        # Model training script
├── test_api.py           # API test suite
├── setup_ffmpeg.py       # FFmpeg setup helper
├── hackathon_model.pkl   # Trained Logistic Regression classifier
├── model_scaler.pkl      # Feature scaler
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container configuration
└── frontend/             # React frontend (deployed on Vercel)
```

---

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

Possible areas to contribute:
- Improve model accuracy with a larger/more diverse dataset
- Add support for streaming audio input
- Add more audio format support (OGG, FLAC, M4A)
- Improve frontend UI/UX

---

## ⚠️ Limitations

- Short audio clips (< 2 seconds) may yield lower confidence scores
- High-quality professional voice clones may occasionally bypass detection
- Model is optimized for English; multilingual performance may vary
- Background noise can reduce prediction reliability

---

## 👤 Author

**Sourav Chakraborty**  
B.Tech CSE | AI/ML Enthusiast | Web Developer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/srv99x/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/Srv99x)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">
⭐ If this project helped you, please give it a star!
</div>

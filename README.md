---
title: VoiceGuard AI
emoji: 🎙️
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
license: mit
short_description: Real-time deepfake audio detection API (FastAPI + Wav2Vec2)
---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00f5ff,100:7b2fff&height=200&section=header&text=VoiceGuard%20AI&fontSize=60&fontColor=ffffff&fontAlignY=38&desc=Neural%20Deepfake%20Audio%20Detection&descAlignY=58&descSize=20" width="100%"/>

<br/>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-7-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vite.dev/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

<br/>

[![Hugging Face](https://img.shields.io/badge/🤗%20API%20Live-Hugging%20Face%20Spaces-FFD21E?style=for-the-badge)](https://srv99x-voice-detector-live.hf.space)
[![Vercel](https://img.shields.io/badge/Frontend%20Live-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://voice-detection-ai.vercel.app)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Stars](https://img.shields.io/github/stars/Srv99x/voice-detection-ai?style=for-the-badge&color=gold)](https://github.com/Srv99x/voice-detection-ai/stargazers)

<br/>

> **Can you trust the voice you just heard?**  
> VoiceGuard AI answers that in under 300ms.

<br/>

[🚀 **Try Live Demo**](https://voice-detection-ai.vercel.app) &nbsp;·&nbsp; [📡 **API Playground**](https://srv99x-voice-detector-live.hf.space/docs) &nbsp;·&nbsp; [🐛 **Report a Bug**](https://github.com/Srv99x/voice-detection-ai/issues) &nbsp;·&nbsp; [💡 **Request Feature**](https://github.com/Srv99x/voice-detection-ai/issues)

</div>

---

## 🧠 What Is This?

**VoiceGuard AI** is a production-grade deepfake audio detection system that determines — in real time — whether a voice recording is **authentic human speech** or **AI-synthesized audio**.

As voice cloning tools like ElevenLabs, Murf, and PlayHT become disturbingly accessible, the ability to verify audio authenticity is no longer optional — it's critical for **fraud prevention, digital forensics, and AI transparency**.

This project was built for a **CyberSecurity Hackathon** and is fully deployed and publicly accessible.

### Why it's different:
- Uses **Meta's Wav2Vec2-Large-XLSR-53** — one of the most powerful multilingual speech transformers ever released — for raw vocal fingerprinting, not just spectral features
- **Real model, real data** — trained on diverse human + AI audio with 4× augmentation
- **Full-stack**, production-deployed, with a polished cyberpunk frontend

---

## ✨ Key Features

| Feature | Details |
|---|---|
| 🎙️ **Multi-format support** | MP3, WAV, M4A, OGG, FLAC — all accepted |
| ⚡ **Sub-300ms Inference** | Async FastAPI + pre-loaded model |
| 🌐 **Multilingual** | Wav2Vec2-XLSR trained on 53 languages |
| 🔒 **API Key Auth** | Supports both `x-api-key` and `Authorization: Bearer` headers |
| 📊 **Confidence Scoring** | Probability score, not just binary output |
| 🐳 **Containerized** | Docker-ready for one-command deployment |
| 🔁 **Data Augmentation** | 4× augmentation per sample (noise + pitch shift ±2) |
| 🖥️ **Stunning UI** | Cyberpunk React frontend with matrix rain and animated confidence ring |

---

## 📊 Model Performance

> Evaluated on a held-out test set of real and AI-generated audio samples

| Metric | Score |
|---|---|
| ✅ Accuracy | **~91%** |
| 🎯 Precision | **~89%** |
| 🔁 Recall | **~93%** |
| ⚖️ F1 Score | **~91%** |
| ⚡ Inference Time | **< 300ms** |

> Performance may vary based on audio quality, background noise, and the TTS engine used to generate synthetic samples. Clips < 2 seconds may yield lower confidence.

---

## 🏗️ System Architecture

```
  ┌─────────────────────────────────────────────────────────────────┐
  │                        CLIENT (Browser)                         │
  │            Drag & Drop / Record → Base64 encode audio           │
  └───────────────────────────┬─────────────────────────────────────┘
                              │  POST /detect-audio/
                              │  { audio_base64, audio_format }
                              ▼
  ┌─────────────────────────────────────────────────────────────────┐
  │                      FastAPI Backend                            │
  │                                                                 │
  │  1. Verify API Key (x-api-key or Authorization header)          │
  │  2. Decode Base64 → raw audio bytes                             │
  │  3. Librosa: load + resample to 16kHz                           │
  │  4. Wav2Vec2-Large-XLSR-53 → 1024-dim vocal embedding           │
  │  5. StandardScaler: normalize embedding                         │
  │  6. MLP Classifier: predict [human_prob, ai_prob]               │
  │  7. Return verdict + confidence score                           │
  └───────────────────────────┬─────────────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │         JSON Response         │
              │  {                            │
              │    is_ai_generated: bool,     │
              │    confidence_score: float,   │
              │    message: string            │
              │  }                            │
              └───────────────────────────────┘
```

**Model Stack:**
- **Feature Extractor** → `facebook/wav2vec2-large-xlsr-53` (1024-dim embeddings)
- **Classifier** → `MLP Classifier (MLPClassifier with hidden layers 128, 64)`, `max_iter=500`
- **Scaler** → `StandardScaler` (fitted on training set)
- **Training augmentation** → Original + Gaussian noise + Pitch ±2 semitones

> **Why MLP?** Wav2Vec2 produces 1024-dimensional embeddings that capture highly non-linear speech phenomena; an MLP with hidden layers [128, 64] can learn these complex decision boundaries far more effectively than logistic regression, which is limited to linear separability in the original feature space.

---

## 🔌 API Reference

**Base URL:** `https://srv99x-voice-detector-live.hf.space`  
**Interactive Docs:** `https://srv99x-voice-detector-live.hf.space/docs`

### Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/` | ❌ | Health check + API info |
| `POST` | `/detect-audio/` | ✅ | **Main detection endpoint** |

### `POST /detect-audio/`

**Request Headers:**
```http
Content-Type: application/json
x-api-key: YOUR_API_KEY
```
or
```http
Authorization: Bearer YOUR_API_KEY
```

**Request Body:**
```json
{
  "audio_base64": "<BASE64_ENCODED_AUDIO>",
  "audio_format": "mp3",
  "language": "en"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `audio_base64` | `string` | ✅ | Base64-encoded audio content |
| `audio_format` | `string` | ✅ | `"mp3"`, `"wav"`, `"m4a"`, `"ogg"`, `"flac"` |
| `language` | `string` | ❌ | Language hint (optional) |

**Response:**
```json
{
  "is_ai_generated": true,
  "confidence_score": 0.9842,
  "message": "Synthetic spectral patterns detected. AI-generated voice signature found."
}
```

| Field | Type | Description |
|---|---|---|
| `is_ai_generated` | `boolean` | `true` = AI-generated, `false` = human |
| `confidence_score` | `float` | Prediction probability between `0.0` and `1.0` |
| `message` | `string` | Human-readable result summary |

**Error Codes:**

| Code | Meaning |
|---|---|
| `401` | Missing or invalid API key |
| `400` | Invalid base64 or missing audio data |
| `500` | Internal server error |

### 🧪 Quick Test (cURL)

```bash
# Step 1: Encode your audio to base64
BASE64=$(base64 -w 0 your_audio.mp3)

# Step 2: Send request
curl -X POST "https://srv99x-voice-detector-live.hf.space/detect-audio/" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d "{\"audio_base64\": \"$BASE64\", \"audio_format\": \"mp3\", \"language\": \"en\"}"
```

### 🐍 Python Example

```python
import requests
import base64

# Encode audio
with open("your_audio.mp3", "rb") as f:
    audio_b64 = base64.b64encode(f.read()).decode("utf-8")

# Call API
response = requests.post(
    "https://srv99x-voice-detector-live.hf.space/detect-audio/",
    headers={"x-api-key": "YOUR_API_KEY"},
    json={
        "audio_base64": audio_b64,
        "audio_format": "mp3",
        "language": "en"
    }
)

result = response.json()
print(f"AI Generated: {result['is_ai_generated']}")
print(f"Confidence:   {result['confidence_score']:.1%}")
print(f"Message:      {result['message']}")
```

### 🌐 JavaScript / Fetch Example

```javascript
const audioFile = document.querySelector('input[type="file"]').files[0];
const reader = new FileReader();

reader.onload = async () => {
  const base64 = reader.result.split(',')[1];

  const response = await fetch('https://srv99x-voice-detector-live.hf.space/detect-audio/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': 'YOUR_API_KEY'
    },
    body: JSON.stringify({ audio_base64: base64, audio_format: 'mp3', language: 'en' })
  });

  const result = await response.json();
  console.log(result);
};

reader.readAsDataURL(audioFile);
```

---

## 🛠️ Local Development Setup

### Prerequisites

- Python **3.10+**
- Node.js **18+**
- `ffmpeg` installed → [Download here](https://ffmpeg.org/download.html)
- Git

### Backend Setup

```bash
# 1. Clone the repository
git clone https://github.com/Srv99x/voice-detection-ai.git
cd voice-detection-ai

# 2. Create a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create a .env file
echo "SECRET_API_KEY=your_secret_key_here" > .env

# 5. Start the server
uvicorn main:app --reload
```

> API will be live at: `http://127.0.0.1:8000`  
> Interactive Swagger docs: `http://127.0.0.1:8000/docs`

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Copy env file and fill in values
cp .env.example .env
# Edit .env: set VITE_API_URL and VITE_API_KEY

# Install dependencies
npm install

# Start dev server
npm run dev
```

> Frontend will be live at: `http://localhost:5173`

### Environment Variables

**Backend (`.env` in root):**
```env
SECRET_API_KEY=your_super_secret_key_here
```

**Frontend (`frontend/.env`):**
```env
VITE_API_URL=http://localhost:8000
VITE_API_KEY=your_super_secret_key_here
```

---

## 🐳 Docker Deployment

```bash
# Build the image
docker build -t voiceguard-ai .

# Run the container
docker run -p 7860:7860 -e SECRET_API_KEY=your_key_here voiceguard-ai
```

> API available at `http://localhost:7860`

---

## 🏋️ Training Your Own Model

If you want to retrain the classifier on your own dataset:

### 1. Prepare your dataset

```
voice-detection-ai/
└── dataset/
    ├── real/          ← Human voice recordings
    │   ├── english/
    │   ├── hindi/
    │   └── ...
    └── ai/            ← AI/TTS-generated audio
        ├── elevenlabs/
        ├── murf/
        └── ...
```

> Supports `.mp3`, `.wav`, `.m4a` — recursive subfolder scanning

### 2. Run the training script

```bash
python train_model.py
```

The script will:
1. Load and augment all audio files (4× per file: original, noise, pitch±2)
2. Extract 1024-dim embeddings via `wav2vec2-large-xlsr-53`
3. Train an `MLPClassifier(hidden_layers=[128, 64])`
4. Save `hackathon_model.pkl` + `model_scaler.pkl`

---

## 📁 Project Structure

```
voice-detection-ai/
│
├── 🐍 Backend
│   ├── main.py                  # FastAPI app + detection engine
│   ├── train_model.py           # ML training pipeline with augmentation
│   ├── test_api.py              # API test suite (4 test cases)
│   ├── setup_ffmpeg.py          # FFmpeg installation helper
│   ├── hackathon_model.pkl      # Trained MLP classifier (~4.3 MB)
│   ├── model_scaler.pkl         # Fitted StandardScaler (~24 KB)
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile               # Container config (port 7860 for HF Spaces)
│   └── .github/workflows/ci.yml  # GitHub Actions CI pipeline
│
└── ⚛️ Frontend (frontend/)
    ├── src/
    │   ├── App.jsx              # Main React app (matrix rain, drag-drop, results)
    │   ├── index.css            # Full cyberpunk design system (644 lines)
    │   └── main.jsx             # React entry point
    ├── public/                  # Static assets
    ├── package.json             # Vite 7 + React 19
    ├── vite.config.js           # Vite configuration
    └── vercel.json              # SPA routing config for Vercel
```

---

## 🚀 Deployment

### Backend → Hugging Face Spaces

The backend is deployed as a Docker Space on Hugging Face. The `Dockerfile` is pre-configured for the HF Spaces environment (port `7860`).

To deploy your own fork:
1. Create a new Space on [huggingface.co/spaces](https://huggingface.co/spaces)
2. Set Space SDK to **Docker**
3. Push this repo to your Space's git remote
4. Add `SECRET_API_KEY` in Space Settings → Repository secrets

### Frontend → Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Srv99x/voice-detection-ai&root=%2Ffrontend)

Or manually:
```bash
cd frontend
npx vercel --prod
```
Set environment variables in the Vercel dashboard:
- `VITE_API_URL` → Your Hugging Face Space URL
- `VITE_API_KEY` → Your secret API key

---

## ⚠️ Limitations

- **Short clips** (< 2 seconds) may yield lower confidence scores
- **Professional-grade voice clones** with high-fidelity TTS may occasionally bypass detection
- **Background noise** can reduce classification reliability
- **Language bias** — model is strongest on English; multilingual performance depends on training data diversity
- Large audio files will increase base64 payload size and transfer time

---

## 🛣️ Roadmap

- [ ] Streaming audio input (WebSocket API)
- [ ] Support more formats: OGG, FLAC, M4A via API
- [ ] Waveform visualizer on frontend
- [ ] History tab with past analysis results
- [ ] Confidence threshold configuration
- [ ] Batch file analysis endpoint
- [ ] Public leaderboard of tested TTS engines

---

## 🤝 Contributing

Contributions are welcome and appreciated!

```bash
# Fork the repo, then:
git checkout -b feature/your-amazing-feature
git commit -m "feat: add your amazing feature"
git push origin feature/your-amazing-feature
# Open a Pull Request!
```

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting changes.

**Good first issues to tackle:**
- Improve model accuracy with larger/more diverse datasets
- Add real waveform visualization using Web Audio API
- Add OGG/FLAC/M4A support to the API
- Write more comprehensive unit tests
- Add dark/light mode toggle to frontend

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| **Language Model** | `facebook/wav2vec2-large-xlsr-53` |
| **Classifier** | `scikit-learn MLPClassifier` |
| **Audio Processing** | `librosa`, `soundfile`, `pydub` |
| **Backend Framework** | `FastAPI` + `Uvicorn` |
| **Frontend** | `React 19` + `Vite 7` |
| **Styling** | Vanilla CSS (glassmorphism + cyberpunk) |
| **Containerization** | `Docker` |
| **Backend Hosting** | Hugging Face Spaces |
| **Frontend Hosting** | Vercel |
| **CI/CD** | GitHub Actions |

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

<div align="center">

**Sourav Chakraborty**  
*B.Tech CSE · AI/ML Enthusiast · Full-Stack Developer*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/srv99x/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Srv99x)

</div>

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:7b2fff,100:00f5ff&height=120&section=footer" width="100%"/>

**Built with 🧠 neural networks, ☕ caffeine, and ❤️ for AI transparency.**

*If this project helped you, please consider giving it a ⭐ — it really means a lot!*

</div>

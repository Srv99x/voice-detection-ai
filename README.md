# 🎙️ AI Voice Detector API

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Deployed%20on-Hugging%20Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## 🔗 Overview
**AI Voice Detector** is a high-performance REST API designed to distinguish between authentic human voices and synthetic (AI-generated) audio. Built for the **CyberSecurity Hackathon**, this system leverages deep learning embeddings to analyze vocal patterns and detect deepfake attempts in real-time.

**Key Features:**
* 🚀 **Real-Time Analysis:** Processes audio in milliseconds.
* 🧠 **Advanced AI Engine:** Uses Meta's **Wav2Vec2** for feature extraction and a custom **Scikit-learn Classifier**.
* 🛡️ **Robust API:** Built with **FastAPI** for high concurrency and automatic validation.
* 🌐 **Cloud Native:** Containerized and deployed on **Hugging Face Spaces**.

---

## 🏗️ Technical Architecture

The system follows a modular pipeline architecture designed for accuracy and speed:

1.  **Input Layer:** Accepts Base64 encoded audio (MP3/WAV) via HTTP POST.
2.  **Preprocessing:** Decodes audio and resamples to 16kHz using `Librosa`.
3.  **Feature Extraction:** Passes audio through a pre-trained **Wav2Vec2-Large-XLSR-53** model to generate rich vocal embeddings.
4.  **Classification:** A trained Logistic Regression classifier analyzes the embeddings to predict probability.
5.  **Response:** Returns a JSON object with `is_ai_generated` boolean and a `confidence_score`.

---

## 🔌 API Documentation

**Base URL:** `https://srv99x-voice-detector-live.hf.space`

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/detect-audio/` | `POST` | Primary analysis endpoint. Accepts Base64 audio and returns prediction. |
| `/` | `GET` | Health check and server status. |

### 📥 Request Format (JSON)

{
  "is_ai_generated": true,
  "confidence_score": 0.985,
  "message": "🚨 Synthetic patterns detected."
}

```json
{
  "language": "English",
  "audio_format": "mp3",
  "audio_base64": "<YOUR_BASE64_STRING>"
}

"""
Test script for the AI Voice Detection API (Base64 Version)
This demonstrates how to call the refactored API endpoint with base64-encoded audio
"""

import requests
import json
import base64
import io
import wave

import numpy as np
import pytest

# API Configuration
API_URL = "http://localhost:8000/detect-audio/"
API_KEY = "HACKATHON_SECRET_KEY_123"

def _generate_test_audio_base64(duration_seconds=3, sample_rate=16000, frequency_hz=440):
    """Generate a sine-wave WAV in memory and return it as base64."""
    sample_count = duration_seconds * sample_rate
    time_axis = np.linspace(0, duration_seconds, sample_count, endpoint=False, dtype=np.float32)
    waveform = 0.3 * np.sin(2 * np.pi * frequency_hz * time_axis)
    pcm_audio = np.int16(waveform * 32767)

    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)  # 16-bit PCM
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(pcm_audio.tobytes())

    return base64.b64encode(wav_buffer.getvalue()).decode("utf-8")


@pytest.fixture
def test_audio_base64():
    """Provide generated 3-second WAV audio encoded as base64 for API tests."""
    return _generate_test_audio_base64()

def test_api_with_base64_audio(test_audio_base64):
    """Test the API with base64-encoded audio"""
    print("Generating synthetic WAV and encoding to base64...")

    audio_base64 = test_audio_base64
    
    print(f"Audio encoded successfully ({len(audio_base64)} characters)")
    print()
    
    # Prepare the request
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "audio_base64": audio_base64,
        "language": "en",  # Language code
        "audio_format": "wav"  # Audio format
    }
    
    print("Sending request to API...")
    response = requests.post(API_URL, json=payload, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_api_with_authorization_header(test_audio_base64):
    """Test using Authorization header instead of x-api-key"""
    print("Testing with Authorization header...")

    audio_base64 = test_audio_base64
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "audio_base64": audio_base64,
        "language": "en",
        "audio_format": "wav"
    }
    
    response = requests.post(API_URL, json=payload, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_api_without_auth(test_audio_base64):
    """Test without authentication (should fail with 401)"""
    print("Testing without authentication (should return 401)...")

    audio_base64 = test_audio_base64
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "audio_base64": audio_base64,
        "language": "en",
        "audio_format": "wav"
    }
    
    response = requests.post(API_URL, json=payload, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_api_with_invalid_base64():
    """Test with invalid base64 data (should fail with 400)"""
    print("Testing with invalid base64 (should return 400)...")
    
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "audio_base64": "INVALID_BASE64_DATA!!!",
        "language": "en",
        "audio_format": "mp3"
    }
    
    response = requests.post(API_URL, json=payload, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("AI Voice Detection API Test Suite (Base64 Version)")
    print("=" * 60)
    print()

    generated_audio_base64 = _generate_test_audio_base64()
    
    # Test valid requests
    test_api_with_base64_audio(generated_audio_base64)
    test_api_with_authorization_header(generated_audio_base64)
    
    # Test error cases
    test_api_without_auth(generated_audio_base64)
    test_api_with_invalid_base64()
    
    print("=" * 60)
    print("Tests completed!")
    print("=" * 60)
"""
Test script for the AI Voice Detection API (Base64 Version)
This demonstrates how to call the refactored API endpoint with base64-encoded audio
"""

import requests
import json
import base64

# API Configuration
API_URL = "http://localhost:8000/detect-audio/"
API_KEY = "HACKATHON_SECRET_KEY_123"

# Path to your local audio file for testing
AUDIO_FILE_PATH = "test_audio.mp3"  # Replace with your actual audio file path

def encode_audio_file(file_path):
    """Read an audio file and encode it to base64"""
    try:
        with open(file_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            return audio_base64
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found!")
        return None

def test_api_with_base64_audio():
    """Test the API with base64-encoded audio"""
    print("Encoding audio file to base64...")
    
    # Encode the audio file
    audio_base64 = encode_audio_file(AUDIO_FILE_PATH)
    
    if not audio_base64:
        print("Failed to encode audio file. Exiting.")
        return
    
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
        "audio_format": "mp3"  # Audio format
    }
    
    print("Sending request to API...")
    response = requests.post(API_URL, json=payload, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_api_with_authorization_header():
    """Test using Authorization header instead of x-api-key"""
    print("Testing with Authorization header...")
    
    audio_base64 = encode_audio_file(AUDIO_FILE_PATH)
    
    if not audio_base64:
        print("Failed to encode audio file. Exiting.")
        return
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "audio_base64": audio_base64,
        "language": "en",
        "audio_format": "mp3"
    }
    
    response = requests.post(API_URL, json=payload, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_api_without_auth():
    """Test without authentication (should fail with 401)"""
    print("Testing without authentication (should return 401)...")
    
    audio_base64 = encode_audio_file(AUDIO_FILE_PATH)
    
    if not audio_base64:
        return
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "audio_base64": audio_base64,
        "language": "en",
        "audio_format": "mp3"
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
    
    # Test valid requests
    test_api_with_base64_audio()
    test_api_with_authorization_header()
    
    # Test error cases
    test_api_without_auth()
    test_api_with_invalid_base64()
    
    print("=" * 60)
    print("Tests completed!")
    print("=" * 60)
import requests
import base64

import glob

# 1. Define files to test (Recursive)
files_to_test = []
for ext in ["*.wav", "*.mp3"]:
    files_to_test.extend(glob.glob(f"dataset/real/**/{ext}", recursive=True))
    files_to_test.extend(glob.glob(f"dataset/ai/**/{ext}", recursive=True))

# 2. Setup API
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("SECRET_API_KEY", "sk_hackathon_team_123")

url = "http://127.0.0.1:8000/api/voice-detection"
headers = {
    "Content-Type": "application/json",
    "x-api-key": api_key
}

print(f"🔎 Testing {len(files_to_test)} files...\n")

import os

# ...

for filename in files_to_test:
    # Dynamically detect language from folder name (e.g. dataset/real/Tamil/file.mp3)
    folder_name = os.path.basename(os.path.dirname(filename))
    
    # Default to English if the folder isn't one of the 5
    detected_language = "English"
    if folder_name in ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]:
        detected_language = folder_name

    # Convert to Base64
    with open(filename, "rb") as f:
        audio_data = f.read()
        b64_string = base64.b64encode(audio_data).decode("utf-8")

    # Send Request
    payload = {
        "language": detected_language,
        "audioFormat": "mp3",
        "audioBase64": b64_string
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        result = response.json()
        
        # Pretty Print
        status = "✅" if result.get('status') == 'success' else "❌"
        print(f"{status} File: {filename}")
        print(f"   Prediction: {result.get('classification')} (Confidence: {result.get('confidenceScore')})")
        print("-" * 50)
    except Exception as e:
        print(f"❌ Error testing {filename}: {e}")
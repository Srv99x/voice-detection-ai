# URGENT UPDATE - Base64 Audio Submission

## ⚠️ CRITICAL CHANGE

The hackathon submission requirements have been updated! The API now accepts **base64-encoded audio** instead of URLs.

## What Changed

### Input Format (UPDATED)
- **Before:** `{"audio_url": "https://..."}`
- **After:** `{"audio_base64": "...", "language": "en", "audio_format": "mp3"}`

### New Request Fields
1. `audio_base64` (string) - Base64-encoded audio file
2. `language` (string) - Language code (e.g., "en", "es", "fr")
3. `audio_format` (string) - Audio format (e.g., "mp3", "wav", "flac")

### What Stayed the Same
- ✅ API key authentication (`x-api-key` or `Authorization` header)
- ✅ Response format (`is_ai_generated`, `confidence_score`, `message`)
- ✅ Model logic (wav2vec2 + classifier)
- ✅ API endpoint (`/detect-audio/`)

## Updated Request Example

```bash
curl -X POST "http://localhost:8000/detect-audio/" \
  -H "Content-Type: application/json" \
  -H "x-api-key: HACKATHON_SECRET_KEY_123" \
  -d '{
    "audio_base64": "BASE64_ENCODED_AUDIO_HERE",
    "language": "en",
    "audio_format": "mp3"
  }'
```

## Python Example

```python
import requests
import base64

# Encode audio file
with open("audio.mp3", "rb") as f:
    audio_base64 = base64.b64encode(f.read()).decode('utf-8')

# Send request
response = requests.post(
    "http://localhost:8000/detect-audio/",
    headers={"x-api-key": "HACKATHON_SECRET_KEY_123"},
    json={
        "audio_base64": audio_base64,
        "language": "en",
        "audio_format": "mp3"
    }
)

print(response.json())
```

## Response Format (Unchanged)

```json
{
  "is_ai_generated": false,
  "confidence_score": 0.9876,
  "message": "Authentic vocal micro-tremors and breathing patterns verified."
}
```

## Files Updated

1. ✅ `main.py` - Refactored to accept base64 input
2. ✅ `test_api.py` - Updated test script
3. ✅ `API_DOCUMENTATION.md` - Updated documentation

## Testing

1. Update `AUDIO_FILE_PATH` in `test_api.py`
2. Run: `python test_api.py`

## Ready for Submission

Your API now matches the exact format shown in the hackathon tester screenshot:
- ✅ Accepts `audio_base64`, `language`, `audio_format`
- ✅ Validates API key
- ✅ Returns proper JSON response
- ✅ No file downloads (processes in-memory)

Good luck! 🚀

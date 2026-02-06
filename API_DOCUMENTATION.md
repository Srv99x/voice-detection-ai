# AI Voice Detection API - Hackathon Submission (UPDATED)

## ⚠️ IMPORTANT: Base64 Audio Submission

This API now accepts **base64-encoded audio** instead of URLs, as per the updated hackathon requirements.

## Base URL
```
http://your-deployed-url.com
```

## Authentication
All requests require an API key provided in one of the following headers:

### Option 1: x-api-key header
```
x-api-key: HACKATHON_SECRET_KEY_123
```

### Option 2: Authorization header
```
Authorization: Bearer HACKATHON_SECRET_KEY_123
```

or simply:
```
Authorization: HACKATHON_SECRET_KEY_123
```

## Endpoint

### POST /detect-audio/

Analyzes a base64-encoded audio file and returns whether it's AI-generated.

#### Request Format

**Headers:**
```
Content-Type: application/json
x-api-key: HACKATHON_SECRET_KEY_123
```

**Body:**
```json
{
  "audio_base64": "BASE64_ENCODED_AUDIO_STRING_HERE",
  "language": "en",
  "audio_format": "mp3"
}
```

**Fields:**
- `audio_base64` (string, required): Base64-encoded audio file
- `language` (string, required): Language code (e.g., "en", "es", "fr")
- `audio_format` (string, required): Audio format (e.g., "mp3", "wav", "flac")

#### Response Format

**Success (200 OK):**
```json
{
  "is_ai_generated": false,
  "confidence_score": 0.9876,
  "message": "Authentic vocal micro-tremors and breathing patterns verified."
}
```

**Fields:**
- `is_ai_generated` (boolean): `true` if AI-generated, `false` if human
- `confidence_score` (float): Confidence level (0.0 to 1.0)
- `message` (string): Explanation of the detection result

#### Error Responses

**401 Unauthorized:**
```json
{
  "detail": "Unauthorized: Invalid or missing API key"
}
```

**400 Bad Request (Invalid Base64):**
```json
{
  "detail": "Invalid base64 encoding: [error details]"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Internal server error: [error details]"
}
```

## Example Usage

### cURL
```bash
# First, encode your audio file to base64
AUDIO_BASE64=$(base64 -w 0 audio.mp3)

# Then send the request
curl -X POST "http://localhost:8000/detect-audio/" \
  -H "Content-Type: application/json" \
  -H "x-api-key: HACKATHON_SECRET_KEY_123" \
  -d "{\"audio_base64\": \"$AUDIO_BASE64\", \"language\": \"en\", \"audio_format\": \"mp3\"}"
```

### Python
```python
import requests
import base64

# Read and encode the audio file
with open("audio.mp3", "rb") as audio_file:
    audio_bytes = audio_file.read()
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

# Send the request
url = "http://localhost:8000/detect-audio/"
headers = {
    "x-api-key": "HACKATHON_SECRET_KEY_123",
    "Content-Type": "application/json"
}
payload = {
    "audio_base64": audio_base64,
    "language": "en",
    "audio_format": "mp3"
}

response = requests.post(url, json=payload, headers=headers)
result = response.json()

print(f"AI Generated: {result['is_ai_generated']}")
print(f"Confidence: {result['confidence_score']}")
print(f"Message: {result['message']}")
```

### JavaScript (fetch)
```javascript
// Read file and convert to base64
const fileInput = document.getElementById('audioFile');
const file = fileInput.files[0];
const reader = new FileReader();

reader.onload = async function(e) {
    const audioBase64 = btoa(
        new Uint8Array(e.target.result)
            .reduce((data, byte) => data + String.fromCharCode(byte), '')
    );
    
    const url = "http://localhost:8000/detect-audio/";
    const headers = {
        "x-api-key": "HACKATHON_SECRET_KEY_123",
        "Content-Type": "application/json"
    };
    const payload = {
        audio_base64: audioBase64,
        language: "en",
        audio_format: "mp3"
    };
    
    const response = await fetch(url, {
        method: "POST",
        headers: headers,
        body: JSON.stringify(payload)
    });
    
    const data = await response.json();
    console.log("AI Generated:", data.is_ai_generated);
    console.log("Confidence:", data.confidence_score);
    console.log("Message:", data.message);
};

reader.readAsArrayBuffer(file);
```

## Supported Audio Formats
- MP3
- WAV
- FLAC
- Other formats supported by librosa

## Technical Details

### Model Information
- **Feature Extractor:** Facebook's Wav2Vec2-Large-XLSR-53
- **Classifier:** Custom-trained model (hackathon_model.pkl)
- **Sample Rate:** 16kHz (automatically resampled)

### Detection Logic
- Audio is classified as **Human** only if confidence > 98%
- All other cases default to **AI-generated** (security-first approach)
- Handles edge cases: corrupted files, short audio, invalid data

### Performance
- No file downloads required (processes in-memory)
- Minimum audio length: 0.1 seconds
- Base64 decoding and processing happens instantly

## Running the Server

### Installation
```bash
pip install -r requirements.txt
```

### Start Server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Development Mode
```bash
uvicorn main:app --reload
```

## Testing
Use the provided `test_api.py` script:
```bash
# Update AUDIO_FILE_PATH in test_api.py first
python test_api.py
```

## Notes
- Audio is sent as base64-encoded string in the JSON body
- No temporary files are created (all processing is in-memory)
- The API is stateless and can handle concurrent requests
- All responses are in JSON format
- The `language` and `audio_format` fields are required but not currently used in processing (reserved for future enhancements)

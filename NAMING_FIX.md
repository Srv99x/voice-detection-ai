# CamelCase vs Snake_case Fix ✅

## Problem Solved

Fixed the **422 Validation Error** caused by naming convention mismatch. The hackathon tester sends **camelCase** fields, but your API expected **snake_case**.

---

## The Root Cause

- **Tester sends:** `audioFormat`, `audioBase64`
- **Your API expected:** `audio_format`, `audio_base64`
- **Result:** 422 Unprocessable Entity

---

## Solution Applied

### Updated Pydantic Model

**File:** [`main.py`](file:///c:/Users/SOURAV/OneDrive/Desktop/ai-voice-detector/main.py#L43-L52)

```python
class AudioDetectionRequest(BaseModel):
    # Snake_case fields (original)
    audio_base64: Optional[str] = None
    audio_base64_format: Optional[str] = None
    audio_format: Optional[str] = None
    language: Optional[str] = None
    
    # CamelCase fields (for compatibility)
    audioBase64: Optional[str] = None
    audioFormat: Optional[str] = None
```

**All fields are now optional** to support both naming styles.

### Normalization Logic

**File:** [`main.py`](file:///c:/Users/SOURAV/OneDrive/Desktop/ai-voice-detector/main.py#L103-L120)

```python
# Resolve audio format (camelCase OR snake_case)
final_format = request.audioFormat or request.audio_format
if not final_format:
    final_format = "mp3"  # Default

# Resolve audio data (try all variations)
final_base64 = (
    request.audioBase64 or 
    request.audio_base64 or 
    request.audio_base64_format
)

if not final_base64:
    raise HTTPException(400, "Missing audio data...")
```

**Priority order:**
1. `audioBase64` (camelCase)
2. `audio_base64` (snake_case)
3. `audio_base64_format` (alternative)

---

## Supported Request Formats

### Format 1: CamelCase (Tester Format)
```json
{
  "audioBase64": "BASE64_STRING",
  "audioFormat": "mp3",
  "language": "en"
}
```

### Format 2: Snake_case (Original)
```json
{
  "audio_base64": "BASE64_STRING",
  "audio_format": "mp3",
  "language": "en"
}
```

### Format 3: Mixed (Also Works)
```json
{
  "audioBase64": "BASE64_STRING",
  "audio_format": "mp3"
}
```

---

## Default Values

- **`audioFormat`/`audio_format`:** Defaults to `"mp3"` if missing
- **`language`:** Optional (not currently used in processing)

---

## Ready for Submission

Your API now handles **both naming conventions** automatically. No more 422 errors! 🎉

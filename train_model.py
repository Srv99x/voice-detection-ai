import os
import glob
import numpy as np
import librosa
import torch
import joblib
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from transformers import Wav2Vec2FeatureExtractor, Wav2Vec2Model

# --- 1. CONFIGURATION ---
MODEL_NAME = "facebook/wav2vec2-large-xlsr-53" # Multilingual Model
BATCH_SIZE = 1 # Keep low for safety on local machines

# Check for GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🚀 Training on: {device.upper()}")

print(f"Loading {MODEL_NAME}...")
# Note: FeatureExtractor is the correct class for Wav2Vec2 audio processing
processor = Wav2Vec2FeatureExtractor.from_pretrained(MODEL_NAME)
model = Wav2Vec2Model.from_pretrained(MODEL_NAME, use_safetensors=True).to(device)

def extract_features(audio_array):
    """Extracts features from an audio array using the GPU."""
    try:
        # Prepare input for Model
        inputs = processor(audio_array, sampling_rate=16000, return_tensors="pt", padding=True).to(device)
        
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Calculate the average voice fingerprint (Size 1024)
        last_hidden_states = outputs.last_hidden_state
        feature_vector = torch.mean(last_hidden_states, dim=1).squeeze().cpu().numpy()
        return feature_vector
    except Exception as e:
        print(f"⚠️ Error extracting features: {e}")
        return None

def load_and_augment(file_path):
    """Generator: Yields Original + 3 Augmented versions of the audio."""
    try:
        audio, sr = librosa.load(file_path, sr=16000)
    except Exception as e:
        print(f"Skipping {file_path}: Load Error ({e})")
        return

    # Skip if too short (avoids crash)
    if librosa.get_duration(y=audio, sr=sr) < 0.5:
        return
    
    # 1. Original
    yield audio
    
    # 2. Noise Injection
    noise = np.random.randn(len(audio))
    yield audio + 0.005 * noise
    
    # 3. Pitch Shift (Up)
    yield librosa.effects.pitch_shift(audio, sr=sr, n_steps=2.0)
    
    # 4. Pitch Shift (Down)
    yield librosa.effects.pitch_shift(audio, sr=sr, n_steps=-2.0)

# --- 2. INTELLIGENT FILE FINDER ---
def get_files(folder):
    """Recursively finds .mp3, .wav, .m4a files in all subfolders."""
    files = []
    # Using glob with recursive=True to find files in dataset/ai/Tamil, dataset/ai/Hindi, etc.
    files.extend(glob.glob(f"{folder}/**/*.mp3", recursive=True))
    files.extend(glob.glob(f"{folder}/**/*.wav", recursive=True))
    files.extend(glob.glob(f"{folder}/**/*.m4a", recursive=True))
    return files

X = []
y = []

# --- 3. PROCESSING DATA ---
print("\nStep 2: Processing Real Audio...")
real_files = get_files("dataset/real")
print(f"   Found {len(real_files)} Real files (Recursive).")

for file in real_files:
    # We loop through the generator to get original + augmented versions
    for augmented_audio in load_and_augment(file):
        feat = extract_features(augmented_audio)
        if feat is not None:
            X.append(feat)
            y.append(0) # 0 = HUMAN

print("\nStep 3: Processing AI Audio...")
ai_files = get_files("dataset/ai")
print(f"   Found {len(ai_files)} AI files (Recursive).")

for file in ai_files:
    for augmented_audio in load_and_augment(file):
        feat = extract_features(augmented_audio)
        if feat is not None:
            X.append(feat)
            y.append(1) # 1 = AI

# --- 4. TRAIN & SAVE ---
if len(X) == 0:
    print("\n[ERROR] No audio files processed! Check your 'dataset' folder structure.")
else:
    print(f"\nStep 4: Training Neural Network on {len(X)} samples...")
    
    # 1. Scale the Data (Crucial for Neural Networks)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 2. Train the MLP (Neural Network)
    clf = MLPClassifier(hidden_layer_sizes=(128, 64), max_iter=500, random_state=42)
    clf.fit(X_scaled, y)

    # 3. Save Model AND Scaler
    joblib.dump(clf, "hackathon_model.pkl")
    joblib.dump(scaler, "model_scaler.pkl")
    
    print("\n✅ SUCCESS! Multilingual Neural Network saved.")
    print("Files created: 'hackathon_model.pkl' and 'model_scaler.pkl'")
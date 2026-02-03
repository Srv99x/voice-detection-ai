import os
import glob
import numpy as np
import librosa
import torch
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestClassifier
from transformers import Wav2Vec2FeatureExtractor, Wav2Vec2Model

# --- 1. Setup Models ---
print("Step 1: Loading AI Model... (This will download ~1GB the first time)")
processor = Wav2Vec2FeatureExtractor.from_pretrained("facebook/wav2vec2-large-xlsr-53")
model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-large-xlsr-53")

from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier

def extract_features(audio_array):
    """Extracts features from an audio array."""
    # Process with Wav2Vec2
    inputs = processor(audio_array, sampling_rate=16000, return_tensors="pt", padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Calculate the average voice feature
    last_hidden_states = outputs.last_hidden_state
    feature_vector = torch.mean(last_hidden_states, dim=1).squeeze().numpy()
    return feature_vector

def load_and_augment(file_path):
    """Loads a file and returns original + augmented data arrays."""
    audio, sr = librosa.load(file_path, sr=16000)
    
    # 1. Original
    yield audio
    
    # 2. Noise Injection (simulate bad mic)
    noise = np.random.randn(len(audio))
    yield audio + 0.005 * noise
    
    # 3. Pitch Shift (simulate different speakers)
    # n_steps= float: fraction of a semitone (e.g. 2.0, -2.0)
    yield librosa.effects.pitch_shift(audio, sr=sr, n_steps=2.0)
    yield librosa.effects.pitch_shift(audio, sr=sr, n_steps=-2.0)

# --- 2. Load Data ---
X = [] # Features
y = [] # Labels (0 = Real, 1 = AI)

# Helper to find mp3 AND m4a files (Recursive for language subfolders)
def get_files(folder):
    # Use distinct globs for each extension to be safe (glob does not support OR syntax natively in all versions)
    # We use recursive=True and ** to look inside subfolders (e.g. dataset/real/tamil/)
    files = []
    files.extend(glob.glob(f"{folder}/**/*.mp3", recursive=True))
    files.extend(glob.glob(f"{folder}/**/*.wav", recursive=True))
    files.extend(glob.glob(f"{folder}/**/*.m4a", recursive=True))
    return files

print("\nStep 2: Processing Real Audio (with Augmentation)...")
real_files = get_files("dataset/real")
for file in real_files:
    print(f"  - Loading {file}...")
    try:
        for augmented_audio in load_and_augment(file):
            feat = extract_features(augmented_audio)
            X.append(feat)
            y.append(0) # 0 = Human
    except Exception as e:
        print(f"    [!] Error loading {file}: {e}")

print("\nStep 3: Processing AI Audio (with Augmentation)...")
ai_files = get_files("dataset/ai")
for file in ai_files:
    print(f"  - Loading {file}...")
    try:
        for augmented_audio in load_and_augment(file):
            feat = extract_features(augmented_audio)
            X.append(feat)
            y.append(1) # 1 = AI
    except Exception as e:
        print(f"    [!] Error loading {file}: {e}")

# --- 3. Train & Save ---
if len(X) == 0:
    print("\n[ERROR] No files were loaded. Check your folders or install FFmpeg.")
else:
    print(f"\nStep 4: Training Neural Network on {len(X)} samples (Augmented)...")
    
    # Scale Features (Crucial for Neural Networks)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Use MLP (Multi-Layer Perceptron) for better accuracy
    clf = MLPClassifier(hidden_layer_sizes=(128, 64), max_iter=500, random_state=42)
    clf.fit(X_scaled, y)

    # Save the brain AND the scaler
    joblib.dump(clf, "hackathon_model.pkl")
    joblib.dump(scaler, "model_scaler.pkl")
    print("\nSUCCESS! Model saved as 'hackathon_model.pkl' and Scaler as 'model_scaler.pkl'.")
    print("Don't forget to restart your API!")
# src/feature_extraction.py
import numpy as np
import librosa


def extract_features(audio_data, sr=22050):
    """Extract audio features from a byte stream."""
    # Convert byte data to a numpy array
    audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)

    # Calculate the average amplitude
    amplitude = np.abs(audio_np).mean()

    # Compute a mel-spectrogram
    mel_spec = librosa.feature.melspectrogram(audio_np, sr=sr, n_mels=64)
    mel_db = librosa.power_to_db(mel_spec, ref=np.max)

    # Compute spectral centroid (average over time)
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(S=mel_spec, sr=sr))

    return {
        "amplitude": amplitude,
        "spectral_centroid": spectral_centroid,
        # Optionally: include mel_db or other features
    }

# src/feature_extraction.py
import numpy as np
import librosa


def extract_features(audio_data, sr=22050):
    """
    Extract features from the audio byte data.

    Returns:
      A dictionary with 'amplitude' and 'spectral_centroid'.
    """
    audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
    amplitude = np.abs(audio_np).mean()

    # Compute a mel-spectrogram (used here to calculate the spectral centroid)
    mel_spec = librosa.feature.melspectrogram(audio_np, sr=sr, n_mels=64)
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(S=mel_spec, sr=sr))

    return {"amplitude": amplitude, "spectral_centroid": spectral_centroid}

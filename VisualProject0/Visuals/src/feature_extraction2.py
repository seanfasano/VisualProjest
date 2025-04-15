import numpy as np
import librosa


def extract_features(audio_data, sr=22050):
    """
    Extract features from the audio byte data after applying RMS normalization.

    The function performs the following steps:
      1. Converts 16-bit integer audio data to float values in [-1, 1].
      2. Applies RMS normalization so that the overall energy becomes consistent
         across tracks mastered at different volumes.
      3. Computes the mean absolute amplitude.
      4. Computes a mel-spectrogram and its spectral centroid (averaged over time).
      5. Averages the mel-spectrogram across the time axis to obtain a 64-element vector,
         and then splits this vector into 8 bands (with 8 elements each),
         computing the average energy in each band.

    Returns a dictionary with the keys:
      - "amplitude": the mean absolute amplitude (after normalization).
      - "spectral_centroid": the average spectral centroid.
      - "frequency_bands": a list of 8 average energy values, one per frequency band.
    """
    # Convert audio data (16-bit) to float values in the range [-1, 1]
    audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

    # RMS normalization: scale the audio so that its RMS equals a target value.
    rms = np.sqrt(np.mean(audio_np ** 2))
    target_rms = 0.1  # You can adjust this target based on your preference
    audio_np = audio_np * (target_rms / (rms + 1e-6))

    # Compute overall amplitude as the mean absolute value of the normalized audio.
    amplitude = np.abs(audio_np).mean()

    # Compute a mel-spectrogram with 64 mel bands
    mel_spec = librosa.feature.melspectrogram(y=audio_np, sr=sr, n_mels=64)

    # Compute the spectral centroid (averaged over time) using the mel-spectrogram.
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(S=mel_spec, sr=sr))

    # Average the mel-spectrogram along the time axis to obtain a 64-element energy vector.
    mel_spec_avg = np.mean(mel_spec, axis=1)  # shape: (64,)

    # Split the 64-element vector into 8 equal frequency bands (each with 8 mel bands)
    bands = np.array_split(mel_spec_avg, 8)
    frequency_bands = [np.mean(band) for band in bands]

    return {
        "amplitude": amplitude,
        "spectral_centroid": spectral_centroid,
        "frequency_bands": frequency_bands
    }


if __name__ == "__main__":
    # For testing purposes, you can load a file or simulate audio_data.
    # Here we assume 'audio_data' contains your 16-bit PCM byte data.
    # Example usage:
    # with open("example_audio.raw", "rb") as f:
    #     audio_data = f.read()
    # features = extract_features(audio_data)
    # print(features)
    pass
# src/mapping.py
import numpy as np

def map_amplitude_to_brightness(amplitude, min_amp=0, max_amp=3000):
    """Map amplitude to a brightness scale (0-100)."""
    brightness = np.clip((amplitude - min_amp) / (max_amp - min_amp) * 100, 0, 100)
    return brightness

def map_centroid_to_hue(centroid, min_centroid=2000, max_centroid=8000):
    """Map spectral centroid to a hue (0-180 in OpenCV's HSV space)."""
    hue = np.clip((centroid - min_centroid) / (max_centroid - min_centroid) * 180, 0, 180)
    return hue

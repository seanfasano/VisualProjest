# src/audio_capture.py
import pyaudio

# Configuration parameters for audio capture
CHUNK = 1024        # Samples per frame
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1        # Mono channel
RATE = 22050        # Sampling rate (Hz)

def get_audio_stream():
    """Initialize and return a PyAudio stream."""
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    return stream, p

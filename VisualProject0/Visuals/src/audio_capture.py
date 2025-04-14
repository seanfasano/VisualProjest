# src/audio_capture.py
import pyaudio

# Audio stream parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 22050

def get_audio_stream():
    """Initializes and returns a PyAudio stream along with the PyAudio instance."""
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )
    return stream, p

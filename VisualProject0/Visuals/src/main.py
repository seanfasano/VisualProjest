# src/main.py
import time
import cv2
import numpy as np
from audio_capture import get_audio_stream, CHUNK, RATE
from feature_extraction import extract_features
from mapping import generate_prompt
from generator import load_diffusion_model, generate_image

def record_audio(stream, duration_sec=5):
    """Records audio from the stream for the specified duration in seconds."""
    frames = []
    num_frames = int(RATE / CHUNK * duration_sec)
    for _ in range(num_frames):
        audio_data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(audio_data)
    return b"".join(frames)

def main():
    # Load the diffusion model only once
    print("Loading diffusion model (this may take a few minutes)...")
    pipe = load_diffusion_model()
    print("Diffusion model loaded.")

    # Set up audio stream
    stream, p = get_audio_stream()
    print("Audio stream started.")

    try:
        while True:
            # Record audio for a fixed duration
            print("Recording audio for 10 seconds...")
            audio_data = record_audio(stream, duration_sec=5)
            print("Audio recorded. Extracting features...")

            features = extract_features(audio_data, sr=RATE)
            print("Extracted features:", features)

            # Convert audio features into a text prompt
            prompt = generate_prompt(features)
            print("Generated prompt:", prompt)

            # Generate an image from the prompt
            print("Generating image, please wait...")
            image = generate_image(pipe, prompt)

            # Convert the PIL image to an OpenCV format and display it
            image_cv = np.array(image)
            image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)
            cv2.imshow("Generated Visuals", image_cv)

            print("Press 'q' to quit or any other key to generate another image.")
            key = cv2.waitKey(0)
            if key & 0xFF == ord("q"):
                break
    except KeyboardInterrupt:
        pass
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

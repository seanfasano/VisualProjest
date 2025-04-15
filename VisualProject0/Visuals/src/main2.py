# src/main.py
import time
import cv2
import numpy as np
from audio_capture import get_audio_stream, CHUNK, RATE
from feature_extraction2 import extract_features
from mapping3 import generate_prompt
from generator import load_diffusion_model, generate_image

def record_audio_frames(stream, duration_sec):
    """
    Records audio from the stream for the specified duration in seconds,
    and returns the list of recorded frames.
    """
    frames = []
    num_frames = int(RATE / CHUNK * duration_sec)
    for _ in range(num_frames):
        # Read a chunk from the stream (exception suppressed on overflow)
        audio_data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(audio_data)
    return frames

def main():
    # Load the diffusion model (this may take a few minutes)
    print("Loading diffusion model (this may take a few minutes)...")
    pipe = load_diffusion_model()
    print("Diffusion model loaded.")

    # Set up audio stream
    stream, p = get_audio_stream()
    print("Audio stream started.")

    # Record audio for a total of 15 seconds at once
    total_duration = 15  # seconds
    print(f"Recording audio for {total_duration} seconds...")
    frames = record_audio_frames(stream, total_duration)
    print("Audio recording complete.")

    # Determine number of frames for 5 and 10 seconds
    num_frames_5 = int(RATE / CHUNK * 5)
    num_frames_10 = int(RATE / CHUNK * 10)
    # For 15 seconds, use all frames
    num_frames_15 = len(frames)

    # Create audio segments by concatenating the appropriate slices of frames
    audio_data_5  = b"".join(frames[:num_frames_5])
    audio_data_10 = b"".join(frames[:num_frames_10])
    audio_data_15 = b"".join(frames[:num_frames_15])

    # Prepare the durations and corresponding audio data
    durations = [5, 10, 15]
    audio_segments = [audio_data_5, audio_data_10, audio_data_15]
    images = []

    # Process each audio segment to extract features, generate a prompt, and produce an image.
    for d, audio_data in zip(durations, audio_segments):
        print(f"Processing audio for the first {d} seconds...")
        features = extract_features(audio_data, sr=RATE)
        print("Extracted features:", features)
        prompt = generate_prompt(features)
        print("Generated prompt:", prompt)
        print("Generating image, please wait...")
        image = generate_image(pipe, prompt)
        # Convert the PIL image to a NumPy array
        images.append(np.array(image))

    # Convert from RGB (PIL format) to BGR (OpenCV format)
    images_cv = [cv2.cvtColor(img, cv2.COLOR_RGB2BGR) for img in images]

    # Combine images side by side; ensure they have the same height
    composite = np.hstack(images_cv)

    # Display the composite image
    cv2.imshow("Generated Visuals (5s, 10s, 15s)", composite)
    print("Displaying combined image. Press any key to exit.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Cleanup: stop the audio stream and terminate PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    main()
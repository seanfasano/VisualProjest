# src/main.py
import cv2
import time
from audio_capture import get_audio_stream, CHUNK, RATE
from feature_extraction import extract_features
from mapping import map_amplitude_to_brightness, map_centroid_to_hue
from visual_mods import adjust_brightness, adjust_hue


def main():
    # Load the base image from the assets
    base_image = cv2.imread('../assets/images/base_image.jpg')
    base_image = cv2.resize(base_image, (640, 480))

    # Set up the audio stream
    stream, p = get_audio_stream()

    print("Starting audio-reactive visual display. Press 'q' to quit.")
    try:
        while True:
            # Read a chunk of audio input
            audio_data = stream.read(CHUNK, exception_on_overflow=False)

            # Extract relevant audio features
            features = extract_features(audio_data, sr=RATE)

            # Map features to visual transformation parameters
            brightness_param = map_amplitude_to_brightness(features["amplitude"])
            hue_param = map_centroid_to_hue(features["spectral_centroid"])

            # Adjust base image based on the mapped parameters
            mod_image = adjust_brightness(base_image, int(brightness_param - 50))
            mod_image = adjust_hue(mod_image, hue_param)

            # Display the modified image
            cv2.imshow('Audio-Reactive Visual', mod_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Brief delay to match processing speed
            time.sleep(0.01)
    except KeyboardInterrupt:
        pass
    finally:
        # Clean-up: stop audio stream and close window
        stream.stop_stream()
        stream.close()
        p.terminate()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

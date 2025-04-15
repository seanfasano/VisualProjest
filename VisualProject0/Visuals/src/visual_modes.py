
# src/visual_mods.py
import cv2
import numpy as np

def adjust_brightness(image, brightness_value):
    """Modify brightness by manipulating the V channel in HSV space."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    # Adjust brightness (clipping between 0 and 255)
    v = np.clip(v + brightness_value, 0, 255).astype(np.uint8)
    final_hsv = cv2.merge((h, s, v))
    image_bright = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return image_bright

def adjust_hue(image, hue_shift):
    """Modify the hue of the image by shifting the H channel."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    h = (h.astype(np.int32) + int(hue_shift)) % 180
    h = h.astype(np.uint8)
    final_hsv = cv2.merge((h, s, v))
    image_hue = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return image_hue

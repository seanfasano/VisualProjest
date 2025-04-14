# src/mapping.py

def generate_prompt(features):
    """
    Generates a textual prompt based on the provided audio features.

    Uses amplitude to decide the mood and spectral_centroid to determine the style.
    """
    amplitude = features.get("amplitude", 0)
    spectral_centroid = features.get("spectral_centroid", 0)

    # Determine mood based on amplitude
    if amplitude > 1500:
        mood = "energetic and vibrant"
    else:
        mood = "calm and soothing"

    # Determine style based on spectral centroid
    if spectral_centroid > 3000:
        style = "modern abstract art"
    else:
        style = "surreal dreamlike scenery"

    prompt = f"A {mood} depiction of {style}"
    return prompt

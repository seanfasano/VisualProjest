import random

def generate_prompt(features):
    """
    Generates a textual prompt based on audio features.

    Expects the following keys in `features`:
      - amplitude: overall amplitude of the signal.
      - spectral_centroid: a measure of the brightness of the sound.
      - frequency_bands: a list of 8 amplitude values, one for each frequency band.

    This function uses:
      - amplitude to decide the overall mood,
      - spectral_centroid to determine a general artistic style,
      - and the amplitude levels in different frequency bands to describe the frequency characteristics.
    """
    amplitude = features.get("amplitude", 0)
    spectral_centroid = features.get("spectral_centroid", 0)
    frequency_bands = features.get("frequency_bands", [0] * 8)

    # Determine mood based on amplitude:
    if amplitude > 1500:
        # High amplitude: energetic and vibrant
        mood = "energetic and vibrant"
    elif amplitude < 800:
        # Low amplitude: adopt a darker mood that still carries a hint of hope
        mood = "somber and introspective, yet with a glimmer of hope"
    else:
        # Moderate amplitude: balanced with a subtle note of optimism amid calmness
        mood = "balanced and serene with subtle optimism"

    # Determine style based on spectral centroid:
    if spectral_centroid > 3000:
        style = "modern abstract art"
    else:
        style = "surreal, dreamlike scenery"

    # Compute average amplitude for frequency subranges
    # We divide the eight bands into groups, for example:
    low_energy = sum(frequency_bands[0:2]) / 2     # bands 0-1 as low frequencies
    mid_energy = sum(frequency_bands[2:4]) / 2     # bands 2-3 as mid frequencies
    high_energy = sum(frequency_bands[6:8]) / 2    # bands 6-7 as high frequencies

    # Determine a frequency description based on which range is dominant:
    if low_energy >= mid_energy and low_energy >= high_energy:
        freq_desc = "bass-heavy and deep"
    elif high_energy >= mid_energy and high_energy >= low_energy:
        freq_desc = "trebly, sharp, and modern"
    else:
        freq_desc = "balanced with a warm midrange"

    # Additional adjective for a darker, sketch-like aesthetic with hints of brightness:
    additional_adjective = ""
    if amplitude < 800:
        additional_adjective = " with a dark, sketch-like aesthetic and subtle hints of brightness"

    prompt = f"A {mood} depiction of {style}{additional_adjective}, featuring {freq_desc} frequency characteristics."
    return prompt

# Example usage:
features_example = {
    "amplitude": 700,
    "spectral_centroid": 2500,
    "frequency_bands": [120, 110, 90, 85, 70, 65, 150, 160]
}
print(generate_prompt(features_example))
import random
import hashlib

def generate_prompt(features, image_index=1, n_prompts=1):
    """
    Generates one or more textual prompts based on audio features and an image index to vary style emphasis.

    Expects the following keys in `features`:
      - amplitude: overall amplitude (loudness) of the track.
      - frequency_bands: a list of 8 amplitude values for:
         [sub_bass, bass, low_mid, mid, high_mid, presence, brilliance, air]

    image_index:
      * 1 or 2 => darker, more realistic abstraction with shadowy, foggy references
      * 3 => a somewhat more muted, minimal approach

    Deterministic seeding is used so identical features yield the same prompts unless multiple variations (n_prompts>1).

    Returns:
      A single prompt if n_prompts==1, or a list of prompts otherwise.
    """
    # Create a deterministic seed from the features
    features_str = str(features)
    base_seed = int(hashlib.md5(features_str.encode()).hexdigest(), 16)

    prompts = []
    for i in range(n_prompts):
        # Slightly different seed for each variation
        random_seed = base_seed + i
        random.seed(random_seed)

        amplitude = features.get("amplitude", 0)
        freq_bands = features.get("frequency_bands", [0]*8)
        sub_bass, bass, low_mid, mid, high_mid, presence, brilliance, air = freq_bands

        # --- 1) Mood: amplitude-based ---
        if amplitude > 1500:
            mood_options = [
                "an intense, shadow-laced energy with a foggy hush",
                "vibrant yet draped in swirling mists and brooding undercurrents",
                "highly charged with dark forest echoes and dense atmospheric shadows"
            ]
        elif amplitude < 800:
            mood_options = [
                "a deeply subdued atmosphere steeped in grey fog and drifting silhouettes",
                "quietly ominous, blanketed by drifting shadows in a dark woodland realm",
                "low, persistent gloom with gentle hints of swirling mist"
            ]
        else:
            mood_options = [
                "a balanced but subdued space, veiled by soft fog and shadow",
                "a calm, mid-level intensity with creeping hazes and understated darkness",
                "an even-tempered gloom, lightly colored by forest-like elements"
            ]
        mood = random.choice(mood_options)

        # --- 2) Style Variation: image_index ---
        # Emphasize darker forests, fog, and subtle realism for 1 & 2
        # More muted and minimal for 3
        darker_styles = [
            "shadowy, abstract landscapes merging earthy textures with ghostly tree lines",
            "fog-laden forms hinting at hidden branches and damp undergrowth",
            "moody, half-real silhouettes of gnarled trunks and swirling mist"
        ]
        minimal_styles = [
            "gentle shapes dissolving into near-monochrome fog",
            "soft, barely outlined textures reminiscent of distant woodland silhouettes",
            "delicate, almost featureless gradients fading into a hazy gloom"
        ]
        if image_index == 3:
            style = random.choice(minimal_styles)
        else:
            style = random.choice(darker_styles)

        # --- 3) Frequency Influence (no direct references to "low/mid/high") ---
        low_avg = (sub_bass + bass) / 2
        mid_avg = (low_mid + mid) / 2
        high_avg = (high_mid + presence + brilliance + air) / 4

        if low_avg > mid_avg and low_avg > high_avg:
            freq_mod = "grounded by a heavy, enveloping undertone"
        elif mid_avg > low_avg and mid_avg > high_avg:
            freq_mod = "holding a warm, enveloping density"
        elif high_avg > low_avg and high_avg > mid_avg:
            freq_mod = "touched by faintly drifting upper wisps"
        else:
            freq_mod = "balancing its shadows with subtle tonal variety"

        # --- 4) Combine everything into the final prompt ---
        prompt = (
            f"A depiction of {mood}, realized through {style}, {freq_mod}."
        )
        prompts.append(prompt)

    return prompts[0] if n_prompts == 1 else prompts

# Example usage:
if __name__ == "__main__":
    # Example features for demonstration
    features_example = {
        "amplitude": 700,
        "frequency_bands": [15.2, 27.8, 12.0, 20.5, 10.0, 5.4, 2.2, 1.9]
    }
    single_prompt = generate_prompt(features_example, image_index=1, n_prompts=1)
    print("Single Prompt:")
    print(single_prompt)
    print()

    multiple_prompts = generate_prompt(features_example, image_index=1, n_prompts=3)
    print("Multiple Prompts:")
    for idx, p in enumerate(multiple_prompts, start=1):
        print(f"{idx}. {p}")
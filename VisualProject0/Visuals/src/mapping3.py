import random
import hashlib


def select_aesthetic_path(features):
    """
    Selects an aesthetic path based on the audio features.

    Expects in features:
      - amplitude: overall loudness.
      - frequency_bands: list of 8 amplitude values, in the order:
         [sub_bass, bass, low_mid, mid, high_mid, presence, brilliance, air]

    Returns:
      A string representing one of the aesthetic paths.

    The candidate paths are:
      "tribal", "natural", "industrial", "minimal_abstract",
      "hybrid_organic_industrial", "dark_surreal", "primal_wilderness",
      "cosmic_natural", "apocalyptic_vision", "biomorphic_abstraction",
      "mystical_ethereal"
    """
    # Get features and frequency averages.
    amplitude = features.get("amplitude", 0)
    freq_bands = features.get("frequency_bands", [0] * 8)
    # For clarity, assume:
    #   band0: sub_bass, band1: bass, band2: low_mid, band3: mid,
    #   bands 4-7: high_mid, presence, brilliance, air.
    low_avg = (freq_bands[0] + freq_bands[1]) / 2
    mid_avg = (freq_bands[2] + freq_bands[3]) / 2
    high_avg = (sum(freq_bands[4:8])) / 4

    # Initialize scores for each candidate path.
    scores = {
        "tribal": 0,
        "natural": 0,
        "industrial": 0,
        "minimal_abstract": 0,
        "hybrid_organic_industrial": 0,
        "dark_surreal": 0,
        "primal_wilderness": 0,
        "cosmic_natural": 0,
        "apocalyptic_vision": 0,
        "biomorphic_abstraction": 0,
        "mystical_ethereal": 0,
    }

    # --- Amplitude-Based Adjustments ---
    # Lower amplitude (e.g., <600) suggests calmer, more subdued aesthetics.
    if amplitude < 600:
        scores["primal_wilderness"] += 2
        scores["mystical_ethereal"] += 2
        scores["natural"] += 1
        scores["tribal"] += 1
    # Moderate amplitude (600 to 1200) might favor natural or biomorphic abstract aesthetics.
    elif amplitude < 1200:
        scores["natural"] += 2
        scores["biomorphic_abstraction"] += 2
        scores["minimal_abstract"] += 1
    # High amplitude (>1200) might push toward harsher, darker, industrial or dark surreal aesthetics.
    else:
        scores["industrial"] += 2
        scores["dark_surreal"] += 2
        scores["hybrid_organic_industrial"] += 1

    # --- Frequency-Based Adjustments ---
    # If low frequencies are dominant, that can lean toward "primal_wilderness" or "tribal"
    if low_avg > mid_avg and low_avg > high_avg:
        scores["primal_wilderness"] += 2
        scores["tribal"] += 1
    # If mid frequencies are dominant, a natural and organic sound might be inferred.
    elif mid_avg > low_avg and mid_avg > high_avg:
        scores["natural"] += 2
        scores["biomorphic_abstraction"] += 1
    # If high frequencies dominate, that might suggest a more ethereal or minimal look.
    elif high_avg > low_avg and high_avg > mid_avg:
        scores["mystical_ethereal"] += 2
        scores["minimal_abstract"] += 1

    # If the frequency bands are more balanced, then a hybrid or dark surreal approach might work well.
    if abs(low_avg - mid_avg) < 5 and abs(mid_avg - high_avg) < 5:
        scores["hybrid_organic_industrial"] += 1
        scores["dark_surreal"] += 1

    # --- Final Selection ---
    # Pick the candidate with the highest cumulative score.
    selected_path = max(scores, key=scores.get)
    return selected_path


def generate_prompt(features, path_type=None, image_index=1, n_prompts=1):
    """
    Generates one or more abstract textual prompts based on audio features.

    If 'path_type' is not provided, it is automatically selected based on audio features
    (i.e., the sound texture), using overall amplitude and the balance between different frequency bands.

    Expects in `features`:
      - amplitude: overall loudness.
      - frequency_bands: list of 8 amplitude values in the order:
            [sub_bass, bass, low_mid, mid, high_mid, presence, brilliance, air]

    The function uses a deterministic seed so that the same features yield the same prompts,
    unless multiple variations are requested.

    The `image_index` parameter (1, 2, or 3) slightly adjusts the style.

    Returns:
      A single prompt string (if n_prompts==1) or a list of prompt strings.
    """
    # Automatically select an aesthetic path if none is provided.
    if path_type not in {
        "tribal", "natural", "industrial", "minimal_abstract",
        "hybrid_organic_industrial", "dark_surreal", "primal_wilderness",
        "cosmic_natural", "apocalyptic_vision", "biomorphic_abstraction",
        "mystical_ethereal"
    }:
        path_type = select_aesthetic_path(features)

    # Define aesthetic options for each path.
    aesthetic_paths = {
        "tribal": {
            "mood": [
                "a raw spirit evoking ancient, carved symbols",
                "a bold, primitive energy with weathered motifs",
                "an earthy pulse reminiscent of timeworn totems"
            ],
            "style": [
                "bold, etched forms with rugged textures",
                "primitive patterns and rough, organic outlines",
                "abstract tribal motifs with a raw, artisanal feel"
            ]
        },
        "natural": {
            "mood": [
                "a deep, shadowed ambiance hinting at dark forests",
                "a misty, organic realm with muted natural hues",
                "an interplay of light and darkness found in wild landscapes"
            ],
            "style": [
                "flowing organic shapes and subtle natural textures",
                "a softly rendered abstraction of forested vistas",
                "forms that evoke shadowed foliage and quiet natural beauty"
            ]
        },
        "industrial": {
            "mood": [
                "a harsh, mechanical energy in a stark urban decay",
                "a cold, rugged mood with imposing, metallic undertones",
                "a gritty vibe where concrete and steel resonate"
            ],
            "style": [
                "fragmented geometric forms with rough, metal textures",
                "industrial structures with a raw, hard-edged presence",
                "abstract urban decay with a futuristic, mechanical edge"
            ]
        },
        "minimal_abstract": {
            "mood": [
                "a spare, subtle calm in a world of soft shapes",
                "an understated, quiet ambiance that focuses on simplicity",
                "a gentle, muted presence with an elegant minimalism"
            ],
            "style": [
                "delicate lines and minimal forms with restrained contrast",
                "sparse abstractions that emphasize negative space",
                "a refined, almost monochromatic interplay of form and void"
            ]
        },
        "hybrid_organic_industrial": {
            "mood": [
                "a dynamic tension where urban decay meets organic resilience",
                "a layered expression of mechanical grit softened by nature",
                "an interplay of raw industrial forms and reclaimed natural textures"
            ],
            "style": [
                "rusted metals interwoven with natural, organic curves",
                "a striking synthesis of urban structures and wild, earthy patterns",
                "abstract forms where concrete rigidity blends with natural fluidity"
            ]
        },
        "dark_surreal": {
            "mood": [
                "a brooding, uncanny atmosphere of deep shadows",
                "an enigmatic gloom where reality blurs into dream",
                "a mysterious, almost dystopian quietude"
            ],
            "style": [
                "ghostly silhouettes and distorted contours in low-key tones",
                "abstract, surreal forms with a stark, somber touch",
                "a collage of shadow and minimalistic detail evoking dark dreams"
            ]
        },
        "primal_wilderness": {
            "mood": [
                "a wild, untamed force echoing the raw pulse of nature",
                "an elemental, rugged spirit drawn from ancient woods",
                "a visceral energy that calls upon the primal earth"
            ],
            "style": [
                "rough, organic textures with bold, earthy outlines",
                "abstract depictions of dense, ancient forests",
                "a raw portrayal of nature’s unbridled wilderness"
            ]
        },
        "cosmic_natural": {
            "mood": [
                "a mysterious blend of celestial wonder and natural calm",
                "an enigmatic aura merging starlight with the earth’s depth",
                "a subtle interplay of cosmic and organic forces"
            ],
            "style": [
                "delicate, astral shapes that flow into shadowed natural forms",
                "abstract contours that evoke both nebulae and deep forests",
                "a soft fusion of cosmic light and rugged nature"
            ]
        },
        "apocalyptic_vision": {
            "mood": [
                "a stark, dystopian energy charged with desolation",
                "a heavy, brooding forewarning of collapse and decay",
                "a raw, ominous atmosphere of shattering reality"
            ],
            "style": [
                "fragmented, harsh structures with a sense of ruin",
                "a grim abstraction of decaying urban landscapes",
                "rough, angular forms that evoke industrial collapse"
            ]
        },
        "biomorphic_abstraction": {
            "mood": [
                "a fluid, evolving energy that mimics the forms of life",
                "an organic, pulsing rhythm reminiscent of living matter",
                "a subtle dance of shapes that hint at nature’s hidden geometry"
            ],
            "style": [
                "soft, curving forms that echo cellular structures",
                "abstract, biomorphic lines that flow organically",
                "delicate shapes suggesting the secret patterns of growth"
            ]
        },
        "mystical_ethereal": {
            "mood": [
                "a dreamlike, intangible aura of quiet mystery",
                "an ethereal calm imbued with subtle spiritual nuance",
                "a softly luminous ambiance that whispers of ancient secrets"
            ],
            "style": [
                "translucent, fading forms that drift in gentle space",
                "minimal, abstract silhouettes suffused with delicate light",
                "an understated abstraction that evokes a mystical quietude"
            ]
        }
    }

    # Create a deterministic seed from the features.
    features_str = str(features)
    base_seed = int(hashlib.md5(features_str.encode()).hexdigest(), 16)

    prompts = []
    for i in range(n_prompts):
        # Use varying seeds for alternative prompts.
        random_seed = base_seed + i
        random.seed(random_seed)

        amplitude = features.get("amplitude", 0)
        freq_bands = features.get("frequency_bands", [0] * 8)
        sub_bass, bass, low_mid, mid, high_mid, presence, brilliance, air = freq_bands
        low_avg = (sub_bass + bass) / 2
        mid_avg = (low_mid + mid) / 2
        high_avg = (high_mid + presence + brilliance + air) / 4

        # Determine a subtle frequency-based modifier.
        if low_avg > mid_avg and low_avg > high_avg:
            freq_mod = "imbued with a deep, resonant undertone"
        elif mid_avg > low_avg and mid_avg > high_avg:
            freq_mod = "carrying an organic, earthy depth"
        elif high_avg > low_avg and high_avg > mid_avg:
            freq_mod = "touched by a delicate, fading light"
        else:
            freq_mod = "in a harmonious, subtle blend"

        # Select mood and style from the chosen path.
        path = aesthetic_paths[path_type]
        mood = random.choice(path["mood"])
        style = random.choice(path["style"])

        # Refine mood based on amplitude.
        if amplitude > 1500:
            mood += ", pulsating with fierce energy"
        elif amplitude < 800:
            mood += ", quiet with a hint of somber introspection"
        else:
            mood += ", modest yet evocative"

        # Adjust style for image_index==3 to yield a more minimal feel.
        if image_index == 3:
            style += " in a muted, sparse palette"

        # Combine into the final prompt.
        prompt = f"A depiction of {mood}, rendered through {style}, {freq_mod}."
        prompts.append(prompt)

    return prompts[0] if n_prompts == 1 else prompts


# Example usage:
if __name__ == "__main__":
    features_example = {
        "amplitude": 700,
        # Frequency bands: [sub_bass, bass, low_mid, mid, high_mid, presence, brilliance, air]
        "frequency_bands": [20.2, 18.4, 8.0, 7.5, 14.0, 6.1, 3.2, 2.0]
    }
    # Generate a single prompt using a chosen path (e.g., "tribal")
    single_prompt = generate_prompt(features_example, path_type="tribal", image_index=1, n_prompts=1)
    print("Single Prompt:")
    print(single_prompt)
    print()

    # Generate alternative prompts (let the code select a path based on the sound texture)
    prompt_variations = generate_prompt(features_example, image_index=1, n_prompts=3)
    print("Prompt Variations:")
    for idx, p in enumerate(prompt_variations, start=1):
        print(f"{idx}. {p}")
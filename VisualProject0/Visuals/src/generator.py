# src/generator.py
from diffusers import StableDiffusionPipeline
import torch


import torch

def load_diffusion_model(model_name="CompVis/stable-diffusion-v1-4", device=None):
    # Prioritize Apple MPS if available, then CUDA, then default to CPU.
    if device is None:
        if torch.backends.mps.is_available():
            device = "mps"
        elif torch.cuda.is_available():
            device = "cuda"
        else:
            device = "cpu"
    pipe = StableDiffusionPipeline.from_pretrained(
        model_name,
        torch_dtype=torch.float16 if device in ["cuda", "mps"] else torch.float32
    )
    pipe = pipe.to(device)
    return pipe



def generate_image(pipe, prompt, num_inference_steps=50, guidance_scale=7.5):
    """
    Generates an image given a prompt using the provided diffusion pipeline.

    Args:
      pipe: The Stable Diffusion pipeline instance.
      prompt (str): The textual prompt to guide image generation.
      num_inference_steps (int): How many denoising steps to use.
      guidance_scale (float): Controls the adherence to the prompt.

    Returns:
      A PIL.Image object of the generated image.
    """
    image = pipe(prompt, num_inference_steps=num_inference_steps, guidance_scale=guidance_scale).images[0]
    return image

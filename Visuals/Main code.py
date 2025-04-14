import numpy as np
import pygame
import sounddevice as sd
import math
import librosa  # For beat tracking

# Screen dimensions
WIDTH, HEIGHT = 800, 600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Techno Reactive Visuals (Black & White) - Librosa BPM")
clock = pygame.time.Clock()

# Setup a font to display BPM on screen.
font = pygame.font.SysFont("Arial", 24)


# Particle class representing each moving dot
class Particle:
    def __init__(self, x, y):
        self.pos = np.array([x, y], dtype=float)
        self.vel = np.array([0.0, 0.0], dtype=float)

    def update(self, force, dt):
        self.vel += force * dt
        self.pos += self.vel * dt
        self.vel *= 0.85  # damping


# Create particles and gravity centers
num_particles = 100
num_centers = 10
columns = int(math.ceil(math.sqrt(num_particles)))
rows = int(math.ceil(num_particles / columns))
margin_x = WIDTH * 0.1
margin_y = HEIGHT * 0.1
spacing_x = (WIDTH - 2 * margin_x) / (columns - 1) if columns > 1 else 0
spacing_y = (HEIGHT - 2 * margin_y) / (rows - 1) if rows > 1 else 0

particles = []
for i in range(rows):
    for j in range(columns):
        if len(particles) < num_particles:
            x = margin_x + j * spacing_x
            y = margin_y + i * spacing_y
            particles.append(Particle(x, y))

gravity_centers = [np.array([WIDTH * (i + 0.5) / num_centers, HEIGHT / 2])
                   for i in range(num_centers)]

# Global parameters for audio
BUFFER_SIZE = 1024
current_block = np.zeros(BUFFER_SIZE, dtype=np.float32)
# List to accumulate audio for BPM estimation
accumulated_audio = []


def audio_callback(indata, frames, time, status):
    global current_block, accumulated_audio
    if status:
        print(status)
    # Use the first channel (mono)
    current_block[:] = indata[:, 0]
    # Append a copy of this block to our accumulated audio
    accumulated_audio.append(current_block.copy())


# Use default input device (ensure your system default input is set to BlackHole if you want system output)
stream = sd.InputStream(
    callback=audio_callback,
    channels=1,
    samplerate=44100,
    blocksize=BUFFER_SIZE,
    device=None
)
stream.start()

samplerate = 44100
# We will use a window of 5 seconds for beat tracking
min_duration = 10  # seconds
min_samples = int(min_duration * samplerate)
stable_bpm = 0

# Particle reaction multiplier
speed_multiplier = 7

# For smoothing BPM readings
bpm_history = []
max_history = 100

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- BPM Detection using Librosa ---
    # Concatenate accumulated blocks into one array
    if accumulated_audio:
        full_audio = np.concatenate(accumulated_audio)
        if full_audio.shape[0] >= min_samples:
            # Run beat tracking on the last 5 seconds of audio
            y_segment = full_audio[-min_samples:]
            tempo, beats = librosa.beat.beat_track(y=y_segment, sr=samplerate)
            if tempo > 0:
                bpm_history.append(tempo)
                if len(bpm_history) > max_history:
                    bpm_history.pop(0)
            # Use the average of bpm_history as the stable BPM value,
            # converting it to a float so it formats correctly.
            stable_bpm = float(np.mean(bpm_history)) if bpm_history else 0
            # Remove older data to keep the buffer size bounded (keep only last 5 seconds)
            if full_audio.shape[0] > min_samples:
                full_audio = full_audio[-min_samples:]
                # Re-split into blocks of BUFFER_SIZE samples
                accumulated_audio = [full_audio[i:i + BUFFER_SIZE]
                                     for i in range(0, full_audio.shape[0], BUFFER_SIZE)]

    # --- Audio Processing for Visual Effects (unfiltered) ---
    fft_result = np.fft.fft(current_block)
    fft_magnitude = np.abs(fft_result[:BUFFER_SIZE // 2])
    low_freq_bins = fft_magnitude[1:5]
    low_energy = np.mean(low_freq_bins)
    pull_factor = 1 + (low_energy / 500.0)

    # --- Update Particles ---
    for p in particles:
        total_force = np.array([0.0, 0.0])
        for gc in gravity_centers:
            direction = gc - p.pos
            distance = np.linalg.norm(direction) + 1e-5
            force = pull_factor * speed_multiplier * direction / (distance ** 2)
            total_force += force
        p.update(total_force, dt=1)
        p.pos[0] %= WIDTH
        p.pos[1] %= HEIGHT

    # --- Drawing ---
    screen.fill((0, 0, 0))
    for gc in gravity_centers:
        pygame.draw.circle(screen, (255, 255, 255), (int(gc[0]), int(gc[1])), 5)
    for p in particles:
        pygame.draw.circle(screen, (255, 255, 255), (int(p.pos[0]), int(p.pos[1])), 2)
        for gc in gravity_centers:
            pygame.draw.aaline(screen, (255, 255, 255),
                               (int(p.pos[0]), int(p.pos[1])),
                               (int(gc[0]), int(gc[1])))
    bpm_text = font.render(f"BPM: {stable_bpm:.2f}", True, (255, 255, 255))
    screen.blit(bpm_text, (10, 10))
    pygame.display.flip()
    clock.tick(60)

stream.stop()
pygame.quit()
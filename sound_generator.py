# sound_generator.py
import numpy as np
from scipy.io import wavfile
from scipy import signal as sig
import os
import tempfile

SAMPLE_RATE = 44100  # Standard sample rate for audio


def _save_wav(samples, filename_prefix):
    """Helper function to normalize, convert to 16-bit, and save WAV."""
    # Normalize to -1.0 to 1.0
    samples = samples / np.max(np.abs(samples)) if np.max(np.abs(samples)) > 0 else samples
    # Convert to 16-bit integers
    samples_int16 = (samples * 32767).astype(np.int16)

    # Create a temporary file
    fd, path = tempfile.mkstemp(suffix=".wav", prefix=f"{filename_prefix}_")
    os.close(fd)  # Close the file descriptor opened by mkstemp

    wavfile.write(path, SAMPLE_RATE, samples_int16)
    return path


def generate_beep(duration=0.2, frequency=1000):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    samples = 0.5 * np.sin(2 * np.pi * frequency * t)
    # Simple fade in/out to avoid clicks
    fade_len = int(SAMPLE_RATE * 0.01)
    samples[:fade_len] *= np.linspace(0, 1, fade_len)
    samples[-fade_len:] *= np.linspace(1, 0, fade_len)
    return _save_wav(samples, "beep")


def generate_laser(duration=0.3, start_freq=2000, end_freq=200):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    # Logarithmic sweep sounds more "laser-like"
    current_freq = np.logspace(np.log10(start_freq), np.log10(end_freq), len(t))
    samples = 0.4 * np.sin(2 * np.pi * current_freq * t)
    fade_len = int(SAMPLE_RATE * 0.02)
    samples[:fade_len] *= np.linspace(0, 1, fade_len)
    samples[-fade_len:] *= np.linspace(1, 0, fade_len)
    return _save_wav(samples, "laser")


def generate_explosion(duration=1.0):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    noise = np.random.uniform(-1, 1, len(t))

    # Low-pass filter the noise and apply a decaying envelope
    # For simplicity, we'll use a strong decay envelope
    decay = np.exp(-t * 5)  # Exponential decay

    # Add some "rumble" by mixing low frequency sine waves
    rumble = 0.3 * np.sin(2 * np.pi * 60 * t) + 0.2 * np.sin(2 * np.pi * 40 * t)

    samples = (noise * 0.6 + rumble * 0.4) * decay
    return _save_wav(samples, "explosion")


def generate_click(duration=0.05, frequency=1500):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    samples = 0.8 * np.sin(2 * np.pi * frequency * t)
    # Very sharp decay
    samples *= np.exp(-t * 150)
    return _save_wav(samples, "click")


def generate_power_up(duration=0.5, start_freq=200, end_freq=1000):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    current_freq = np.linspace(start_freq, end_freq, len(t))
    samples = 0.5 * sig.square(2 * np.pi * current_freq * t, duty=0.5)  # Square wave
    fade_len = int(SAMPLE_RATE * 0.05)
    samples[:fade_len] *= np.linspace(0, 1, fade_len)
    samples[-fade_len:] *= np.linspace(1, 0, fade_len)
    return _save_wav(samples, "power_up")


def generate_coin(duration=0.2, frequency=2000, high_freq_mod=4000):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    main_tone = 0.5 * np.sin(2 * np.pi * frequency * t)
    mod_tone = 0.3 * np.sin(2 * np.pi * high_freq_mod * t)
    samples = (main_tone + mod_tone) * np.exp(-t * 30)  # Quick decay
    return _save_wav(samples, "coin")


def generate_woosh(duration=0.5):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    noise = np.random.uniform(-0.5, 0.5, len(t))
    # Create a band-pass filter effect by sweeping frequencies (simplified)
    # We'll simulate this with a rising and falling amplitude envelope
    envelope = np.sin(np.pi * t / duration) ** 2  # Hump shape
    samples = noise * envelope
    return _save_wav(samples, "woosh")


def generate_siren(duration=1.0, freq1=600, freq2=800, switch_time=0.3):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    # Create a signal that alternates between freq1 and freq2
    mod_wave = sig.square(2 * np.pi * (1 / (2 * switch_time)) * t)  # Switches every switch_time
    current_freq = np.where(mod_wave > 0, freq1, freq2)
    samples = 0.4 * np.sin(2 * np.pi * current_freq * t)
    return _save_wav(samples, "siren")


def generate_blip(duration=0.1, frequency=1200, sweep_factor=1.5):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    # Frequency quickly sweeps up
    current_freq = frequency * (1 + sweep_factor * (t / duration))
    samples = 0.6 * np.sin(2 * np.pi * current_freq * t)
    samples *= np.exp(-t * 60)  # Fast decay
    return _save_wav(samples, "blip")


def generate_hit(duration=0.15, base_freq=150):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    noise = np.random.uniform(-0.3, 0.3, len(t))
    tone = 0.7 * np.sin(2 * np.pi * base_freq * t)
    samples = (noise + tone) * np.exp(-t * 40)  # Sharp decay
    return _save_wav(samples, "hit")


def generate_static(duration=0.5):
    samples = np.random.uniform(-0.3, 0.3, int(SAMPLE_RATE * duration))
    return _save_wav(samples, "static")


def generate_boing(duration=0.4, start_freq=1000, end_freq=100, oscillations=3):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    # Frequency decays while oscillating
    freq_decay = np.exp(-t * 5) * (start_freq - end_freq) + end_freq
    freq_oscillation = (start_freq - end_freq) / 5 * np.sin(2 * np.pi * oscillations * t / duration)
    current_freq = freq_decay + freq_oscillation
    current_freq = np.maximum(current_freq, 20)  # Ensure positive frequency

    samples = 0.5 * np.sin(2 * np.pi * current_freq * t)
    samples *= np.exp(-t * 8)  # Overall amplitude decay
    return _save_wav(samples, "boing")


# --- List of sound effects for the app ---
SOUND_EFFECTS_GENERATORS = {
    "Beep": generate_beep,
    "Laser": generate_laser,
    "Explosion": generate_explosion,
    "Click": generate_click,
    "Power Up": generate_power_up,
    "Coin": generate_coin,
    "Woosh": generate_woosh,
    "Siren": generate_siren,
    "Blip": generate_blip,
    "Hit": generate_hit,
    "Static": generate_static,
    "Boing": generate_boing,
}

# --- Cleanup function ---
TEMP_FILES = []


def add_temp_file(path):
    TEMP_FILES.append(path)


def cleanup_temp_files():
    for f_path in TEMP_FILES:
        try:
            if os.path.exists(f_path):
                os.remove(f_path)
        except Exception as e:
            print(f"Error removing temp file {f_path}: {e}")
    TEMP_FILES.clear()
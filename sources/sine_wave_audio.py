import pathlib
import wave

import numpy as np

OUTPUT_PATH = pathlib.Path(__file__).with_name("sine_wave_foundation.wav")


def generate_sine_wave_audio(
    frequency=440,
    duration=2,
    sample_rate=44100,
    width_control=0.0,
):
    """
    Generate a sine wave audio file based on the visual Core Structure pattern.
    This creates an audible representation of the sine wave foundation.
    """
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    # Clamp the user control so "left" (-1) widens and "right" (+1) narrows the band
    width_control = float(np.clip(width_control, -1.0, 1.0))

    # Map control to modulation characteristics
    modulation_depth = np.interp(width_control, [-1.0, 1.0], [0.6, 0.05])
    modulation_rate = np.interp(width_control, [-1.0, 1.0], [0.5, 4.0])

    # Create a pure sine wave (harmonic foundation)
    sine_wave = np.sin(frequency * 2 * np.pi * t)

    # Add some modulation to represent the "four blocks" pattern
    # Modulate with a slower sine wave for the repeating structure
    modulation = modulation_depth * np.sin(2 * np.pi * modulation_rate * t)
    modulated_wave = sine_wave * (1 + modulation)

    # Normalize to prevent clipping
    modulated_wave = modulated_wave / np.max(np.abs(modulated_wave))

    # Save as WAV file using the standard library to avoid external dependencies
    pcm_wave = (modulated_wave * 32767).astype(np.int16)

    with wave.open(str(OUTPUT_PATH), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)  # 16-bit audio
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(pcm_wave.tobytes())

    # Provide a brief textual summary so the code "speaks" through the console
    print("Audible Sine Wave Foundation")
    print(f"  Frequency       : {frequency} Hz")
    print(f"  Duration        : {duration} seconds")
    print(f"  Width control   : {width_control:+.2f}")
    print(f"    depth         : {modulation_depth:.2f}")
    print(f"    modulation Hz : {modulation_rate:.2f}")
    print(f"  Saved to        : {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_sine_wave_audio()

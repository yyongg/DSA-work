"""Apply the FFT to A440.wav to find the pitch of the recorded tone."""

import math
import wave

import matplotlib.pyplot as plt

from fft import fft

N = 2 ** 16  # number of samples to analyze; the FFT needs a power of 2

with wave.open("A440.wav", "rb") as f:
    rate = f.getframerate()
    channels = f.getnchannels()
    frames = f.readframes(N)

# Samples are 16-bit little-endian; keep only the first channel
samples = [int.from_bytes(frames[i:i + 2], "little", signed=True)
           for i in range(0, len(frames), 2 * channels)]

coefficients = fft(samples)
magnitudes = [math.hypot(re, im) for re, im in coefficients[:N // 2]]
freqs = [k * rate / N for k in range(N // 2)]

peak = max(range(1, N // 2), key=lambda k: magnitudes[k])
print(f"Analyzed {N} samples ({N / rate:.2f} s) at {rate} Hz")
print(f"Frequency resolution: {rate / N:.2f} Hz")
print(f"Peak frequency: {freqs[peak]:.1f} Hz")

plt.figure(figsize=(10, 4))
plt.plot(freqs, magnitudes, color="#2a78d6")
plt.xlim(0, 2000)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title(f"FFT of A440.wav: peak at {freqs[peak]:.1f} Hz")
plt.tight_layout()
plt.savefig("a440_spectrum.png", dpi=150)

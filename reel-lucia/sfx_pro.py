import numpy as np, wave, sys
SR = 44100
rng = np.random.default_rng(7)
def make(dur): return np.zeros(int(SR * dur))
def add(out, sig, t, g=1.0):
    i = int(t * SR); n = min(len(sig), len(out) - i)
    if n > 0: out[i:i + n] += sig[:n] * g
def env(n, att, dec):
    tt = np.arange(n) / SR; return np.minimum(1, tt / att) * np.exp(-tt / dec)
def lowpass(x, k=6):
    return np.convolve(x, np.ones(k) / k, 'same')
def pop(a=0.22):
    n = int(0.09 * SR); tt = np.arange(n) / SR
    f = 520 * np.exp(-tt * 18) + 260
    ph = 2 * np.pi * np.cumsum(f) / SR
    return lowpass(np.sin(ph) * env(n, 0.002, 0.03), 8) * a
def bell(freq, a=0.12, dec=0.55):
    n = int(1.4 * SR); tt = np.arange(n) / SR
    x = (np.sin(2 * np.pi * freq * tt) + 0.35 * np.sin(2 * np.pi * freq * 2.01 * tt) + 0.12 * np.sin(2 * np.pi * freq * 3.98 * tt))
    return x * env(n, 0.004, dec) * a
def ding2(a=0.11):
    o = np.zeros(int(1.6 * SR)); add(o, bell(1318.5, a), 0); add(o, bell(1975.5, a * 0.9), 0.09); return o
def success(a=0.10):
    o = np.zeros(int(2.0 * SR))
    for k, f in enumerate([523.25, 659.25, 783.99, 1046.5]): add(o, bell(f, a, 0.8), k * 0.05)
    return o
def tick(a=0.05):
    n = int(0.025 * SR); tt = np.arange(n) / SR
    return np.sin(2 * np.pi * 2400 * tt) * env(n, 0.0008, 0.006) * a
def whoosh(l=0.45, a=0.07):
    n = int(l * SR); x = rng.standard_normal(n)
    x = lowpass(lowpass(x, 40), 40) * np.hanning(n)
    return x / (np.abs(x).max() + 1e-9) * a
def counter(out, t0, t1):
    t = t0; step = 0.045
    while t < t1:
        add(out, tick(), t); t += step; step *= 1.06
def reverb(x, wet=0.22):
    n = int(0.8 * SR); ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR / 0.25)
    ir /= np.abs(ir).sum() / 8
    y = np.convolve(x, ir)[:len(x)]
    return x * (1 - wet) + y * wet
def save(out, path):
    out = reverb(out); out = np.clip(out, -1, 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes())

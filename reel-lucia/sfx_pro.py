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

# ---------- soft palette (v2) ----------
def lp(x, k): return np.convolve(x, np.ones(k) / k, 'same')
def soft_tap(a=0.07):
    n = int(0.06 * SR); tt = np.arange(n) / SR
    body = np.sin(2 * np.pi * 820 * tt) * env(n, 0.001, 0.012)
    noise = lp(rng.standard_normal(n), 30) * env(n, 0.0005, 0.006) * 0.6
    return lp(body + noise, 10) * a
def marimba(freq, a=0.06, dec=0.28):
    n = int(1.0 * SR); tt = np.arange(n) / SR
    x = np.sin(2 * np.pi * freq * tt) * env(n, 0.003, dec) + 0.25 * np.sin(2 * np.pi * freq * 4 * tt) * env(n, 0.002, dec / 5)
    return lp(x, 4) * a
def detect_soft(a=0.06):
    o = np.zeros(int(1.2 * SR)); add(o, marimba(783.99, a), 0); add(o, marimba(1046.5, a * 0.9), 0.12); return o
def pad(freqs, dur=1.6, a=0.02):
    n = int(dur * SR); tt = np.arange(n) / SR
    e = np.minimum(1, tt / 0.15) * np.exp(-np.maximum(0, tt - 0.3) / 0.6)
    return sum(np.sin(2 * np.pi * f * tt) for f in freqs) * e * a
def success_soft(a=0.055):
    o = np.zeros(int(2.0 * SR))
    for k, f in enumerate([523.25, 659.25, 783.99]): add(o, marimba(f, a, 0.35), k * 0.09)
    add(o, pad([261.63, 329.63, 392.0], 1.8, 0.018), 0.05)
    return o
def tick_soft(a=0.018):
    n = int(0.02 * SR); tt = np.arange(n) / SR
    return lp(np.sin(2 * np.pi * 1500 * tt) * env(n, 0.0008, 0.005), 3) * a
def counter_soft(out, t0, t1):
    t = t0; step = 0.05
    while t < t1:
        add(out, tick_soft(), t); t += step; step *= 1.07

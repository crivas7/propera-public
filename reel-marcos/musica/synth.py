"""Música original para el reel «Día 30» (Marcos), sintetizada aquí mismo (sin samples ni licencias).

Estructura común, a 100 BPM (1 tiempo = 0,6 s), cuadrada con el montaje:
  0–11 s     día 30 y recuerdos: contenida, algo de tensión (La menor), reloj que avanza en los recuerdos
  11 s       «Mes siguiente»: se abre a un groove optimista en Do mayor (Do–Sol–Lam–Fa)
  29 s       golpe final en Do mayor que se apaga con el logo

Uso: python3 synth.py OPCION SALIDA.wav [DURACION]
  OPCION: a = lo-fi cálido · b = pop acústico · c = piano emotivo
"""
import sys
import numpy as np
from scipy.signal import lfilter, butter, sosfilt, fftconvolve
from scipy.io import wavfile

SR = 44100
OPT = sys.argv[1]
OUT = sys.argv[2]
DUR = float(sys.argv[3]) if len(sys.argv) > 3 else 32.2
B = 0.6            # un tiempo a 100 BPM
LIFT = 11.0        # «Mes siguiente»
HIT = 29.0         # golpe final
N = int(DUR * SR)
rng = np.random.default_rng(7)

L = np.zeros(N); R = np.zeros(N)

def add(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N or i + len(sig) <= 0: return
    if i < 0: sig = sig[-i:]; i = 0
    sig = sig[: N - i]
    l = gain * np.cos((pan + 1) * np.pi / 4); r = gain * np.sin((pan + 1) * np.pi / 4)
    L[i:i + len(sig)] += sig * l * 1.414; R[i:i + len(sig)] += sig * r * 1.414

def tt(d): return np.arange(int(d * SR)) / SR
def env(d, a=0.005, dec=0.3):
    t = tt(d); e = np.minimum(1, t / a) * np.exp(-t / dec)
    return e
def filt(x, kind, f, order=2):
    sos = butter(order, f, btype=kind, fs=SR, output="sos"); return sosfilt(sos, x)
def mtof(m): return 440.0 * 2 ** ((m - 69) / 12)

# ---------- instrumentos ----------
def kick(g=1.0):
    t = tt(0.45); f = 45 + 75 * np.exp(-t / 0.04)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return g * np.sin(ph) * np.exp(-t / 0.18) + 0.15 * g * filt(rng.standard_normal(len(t)), "highpass", 2000) * np.exp(-t / 0.006)
def snare(g=1.0):
    t = tt(0.3); n = filt(rng.standard_normal(len(t)), "bandpass", [1500, 7000]) * np.exp(-t / 0.09)
    return g * (0.7 * n + 0.4 * np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05))
def clap(g=1.0):
    t = tt(0.35); x = np.zeros(len(t))
    for k, o in enumerate([0, 0.011, 0.022, 0.034]):
        i = int(o * SR); m = len(t) - i
        x[i:] += rng.standard_normal(m) * np.exp(-np.arange(m) / SR / (0.012 if k < 3 else 0.11))
    return g * 0.6 * filt(x, "bandpass", [900, 3500])
def hat(g=1.0, d=0.045):
    t = tt(0.15); return g * 0.35 * filt(rng.standard_normal(len(t)), "highpass", 7000) * np.exp(-t / d)
def shaker(g=1.0):
    t = tt(0.12); e = np.minimum(1, t / 0.02) * np.exp(-t / 0.035)
    return g * 0.25 * filt(rng.standard_normal(len(t)), "bandpass", [4500, 11000]) * e
def tick(g=1.0, f=1900):  # reloj / bloque de madera
    t = tt(0.08); return g * 0.5 * np.sin(2 * np.pi * f * t) * np.exp(-t / 0.012)
def bass(m, d, g=1.0):
    t = tt(d); f = mtof(m)
    x = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t) + 0.08 * np.sin(6 * np.pi * f * t)
    e = np.minimum(1, t / 0.01) * np.exp(-t / (d * 0.9)) * np.minimum(1, (d - t) / 0.03)
    return g * 0.55 * x * e
def ep(m, d, g=1.0):  # piano eléctrico (FM)
    t = tt(d + 0.8); f = mtof(m)
    idx = 1.8 * np.exp(-t / 0.25) + 0.25
    x = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * t))
    x += 0.15 * np.sin(2 * np.pi * 14 * f * t) * np.exp(-t / 0.02)  # «tine»
    e = np.minimum(1, t / 0.004) * np.exp(-t / 1.1)
    rel = np.clip((d + 0.8 - t) / 0.8, 0, 1)
    return g * 0.22 * x * e * rel * (1 + 0.12 * np.sin(2 * np.pi * 4.5 * t))
def piano(m, d, g=1.0):
    t = tt(d + 1.5); f = mtof(m); x = np.zeros(len(t))
    for n in range(1, 11):
        fn = f * n * np.sqrt(1 + 0.0004 * n * n)
        if fn > 16000: break
        x += (1 / n ** 1.25) * np.sin(2 * np.pi * fn * t + rng.uniform(0, 6)) * np.exp(-t / (2.4 / (1 + 0.45 * n)))
    x += 0.04 * filt(rng.standard_normal(len(t)), "bandpass", [800, 5000]) * np.exp(-t / 0.01)
    e = np.minimum(1, t / 0.003) * np.clip((d + 1.5 - t) / 1.5, 0, 1)
    return g * 0.2 * x * e
def pluck(m, d, g=1.0, damp=0.996, bright=0.5):  # Karplus-Strong
    f = mtof(m); P = int(SR / f); n = int((d + 0.4) * SR)
    x = np.zeros(n); burst = rng.uniform(-1, 1, P)
    burst = lfilter([1 - bright], [1, -bright], burst)
    x[:P] = burst
    a = np.zeros(P + 2); a[0] = 1; a[P] = -0.5 * damp; a[P + 1] = -0.5 * damp
    y = lfilter([1], a, x)
    rel = np.clip((d + 0.4 - np.arange(n) / SR) / 0.4, 0, 1)
    return g * 0.35 * y * rel
def bell(m, d, g=1.0):
    t = tt(d + 1.0); f = mtof(m)
    x = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2.76 * f * t) * np.exp(-t / 0.3) + 0.15 * np.sin(2 * np.pi * 5.4 * f * t) * np.exp(-t / 0.12)
    return g * 0.16 * x * np.minimum(1, t / 0.002) * np.exp(-t / 0.9)
def pad(ms, d, g=1.0, cut=1800):
    t = tt(d); x = np.zeros(len(t))
    for m in ms:
        for det in (-0.08, 0.0, 0.08):
            f = mtof(m + det); ph = (f * t + rng.uniform()) % 1.0
            x += 2 * ph - 1
    x = filt(x, "lowpass", cut, 2)
    e = np.minimum(1, t / 0.6) * np.minimum(1, (d - t) / 0.6)
    return g * 0.035 * x * e
def riser(t0, t1, g=1.0):
    d = t1 - t0; t = tt(d); x = rng.standard_normal(len(t)); y = np.zeros(len(t))
    seg = int(0.05 * SR)
    for i in range(0, len(t), seg):  # barrido de filtro hacia arriba
        fc = 300 + 7000 * (i / len(t)) ** 2
        y[i:i + seg] = filt(x[i:i + seg + 2000], "bandpass", [fc * 0.7, min(fc * 1.4, 18000)], 2)[:len(y[i:i + seg])]
    add(g * 0.25 * y * (t / d) ** 2, t0, 1.0, 0)

def chord(name, base=60):
    root = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[name[0]]
    minor = "m" in name[1:] and "maj" not in name
    third = 3 if minor else 4
    notes = [root, root + third, root + 7]
    if "7" in name: notes.append(root + (11 if "maj" in name else 10))
    if "9" in name: notes.append(root + 14)
    if "sus" in name: notes[1] = root + 5
    out = []
    for n in notes:
        v = base + (n % 12)
        while v < base: v += 12
        out.append(v)
    return sorted(out), base - 24 + root

# progresiones
INTRO = [(0.0, "Am"), (1.4, "Am"), (3.8, "F"), (6.2, "Dm"), (8.6, "Gsus")]   # hasta 11 s
GROOVE = ["C", "G", "Am", "F"]
def bar_chords():
    out = []
    for k in range(8):
        t0 = LIFT + k * 4 * B
        if t0 >= HIT: break
        out.append((t0, GROOVE[k % 4]))
    return out
BARS = bar_chords()

def beats(t0, t1, step=B):
    k0 = int(np.ceil((t0 - LIFT) / step - 1e-6)); t = LIFT + k0 * step
    while t < t1 - 1e-6:
        yield t; t += step

# ---------- arreglos ----------
import os
SIN_INTRO = bool(os.environ.get("SIN_INTRO"))  # SIN_INTRO=1: la música solo entra en «Mes siguiente / Día 1»

def arr_lofi():
    # intro: arpegio apagado + bajo largo; recuerdos: reloj y bombo suave
    for i, (t0, c) in enumerate([] if SIN_INTRO else INTRO):
        t1 = INTRO[i + 1][0] if i + 1 < len(INTRO) else LIFT
        ns, root = chord(c, 57)
        add(bass(root, t1 - t0, 0.7), t0)
        seq = [ns[0], ns[1], ns[2], ns[1] + 12 if len(ns) > 1 else ns[0]]
        for j, bt in enumerate(beats(max(t0, 0.2), t1, B / 2)):
            add(pluck(seq[j % 4], 0.25, 0.55, damp=0.985, bright=0.2), bt, 1.0, -0.3 + 0.2 * (j % 3))
    if not SIN_INTRO:
        for bt in beats(4.1, LIFT, B / 2): add(tick(0.35 if int(round((bt - LIFT) / (B / 2))) % 2 == 0 else 0.22), bt, 1.0, 0.35)
        for bt in beats(6.2, LIFT, B * 2): add(kick(0.55), bt)
        riser(9.2, LIFT, 0.8)
    # groove
    for t0, c in BARS:
        ns, root = chord(c + ("maj7" if c in ("C", "F") else ("m7" if c == "Am" else "")), 60)
        for off, ln in [(0, 0.95), (1.5 * B, 0.5), (2.5 * B, 0.9)]:
            for n in ns: add(ep(n, ln, 0.85), t0 + off + 0.012 * ns.index(n), 1.0, -0.15)
        add(bass(root, 1.3 * B, 0.95), t0); add(bass(root, 0.9 * B, 0.8), t0 + 1.75 * B); add(bass(root + 7, 0.9 * B, 0.7), t0 + 3 * B)
        add(kick(0.9), t0); add(kick(0.6), t0 + 1.75 * B); add(kick(0.75), t0 + 2.5 * B)
        add(snare(0.55), t0 + B); add(snare(0.55), t0 + 3 * B)
        for j in range(8):
            sw = 0.06 * B if j % 2 else 0
            add(hat(0.5 if j % 2 == 0 else 0.32), t0 + j * B / 2 + sw, 1.0, 0.25)
    ns, root = chord("Cmaj9", 60)
    for n in ns: add(ep(n, 2.6, 0.95), HIT + 0.015 * ns.index(n))
    add(bass(root, 2.5, 0.9), HIT); add(kick(0.7), HIT)
    # crujido de vinilo
    cr = np.zeros(N); idx = rng.integers(0, N, int(DUR * 25)); cr[idx] = rng.uniform(-1, 1, len(idx))
    cr = filt(cr, "bandpass", [1500, 6000]) * 0.9
    if SIN_INTRO: cr[: int(LIFT * SR)] = 0
    L[:] += cr * 0.5; R[:] += np.roll(cr, 300) * 0.5

def arr_pop():
    for i, (t0, c) in enumerate(INTRO):
        t1 = INTRO[i + 1][0] if i + 1 < len(INTRO) else LIFT
        ns, root = chord(c, 52)
        add(bass(root, t1 - t0, 0.55), t0)
        for bt in beats(max(t0, 0.2), t1, B / 2):  # guitarra apagada (palm mute)
            for k, n in enumerate([root + 12, root + 19]): add(pluck(n, 0.12, 0.5, damp=0.97, bright=0.15), bt + 0.004 * k, 1.0, -0.25)
    for bt in beats(4.1, LIFT, B / 2): add(shaker(0.8), bt, 1.0, 0.3)
    for bt in beats(4.1, LIFT, B): add(tick(0.28, 1500), bt, 1.0, -0.3)
    riser(9.0, LIFT, 0.9)
    strum = [(0, 1), (B, 1), (1.5 * B, -1), (2.5 * B, -1), (3 * B, 1), (3.5 * B, -1)]
    hook = {"C": [76, 79, 81, 79], "G": [74, 79, 83, 81], "Am": [76, 81, 84, 83], "F": [77, 81, 84, 81]}
    for k, (t0, c) in enumerate(BARS):
        ns, root = chord(c, 52)
        voic = sorted(set([root + 12, root + 19] + [n + 12 for n in ns]))
        for off, dirn in strum:  # rasgueo
            seq = voic if dirn > 0 else voic[::-1]
            for j, n in enumerate(seq): add(pluck(n, 0.6, 0.42, damp=0.994, bright=0.55), t0 + off + 0.012 * j, 1.0, 0.2 * dirn)
        add(bass(root, 0.9 * B, 1.0), t0); add(bass(root, 0.5 * B, 0.8), t0 + 1.5 * B); add(bass(root + 7, 0.9 * B, 0.8), t0 + 2 * B); add(bass(root, 0.9 * B, 0.8), t0 + 3 * B)
        add(kick(0.85), t0); add(kick(0.7), t0 + 2 * B)
        add(clap(0.75), t0 + B, 1.0, 0.05); add(clap(0.75), t0 + 3 * B, 1.0, -0.05)
        for j in range(8): add(shaker(0.9 if j % 2 else 0.6), t0 + j * B / 2, 1.0, 0.35)
        if k >= 2:  # melodía de campanitas desde el tercer compás
            for j, n in enumerate(hook[c]): add(bell(n, 0.4, 0.9), t0 + [0, 0.5, 1.5, 2.5][j] * B, 1.0, -0.2)
    ns, root = chord("C", 52)
    voic = sorted(set([root + 12, root + 19] + [n + 12 for n in ns]))
    for j, n in enumerate(voic): add(pluck(n, 2.8, 0.5, damp=0.998, bright=0.6), HIT + 0.02 * j)
    add(bell(84, 2.5, 0.9), HIT + 0.05); add(bass(root, 2.5, 0.9), HIT); add(kick(0.8), HIT); add(clap(0.5), HIT)

def arr_piano():
    add(pad([57, 64], LIFT - 0.0, 0.8, 900), 0.0)
    notes = [(0.3, 69), (1.4, 64), (2.6, 72), (3.8, 65), (5.0, 69), (6.2, 62), (7.4, 65), (8.6, 67), (9.8, 71)]
    for t0, m in notes: add(piano(m, 1.2, 0.7), t0, 1.0, 0.1)
    for i, (t0, c) in enumerate(INTRO):
        t1 = INTRO[i + 1][0] if i + 1 < len(INTRO) else LIFT
        ns, root = chord(c, 57); add(piano(root, t1 - t0, 0.55), t0, 1.0, -0.2)
    for bt in beats(4.1, LIFT, B): add(tick(0.25, 2100), bt, 1.0, 0.4)
    for bt in beats(4.1, LIFT, B): add(piano(45, 0.25, 0.25), bt, 1.0, -0.3)  # pulso grave
    riser(9.6, LIFT, 0.5)
    mel = {"C": [79, 76, 72], "G": [79, 74, 71], "Am": [81, 76, 72], "F": [81, 77, 72]}
    for k, (t0, c) in enumerate(BARS):
        ns, root = chord(c + ("add9" if c in ("C", "F") else ""), 60)
        add(pad(ns, 4 * B + 0.4, 0.7, 2200), t0 - 0.1)
        for j, off in enumerate([0, 1, 2, 3]):  # acordes en negras
            for n in ns: add(piano(n, 0.55, 0.42 if j else 0.55), t0 + off * B + 0.01 * ns.index(n), 1.0, -0.1)
        add(piano(root, 4 * B, 0.7), t0, 1.0, -0.2); add(piano(root + 12, 2 * B, 0.35), t0 + 2 * B, 1.0, -0.2)
        if k >= 1:
            for j, n in enumerate(mel[c]): add(piano(n, 0.9, 0.55), t0 + [0.5, 1.5, 2.5][j] * B, 1.0, 0.15)
        add(kick(0.55), t0); add(kick(0.35), t0 + 2 * B)
        for j in range(4): add(shaker(0.5), t0 + (j + 0.5) * B, 1.0, 0.3)
    ns, root = chord("Cadd9", 60)
    for n in ns: add(piano(n, 2.8, 0.7), HIT + 0.02 * ns.index(n))
    add(piano(root, 3.0, 0.8), HIT); add(piano(84, 2.5, 0.4), HIT + 0.3); add(pad(ns, 3.0, 0.8, 2000), HIT)

{"a": arr_lofi, "b": arr_pop, "c": arr_piano}[OPT]()

# ---------- mezcla final: reverb, color, nivel ----------
ir_len = int(1.6 * SR); ti = np.arange(ir_len) / SR
irL = rng.standard_normal(ir_len) * np.exp(-ti / 0.45); irR = rng.standard_normal(ir_len) * np.exp(-ti / 0.45)
irL = filt(irL, "lowpass", 6000); irR = filt(irR, "lowpass", 6000)
irL /= np.sqrt(np.sum(irL ** 2)); irR /= np.sqrt(np.sum(irR ** 2))
wet = {"a": 0.18, "b": 0.14, "c": 0.28}[OPT]
L2 = L + wet * fftconvolve(L, irL)[:N]; R2 = R + wet * fftconvolve(R, irR)[:N]
if OPT == "a":  # color lo-fi
    L2 = filt(L2, "lowpass", 9000); R2 = filt(R2, "lowpass", 9000)
L2 = filt(L2, "highpass", 30); R2 = filt(R2, "highpass", 30)
fade = np.ones(N); fl = int(0.25 * SR); fade[-fl:] = np.linspace(1, 0, fl)
st = np.stack([L2 * fade, R2 * fade], 1)
st = np.tanh(1.2 * st / (np.max(np.abs(st)) + 1e-9)) * 0.85
wavfile.write(OUT, SR, (st * 32767).astype(np.int16))
print(OUT, f"{DUR:.1f}s")

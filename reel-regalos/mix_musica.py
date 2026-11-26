"""Adapta la música de ElevenLabs (musica/eleven_navidad.mp3) a las escenas del reel -> musica/musica_regalos.wav.

La canción tiene una intro suave (0–9 s) y a los 9 s «coge fuerza». Montaje:
- gancho y lista: la intro (entra 0,5 s tarde para que la subida no caiga antes de «el año pasado»);
  muy baja durante la primera frase;
- «el año pasado»: un trozo de la intro, muy bajo y apagado (paso bajo);
- «Este año…» (Propera): la subida de la canción cae justo cuando empieza la escena, y sigue a tope hasta el final;
- se desvanece en el último segundo.
"""
import json, os, subprocess
import numpy as np
from scipy.signal import butter, sosfiltfilt
from scipy.io import wavfile

HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, "timeline.json")))
SR = 48000
DROP = 9.0          # segundo de la canción en el que coge fuerza
src, out = os.path.join(HERE, "musica", "eleven_navidad.mp3"), os.path.join(HERE, "musica", "musica_regalos.wav")
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
song = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).astype(np.float64)
N = int(T["DUR"] * SR)
ly, fx = T["lastyear"], T["fix"]
lp = sosfiltfilt(butter(4, 500, "low", fs=SR, output="sos"), song, axis=0)

def piece(src_arr, v0, v1, s0):
    """Trozo de la canción que empieza en su segundo s0 y suena en el vídeo de v0 a v1."""
    n = int((v1 - v0) * SR); a = int(s0 * SR)
    seg = src_arr[a:a + n]
    if len(seg) < n: seg = np.vstack([seg, np.zeros((n - len(seg), 2))])
    return seg

XF = 0.15
y = np.zeros((N + SR, 2))
def place(seg, v0, fin=XF, fout=XF):
    seg = seg.copy(); n = len(seg); i0 = int(v0 * SR)
    if fin: k = int(fin * SR); seg[:k] *= np.linspace(0, 1, k)[:, None]
    if fout: k = int(fout * SR); seg[-k:] *= np.linspace(1, 0, k)[:, None]
    y[i0:i0 + n] += seg

START = 0.5
place(piece(song, START, ly + XF, 0.0), START, fin=0.05)                    # intro: gancho y lista
place(piece(lp, ly, fx - 0.4 + XF, 2.0) * 10 ** (-17 / 20), ly)            # «el año pasado»: bajo y apagado
place(piece(song, fx - 0.4, T["DUR"], DROP - 0.4), fx - 0.4, fout=0)      # la subida cae al empezar «Este año…»
y = y[:N]

t = np.arange(N) / SR
def ramp(a, b): return np.clip((t - a) / (b - a), 0, 1)
db = np.full(N, 3.0)                                         # intro un poco más alta (es suave)
db += -12.0 * (1 - ramp(T["list"] - 0.6, T["list"] + 0.2))   # primera frase: música muy baja
db += -3.0 * ramp(fx - 0.45, fx - 0.4)                       # desde «Este año…»: la canción a su nivel
g = 10 ** (db / 20) * (1 - ramp(T["DUR"] - 1.3, T["DUR"] - 0.05))
y *= g[:, None]
y /= max(1.0, np.abs(y).max() / 0.95)
wavfile.write(out, SR, (y * 32767).astype(np.int16))
print(out, f"{T['DUR']}s")

"""Adapta la música de ElevenLabs (musica/eleven_navidad.mp3) a las escenas del reel -> musica/musica_regalos.wav.

- gancho y lista: un poco más alta (la intro de la canción es suave);
- «el año pasado»: baja mucho y se apaga (filtro paso bajo), como si se desinflara;
- Propera: vuelve, todavía contenida;
- final feliz: a tope; se desvanece en el último segundo.
"""
import json, os, subprocess
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfiltfilt

HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, "timeline.json")))
SR = 48000
src, out = os.path.join(HERE, "musica", "eleven_navidad.mp3"), os.path.join(HERE, "musica", "musica_regalos.wav")
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
x = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).astype(np.float64)
N = int(T["DUR"] * SR)
if len(x) < N: x = np.vstack([x, np.zeros((N - len(x), 2))])
x = x[:N]
t = np.arange(N) / SR

def ramp(a, b, d=0.25):  # 0 antes de a, 1 después de a+d ... (suave)
    return np.clip((t - a) / d, 0, 1)

db = np.full(N, 3.0)                                   # gancho y lista: +3 dB
ly, fx, hp, en = T["lastyear"], T["fix"], T["happy"], T["end"]
db += (-17.0 - 3.0) * ramp(ly - 0.05, ly + 0.25)        # el año pasado: muy baja
db += (-5.0 + 17.0) * ramp(fx - 0.2, fx + 0.6)          # Propera: vuelve contenida
db += (0.0 + 5.0) * ramp(hp - 0.6, hp + 0.1)            # final feliz: a tope
g = 10 ** (db / 20) * (1 - ramp(T["DUR"] - 1.3, T["DUR"] - 0.05, 1.25))
muffle = ramp(ly - 0.05, ly + 0.3) * (1 - ramp(fx - 0.3, fx + 0.3))   # paso bajo solo en «el año pasado»
lp = sosfiltfilt(butter(4, 500, "low", fs=SR, output="sos"), x, axis=0)
y = (x * (1 - muffle)[:, None] + lp * muffle[:, None]) * g[:, None]
y /= max(1.0, np.abs(y).max() / 0.95)
wavfile.write(out, SR, (y * 32767).astype(np.int16))
print(out, f"{T['DUR']}s")

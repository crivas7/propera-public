import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import render as R
CUES = [
 (5.45, 7.7, "Quería estas zapatillas. Noventa euros."),
 (7.7, 9.1, "¿Me las puedo permitir?"),
 (9.4, 12.15, "Se lo pregunto a ChatGPT, que tiene Propera conectado."),
 (12.45, 13.3, "Y me lo dice claro:"),
 (13.6, 16.2, "430 € ya están comprometidos."),
 (16.2, 18.0, "Alquiler, luz, gimnasio."),
 (18.3, 20.9, "Lo que tengo de verdad son 210 €."),
 (21.2, 23.4, "Hoy no. El mes que viene, sin agobios."),
]
f = R.F(R.POP, 50)
src, dst = sys.argv[1], sys.argv[2]
os.makedirs(dst, exist_ok=True)
for name in sorted(os.listdir(src)):
    t = int(name[:4]) / 30
    im = Image.open(f'{src}/{name}').convert('RGB')
    cue = next((c for c in CUES if c[0] <= t < c[1]), None)
    if cue:
        a = R.ease((t - cue[0]) / 0.12) * (1 - R.ease((t - (cue[1] - 0.12)) / 0.12))
        d = ImageDraw.Draw(im, 'RGBA')
        lines = R.wrap(d, cue[2], f, 880)
        lh = 64; h = len(lines) * lh + 36
        y0 = 1500 - h
        w = max(d.textlength(l, font=f) for l in lines) + 60
        d.rounded_rectangle(((1080 - w) / 2, y0, (1080 + w) / 2, y0 + h), 28, fill=(14, 9, 32, int(215 * a)))
        for i, l in enumerate(lines):
            lw = d.textlength(l, font=f)
            d.text(((1080 - lw) / 2, y0 + 14 + i * lh), l, font=f, fill=(255, 255, 255, int(255 * a)))
    im.save(f'{dst}/{name}')

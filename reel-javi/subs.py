import os, sys
sys.path.insert(0, 'work')
from PIL import Image, ImageDraw
import render as R
CUES = [
 (0.3, 2.6, "Mira qué zapatillas. Me encantan."),
 (3.6, 7.1, "Noventa euros. El banco dice que tengo 640 €…"),
 (7.5, 8.9, "¿Pero me las puedo permitir?"),
 (9.2, 12.2, "Así que se lo pregunto a mi IA, que tiene Propera conectado."),
 (14.0, 14.95, "Y me lo dice claro:"),
 (15.2, 19.1, "de esos 640 €, 430 ya están comprometidos."),
 (19.3, 21.45, "Alquiler, luz, gimnasio…"),
 (21.6, 24.1, "Lo que tengo de verdad son 210 €."),
 (24.5, 27.7, "Hoy no. Mejor el mes que viene, sin agobios."),
 (27.9, 31.0, "Propera. Sabe lo que tienes de verdad antes de gastar."),
]
f = R.F(R.POP, 50)
src, dst = sys.argv[1], sys.argv[2]
os.makedirs(dst, exist_ok=True)
for name in sorted(os.listdir(src)):
    k = int(name[:4]); t = k / 30
    im = Image.open(f'{src}/{name}').convert('RGB')
    cue = next((c for c in CUES if c[0] <= t < c[1]), None)
    if cue:
        a = R.ease((t - cue[0]) / 0.15) * (1 - R.ease((t - (cue[1] - 0.15)) / 0.15))
        d = ImageDraw.Draw(im, 'RGBA')
        lines = R.wrap(d, cue[2], f, 900)
        lh = 64; h = len(lines) * lh + 36
        y0 = 1850 - h
        w = max(d.textlength(l, font=f) for l in lines) + 60
        d.rounded_rectangle(((1080 - w) / 2, y0, (1080 + w) / 2, y0 + h), 28, fill=(14, 9, 32, int(200 * a)))
        for i, l in enumerate(lines):
            lw = d.textlength(l, font=f)
            d.text(((1080 - lw) / 2, y0 + 14 + i * lh), l, font=f, fill=(255, 255, 255, int(255 * a)))
    im.save(f'{dst}/{name}')

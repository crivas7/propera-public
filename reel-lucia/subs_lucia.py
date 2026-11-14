import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import render as R
CUES = [
 (4.2, 5.05, "Día veinte."),
 (5.45, 7.9, "El banco dice 640 €…"),
 (8.25, 10.75, "…y tiene un montón de movimientos sin revisar."),
 (11.0, 12.3, "¿Apuntarlos uno a uno?"),
 (12.6, 13.4, "Ni de broma."),
 (13.5, 16.65, "Hace una sola captura del banco y se la pasa a Propera."),
 (17.0, 19.3, "Propera saca todos los movimientos de golpe…"),
 (19.7, 21.1, "…y detecta el Netflix y el gimnasio…"),
 (21.15, 22.5, "…que aún tienen que pasar."),
 (22.6, 24.55, "640 € en el banco…"),
 (24.85, 26.0, "…99 € de verdad."),
 (26.35, 28.2, "Y lo ha resuelto en diez segundos."),
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

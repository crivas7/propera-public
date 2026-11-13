import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import render as R
CUES = [
 (0.2, 3.55, "¿Quieres preguntarle a ChatGPT cuánto dinero tienes de verdad?"),
 (4.0, 5.85, "Te enseño a conectarlo en un minuto."),
 (7.2, 10.6, "Si aún no tienes cuenta, créala gratis en propera.life."),
 (12.15, 16.1, "En ChatGPT, abre el menú, entra en Plugins y busca Propera."),
 (17.45, 20.7, "Pulsa Conectar, entra con tu cuenta de Propera y autoriza."),
 (21.7, 23.0, "Y listo."),
 (23.35, 25.0, "Pregúntale: ¿cuánto tengo disponible de verdad?"),
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

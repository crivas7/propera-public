import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import render as R
W, H, FPS = 1080, 1920, 30
C1 = sorted(os.listdir('work/c1')); C2 = sorted(os.listdir('work/c2'))
def clip(folder, files, t):
    return Image.open(f'{folder}/' + files[min(int(t * FPS), len(files) - 1)]).convert('RGB')

# top dark gradient for white text on clip 1
grad = Image.new('L', (1, H))
for y in range(H):
    grad.putpixel((0, y), int(200 * max(0, 1 - y / 760)))
grad = grad.resize((W, H))
def darken_top(im):
    return Image.composite(Image.new('RGB', (W, H), (10, 6, 24)), im, grad)

DARKTXT = (25, 18, 50); PURP_D = (110, 60, 210)

def s1(t):
    im = darken_top(clip('work/c1', C1, t))
    R.headline(im, [("POV: quieres", R.WHITE), ("estas zapatillas", R.PURPLE)], 170, t, 84)
    return im

def s2(t):
    im = darken_top(clip('work/c1', C1, t + 3.5))
    d = ImageDraw.Draw(im, 'RGBA')
    p = R.ease((t - 0.3) / 0.4)
    if p > 0:
        tw, th = 400, 160; x0 = (W - tw) / 2; y0 = 1470 + (1 - p) * 60
        R.rrect(d, (x0, y0, x0 + tw, y0 + th), 26, fill=(255, 255, 255, int(245 * p)))
        pf = R.F(R.POP, 86); s = "89,99 €"
        d.text(((W - d.textlength(s, font=pf)) / 2, y0 + 22), s, font=pf, fill=DARKTXT + (int(255 * p),))
    R.headline(im, [("El banco dice 640 €…", R.WHITE)], 170, t, 74, start=1.0)
    R.headline(im, [("¿me las puedo permitir?", R.PURPLE)], 270, t, 70, start=2.2)
    return im

def s3(t):
    im = clip('work/c2', C2, t)
    R.headline(im, [("Se lo pregunto a mi IA", DARKTXT), ("con Propera conectado", PURP_D)], 110, t, 62)
    if t > 0.9:
        pin = R.ease((t - 0.9) / 0.5)
        ph = R.phone(R.chat_screen(t - 0.9), 1.08)
        R.paste_phone(im, ph, W / 2, 330 + (1 - pin) * 1300)
    return im

def s4(t):
    im = clip('work/c2', C2, t + 13.0)
    d = ImageDraw.Draw(im, 'RGBA')
    f = R.F(R.POP, 70); l1 = "640 € en el banco."
    p = R.ease(t / 0.45); w = d.textlength(l1, font=f)
    d.text(((W - w) / 2, 110 + (1 - p) * 40), l1, font=f, fill=DARKTXT + (int(255 * p),))
    sp = R.ease((t - 1.0) / 0.5)
    if sp > 0:
        y = 110 + 50
        d.line(((W - w) / 2 - 10, y, (W - w) / 2 - 10 + (w + 20) * sp, y), fill=PURP_D, width=8)
    R.headline(im, [("210 € de verdad.", PURP_D)], 200, t, 70, start=1.4)
    R.paste_phone(im, R.phone(R.propera_screen(max(0, t - 0.3)), 1.08), W / 2, 330)
    return im

R.SCENES[:] = [(0.0, 3.5, s1), (3.5, 8.5, s2), (8.5, 21.5, s3), (21.5, 27.0, s4), (27.0, 31.0, R.s5)]
if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    only = os.environ.get('ONLY')
    ks = range(int(31 * FPS)) if not only else [int(float(x) * FPS) for x in only.split(',')]
    for k in ks:
        R.frame(k / FPS).save(f'{out}/{k:04d}.png')

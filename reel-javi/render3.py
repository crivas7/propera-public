import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import render as R

W, H, FPS = 1080, 1920, 30
DUR = 30.3
P1 = sorted(os.listdir('work/p1')); B1 = sorted(os.listdir('work/b1')); C2 = sorted(os.listdir('work/c2g'))
def fr(folder, files, t):
    return Image.open(f'{folder}/' + files[max(0, min(int(t * FPS), len(files) - 1))]).convert('RGB')

DARKTXT = (25, 18, 50); PURP_D = (110, 60, 210)
S4_SECOND = 3.4

# rounded mask for the store panel
PANEL_Y = 560
_pm = Image.new('L', (1080, 568), 0)
ImageDraw.Draw(_pm).rounded_rectangle((0, 0, 1079, 567), 36, fill=255)

import render2 as R2
C1 = sorted(os.listdir('work/c1g'))
def store(t):
    return R2.darken_top(fr('work/c1g', C1, t))

# ---- scenes ----
def s1(t):  # hook
    im = store(t)
    R.headline(im, [("Mi banco dice 640 €.", R.WHITE)], 260, t, 82, start=0.15)
    R.headline(im, [("Spoiler: no es", R.PURPLE), ("lo que tengo.", R.PURPLE)], 365, t, 82, start=3.1)
    return im

def s2(t):  # price
    T = t + 5.3
    im = store(T)
    d = ImageDraw.Draw(im, 'RGBA')
    p = R.ease((t - 1.1) / 0.35)
    if p > 0:
        tw, th = 420, 170; x0 = (W - tw) / 2; y0 = 1120 + (1 - p) * 50
        sc = 1 + 0.08 * (1 - R.ease((t - 1.1) / 0.5))
        R.rrect(d, (x0, y0, x0 + tw, y0 + th), 28, fill=(255, 255, 255, int(248 * p)))
        pf = R.F(R.POP, int(90 * sc)); s = "89,99 €"
        d.text(((W - d.textlength(s, font=pf)) / 2, y0 + 26), s, font=pf, fill=DARKTXT + (int(255 * p),))
    return im

ZOOM_AT = 6.7
def s3(t):  # chat
    im = fr('work/c2g', C2, t)
    pin = R.ease(t / 0.45)
    z = R.ease((t - ZOOM_AT) / 0.7)
    s = 1.08 + 0.42 * z
    top0 = 150 + (1 - pin) * 1300
    top = top0 * (1 - z) + (760 - 476 * 1.5) * z
    ph = R.phone(R.chat_screen(t), s)
    R.paste_phone(im, ph, W / 2, top)
    return im

def s4(t):  # numbers
    im = fr('work/c2g', C2, t + 7.75)
    R.headline(im, [("210 € para 17 días", DARKTXT)], 120, t, 72, start=0.0)
    R.headline(im, [("De 12 €/día a 7 €/día", PURP_D)], 215, t, 76, start=S4_SECOND)
    R.paste_phone(im, R.phone(R.propera_screen(max(0, t - 0.3)), 1.0), W / 2, 380)
    return im

def s5(t):  # end + CTA
    im = R.END.copy()
    R.headline(im, [("Pruébalo gratis, sin tarjeta", R.WHITE)], 1400, t, 56, start=1.1)
    R.headline(im, [("Link en la bio", R.PURPLE)], 1478, t, 56, start=2.9)
    return im

R.SCENES[:] = [(0.0, 5.3, s1), (5.3, 9.25, s2), (9.25, 17.0, s3), (17.0, 25.9, s4), (25.9, DUR, s5)]

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    only = os.environ.get('ONLY')
    ks = range(int(DUR * FPS)) if not only else [int(float(x) * FPS) for x in only.split(',')]
    for k in ks:
        R.frame(k / FPS).save(f'{out}/{k:04d}.png')

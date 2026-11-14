import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter
import render as R, lucia_screens as L, endcard as EC

W, H, FPS = 1080, 1920, 30
DUR = 29.6
T = dict(A=0.0, B=4.0, C=10.9, E=23.1, F=25.6)
DARKTXT = (25, 18, 50); PURP_D = (110, 60, 210)

def _frames(folder):
    return sorted(os.listdir(folder)) if os.path.isdir(folder) else []
L2 = _frames('work/l2'); L4 = _frames('work/l4')

def placeholder(label):
    im = R.BRAND.copy(); d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = 90, 520, 990, 1420
    for x in range(x0, x1, 56):
        d.line((x, y0, min(x + 28, x1), y0), fill=(120, 95, 180), width=4); d.line((x, y1, min(x + 28, x1), y1), fill=(120, 95, 180), width=4)
    for y in range(y0, y1, 56):
        d.line((x0, y, x0, min(y + 28, y1)), fill=(120, 95, 180), width=4); d.line((x1, y, x1, min(y + 28, y1)), fill=(120, 95, 180), width=4)
    f = R.I("Medium", 34)
    d.text(((W - d.textlength(label, font=f)) / 2, 950), label, font=f, fill=(150, 130, 200))
    return im

def clip(frames, folder, t, label):
    if not frames: return placeholder(label)
    return Image.open(f'{folder}/' + frames[max(0, min(int(t * FPS), len(frames) - 1))]).convert('RGB')

_grad = Image.new('L', (1, H))
for y in range(H): _grad.putpixel((0, y), int(190 * max(0, 1 - y / 700)))
_grad = _grad.resize((W, H))
def darken_top(im):
    return Image.composite(Image.new('RGB', (W, H), (10, 6, 24)), im, _grad)

def soft(im):
    return Image.blend(im.filter(ImageFilter.GaussianBlur(14)), Image.new('RGB', im.size, (14, 9, 32)), 0.45)

def sA(t):  # hook
    im = darken_top(clip(L2, 'work/l2', t, 'CLIP 6608790 · Lucía con el móvil'))
    R.headline(im, [("Lucía odia", R.WHITE), ("apuntar gastos.", R.PURPLE)], 200, t, 84, start=0.15)
    return im

def sB(t):  # bank, problem
    gt = t + T['B']
    im = darken_top(clip(L2, 'work/l2', gt, 'CLIP 6608790 · Lucía con el móvil'))
    R.headline(im, [("Día 20", R.WHITE)], 115, t, 76)
    pin = R.ease((t - 0.8) / 0.45)
    if pin > 0:
        im = Image.blend(im, soft(im), 0.85 * pin)
        R.headline(im, [("Día 20", R.WHITE)], 115, 9, 76)
        R.paste_phone(im, R.phone(L.scr_bank(t - 0.8), 0.95), W / 2, 230 + (1 - pin) * 1200)
    return im

L.CAP.update(tap=3.2, read=3.5, lst=6.1, hl=9.1, conf=10.2)
def sC(t):  # capture with Propera
    gt = min(16.6, 10.9 + t * 0.45)
    im = soft(clip(L2, 'work/l2', gt, 'CLIP 6608790 · Lucía con el móvil'))
    R.headline(im, [("Con Propera", R.PURPLE)], 115, t + 1, 76)
    R.paste_phone(im, R.phone(L.scr_capture2(t), 0.95), W / 2, 230)
    return im

def sE(t):  # payoff, smiling
    im = darken_top(clip(L4, 'work/l4', t + 3.5, 'CLIP 6608792 · Lucía sonriendo'))
    d = ImageDraw.Draw(im, 'RGBA')
    f = R.F(R.POP, 80); l1 = "640 € en el banco."
    p = R.ease((t - 0.0) / 0.3); w = d.textlength(l1, font=f)
    d.text(((W - w) / 2, 170 + (1 - p) * 40), l1, font=f, fill=(255, 255, 255, int(255 * p)))
    sp = R.ease((t - 0.2) / 0.35)
    if sp > 0:
        y = 170 + 58
        d.line(((W - w) / 2 - 10, y, (W - w) / 2 - 10 + (w + 20) * sp, y), fill=R.PURPLE, width=9)
    R.headline(im, [("99 € de verdad.", R.PURPLE)], 280, t, 88, start=0.3)
    return im

def sF(t):
    return EC.endcard(t, cta_at=1.0, link_at=2.8)

R.SCENES[:] = [(T['A'], T['B'], sA), (T['B'], T['C'], sB), (T['C'], T['E'], sC), (T['E'], T['F'], sE), (T['F'], DUR, sF)]

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    only = os.environ.get('ONLY')
    ks = range(int(DUR * FPS)) if not only else [int(float(x) * FPS) for x in only.split(',')]
    for k in ks:
        R.frame(k / FPS).save(f'{out}/{k:04d}.png')

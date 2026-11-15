import numpy as np, scipy.ndimage as nd
from PIL import Image, ImageDraw, ImageFont
g = {}; exec(open('splash.py').read().split("VIOLET = ")[0], g)
MARK = g['MARK']; a = np.array(MARK).astype(float); MH, MW = a.shape[:2]
cy_ = (a[..., 1] > 150) & (a[..., 0] < 120) & (a[..., 3] > 30); ys, xs = np.where(cy_); pcy, pcx = ys.mean(), xs.mean()
wh = (a[..., 3] > 128) & (a[..., 0] > 200); l, n = nd.label(wh); sz = nd.sum(wh, l, range(1, n + 1))
ringid = 1 + [i for i in range(n) if 3000 < sz[i] < 10000][0]
bodyc = wh & (l != ringid)
ECX, ECY = 264.88, 330.18
Y, X = np.mgrid[0:MH, 0:MW]
import cv2
ringm = (l == ringid).astype(np.uint8); pts = cv2.findNonZero(ringm)
hull = np.zeros((MH, MW), np.uint8); cv2.fillPoly(hull, [cv2.convexHull(pts)], 1)
eyezone = hull > 0
ys_, xs_ = np.where(eyezone); EYT, EYB = ys_.min(), ys_.max()
body = a.copy(); body[..., 3] = np.where(a[..., 0] < 200, 0, a[..., 3])
pup = a.copy(); pup[..., 3] = np.where(a[..., 0] < 200, a[..., 3], 0)
BODY = Image.fromarray(body.astype(np.uint8), 'RGBA'); PUP = Image.fromarray(pup.astype(np.uint8), 'RGBA')
BG = (124, 44, 222); W, H = 584, 1266; FPS = 30
POP = ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf', 32)
def ease_out(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def back(x): x = min(max(x, 0), 1); c = 1.9; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
def lid(t, t0=1.30):
    if t0 <= t < t0 + 0.08: return (t - t0) / 0.08
    if t0 + 0.08 <= t < t0 + 0.11: return 1.0
    if t0 + 0.11 <= t < t0 + 0.24: return 1 - ease_out((t - t0 - 0.11) / 0.13)
    return 0.0
hb = 200; bw = round(hb * MW / MH)
for f in range(int(2.4 * FPS)):
    t = f / FPS; layer = Image.new('RGBA', (MW, MH), (0, 0, 0, 0))
    p = ease_out(t / 0.5); s = 0.86 + 0.14 * p
    layer.alpha_composite(BODY)
    q = back((t - 0.45) / 0.35)
    if q > 0.01:
        pw, ph = max(1, round(MW * q)), max(1, round(MH * q))
        layer.alpha_composite(PUP.resize((pw, ph), Image.LANCZOS), (round(pcx - pcx * q), round(pcy - pcy * q)))
    c = lid(t)
    if c > 0:
        edge = EYB - (EYB - EYT + 6) * c
        cover = eyezone & (Y > edge)
        line = eyezone & (np.abs(Y - edge) < 4.5) & (c < 0.97)
        arr = np.array(layer)
        arr[cover] = (0, 0, 0, 0)
        layer = Image.fromarray(arr, 'RGBA')
    h = round(hb * s); w = round(bw * s)
    lay = layer.resize((w, h), Image.LANCZOS); lay.putalpha(lay.getchannel('A').point(lambda v: int(v * p)))
    im = Image.new('RGBA', (W, H), BG + (255,)); im.alpha_composite(lay, ((W - w) // 2 + 3, (H - h) // 2))
    r = ease_out((t - 0.75) / 0.45)
    if r > 0:
        d = ImageDraw.Draw(im, 'RGBA'); txt = 'propera'; tw = d.textlength(txt, font=POP)
        tx = (W - tw) / 2 - 5; ty = H - 150 + (1 - r) * 14; al = int(255 * r)
        d.text((tx, ty), txt, font=POP, fill=(255, 255, 255, al)); d.ellipse((tx + tw + 3, ty + 28, tx + tw + 12, ty + 37), fill=(56, 196, 248, al))
    im.convert('RGB').save(f'anim/{f:03d}.png')
s = Image.new('RGB', (6 * 200, 200))
for i, f in enumerate([38, 40, 41, 42, 44, 47]): s.paste(Image.open(f'anim/{f:03d}.png').crop((192, 533, 392, 733)), (i * 200, 0))
s.save('/tmp/blink.png')

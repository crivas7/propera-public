import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import render as R

W, H = 1080, 1920
_END = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frames', 'end.png')).convert('RGB') \
    if os.path.exists('/home/claude/frames/end.png') else None
if _END is None: _END = Image.open('assets/end.png').convert('RGB')

def _bg():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    g = np.exp(-(((x - 540) / 360) ** 2 + ((y - 880) / 820) ** 2))
    edge = np.array([11, 7, 28], np.float32); cen = np.array([44, 22, 92], np.float32)
    img = edge + (cen - edge) * g[..., None]
    return Image.fromarray(img.clip(0, 255).astype(np.uint8))
BG = _bg()

# logo + wordmark sprite from the brand end frame, feathered so it blends with BG
_SPR_BOX = (390, 400, 690, 800)
SPR = _END.crop(_SPR_BOX)
_m = Image.new('L', SPR.size, 0)
ImageDraw.Draw(_m).ellipse((10, 10, SPR.size[0] - 10, SPR.size[1] - 10), fill=255)
MASK = _m.filter(ImageFilter.GaussianBlur(20))

def endcard(t, cta_at=1.0, link_at=2.8):
    im = BG.copy()
    # logo + wordmark: fade + gentle scale
    p = R.ease((t - 0.0) / 0.6)
    if p > 0:
        sc = 0.9 + 0.1 * p
        spr = SPR.resize((int(SPR.size[0] * sc), int(SPR.size[1] * sc)), Image.LANCZOS)
        mk = MASK.resize(spr.size).point(lambda v: int(v * p))
        x = (W - spr.size[0]) // 2; y = 300 + int((SPR.size[1] - spr.size[1]) / 2) - int(20 * (1 - p))
        im.paste(spr, (x, y), mk)
    d = ImageDraw.Draw(im, 'RGBA')
    wp = R.ease((t - 0.25) / 0.5)
    if wp > 0:
        f = R.F(R.POP, 132); s0 = "propera"
        d.text(((W - d.textlength(s0, font=f)) / 2, 700 + (1 - wp) * 20), s0, font=f, fill=(255, 255, 255, int(255 * wp)))
    # slogan
    q = R.ease((t - 0.5) / 0.5)
    if q > 0:
        f = R.F(R.POPM, 40); s = "Prosperar comienza con orden."
        d.text(((W - d.textlength(s, font=f)) / 2, 880 + (1 - q) * 20), s, font=f, fill=(214, 200, 245, int(255 * q)))
    # CTA button (single message)
    b = R.ease((t - cta_at) / 0.45)
    if b > 0:
        pulse = 1 + 0.025 * max(0, np.sin((t - cta_at - 0.5) * 3.2)) if t > cta_at + 0.5 else 1
        f = R.F(R.POP, 46); s = "Pruébalo gratis · sin tarjeta"
        tw = d.textlength(s, font=f); bw = (tw + 110) * pulse; bh = 108 * pulse
        x0 = (W - bw) / 2; y0 = 1000 + (1 - b) * 30
        glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(glow).rounded_rectangle((x0 - 10, y0 - 6, x0 + bw + 10, y0 + bh + 14), 60, fill=(140, 80, 255, int(110 * b)))
        im.paste(glow.filter(ImageFilter.GaussianBlur(26)), (0, 0), glow.filter(ImageFilter.GaussianBlur(26)))
        d = ImageDraw.Draw(im, 'RGBA')
        d.rounded_rectangle((x0, y0, x0 + bw, y0 + bh), int(bh / 2), fill=(124, 58, 237, int(255 * b)))
        d.text(((W - tw) / 2, y0 + (bh - 62) / 2), s, font=f, fill=(255, 255, 255, int(255 * b)))
    # url + link en la bio
    u = R.ease((t - link_at) / 0.45)
    if u > 0:
        f = R.F(R.POP, 44); s1 = "propera.life"; s2 = "  ·  Link en la bio"
        f2 = R.F(R.POPM, 38)
        w = d.textlength(s1, font=f) + d.textlength(s2, font=f2); x = (W - w) / 2; y = 1180 + (1 - u) * 20
        d.text((x, y), s1, font=f, fill=(56, 189, 248, int(255 * u)))
        d.text((x + d.textlength(s1, font=f), y + 6), s2, font=f2, fill=(200, 190, 235, int(255 * u)))
    return im

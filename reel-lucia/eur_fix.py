"""Sustituye 'EUR' por '€' en capturas de Propera (la producción ya muestra el símbolo)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
INTER = "/usr/share/fonts/opentype/inter/Inter-%s.otf"

def clusters(mask_cols, gap):
    xs = np.where(mask_cols)[0]
    if len(xs) == 0: return []
    out = [[xs[0], xs[0]]]
    for x in xs[1:]:
        if x - out[-1][1] > gap: out.append([x, x])
        else: out[-1][1] = x
    return out

def fix_line(im, box, weight="SemiBold", dark=140, word_gap=9, color=None):
    """box: (x0,y0,x1,y1) region containing one text line ending in 'EUR'."""
    x0, y0, x1, y1 = box
    a = np.asarray(im.crop(box).convert('RGB')).astype(int)
    lum = a.mean(axis=2)
    ink = lum < dark
    rows = np.where(ink.any(axis=1))[0]
    ty0, ty1 = rows.min(), rows.max()                 # text vertical extent
    cl = clusters(ink.any(axis=0), word_gap)
    eur = cl[-1]                                      # last word = EUR
    ex0, ex1 = eur
    # sample text colour & background
    txt = a[ink].reshape(-1, 3)
    tcol = tuple(int(v) for v in np.percentile(txt, 10, axis=0)) if color is None else color
    bg = tuple(int(v) for v in a[ty0:ty1 + 1, ex1 + 4:ex1 + 12].reshape(-1, 3).mean(axis=0)) if ex1 + 12 < a.shape[1] else tuple(int(v) for v in a[0, -1])
    d = ImageDraw.Draw(im)
    d.rectangle((x0 + ex0 - 2, y0 + ty0 - 2, x0 + ex1 + 3, y0 + ty1 + 3), fill=bg)
    cap = ty1 - ty0 + 1                                # cap height of 'EUR'
    # find font size whose '€' ink height == cap
    size = cap
    for s in range(int(cap * 0.8), int(cap * 2.0)):
        f = ImageFont.truetype(INTER % weight, s)
        bb = d.textbbox((0, 0), "€", font=f)
        if bb[3] - bb[1] >= cap: size = s; break
    f = ImageFont.truetype(INTER % weight, size)
    bb = d.textbbox((0, 0), "€", font=f)
    d.text((x0 + ex0 - bb[0], y0 + ty0 - bb[1]), "€", font=f, fill=tcol)
    return (x0 + ex0, y0 + ty0, x0 + ex1, y0 + ty1)

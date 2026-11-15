"""Reel 'Luego lo apunto' (Propera). Clips de Tim Douglas (Pexels), misma actriz.
Uso: python3 work/luego.py <frames_dir>   (escribe PNG por fotograma; el audio se monta aparte)"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import render as R, lucia_screens as L, endcard as EC
import inspect
_src = inspect.getsource(L._home).replace('Hola, Lucía', 'Hola, Sara')
exec(_src, L.__dict__)

W, H, FPS = 1080, 1920, 30
ease = R.ease
# línea de tiempo (se reajusta con la voz vía LUEGO_TL)
T = dict(A=0.0, B=3.6, C=8.0, D=12.0, E=21.5, F=25.0)
DUR = 30.0
CAPS = [  # subtítulos (texto, inicio, fin)
    ("Las tres palabras más caras del mes.", 1.5, 3.5),
    ("Las compras…", 3.7, 4.9), ("la tarjeta…", 5.1, 6.2), ("el taxi…", 6.4, 7.2), ("luego lo apunto.", 7.2, 7.9),
    ("Y a fin de mes, nadie sabe", 8.2, 9.8), ("a dónde se fue el dinero.", 9.8, 11.7),
    ("Ahora no lo apunta:", 12.2, 13.6), ("se lo dice a Propera.", 13.6, 15.2),
    ("Propera prepara el movimiento,", 16.2, 18.0), ("y ella solo confirma.", 18.0, 19.8),
]
if os.environ.get('LUEGO_TL'):
    tl = json.load(open(os.environ['LUEGO_TL'])); T.update(tl['T']); DUR = tl['DUR']; CAPS = [tuple(c) for c in tl['CAPS']]
    VO = tl.get('VO', {})
else:
    VO = {}

def frames(name): return sorted(os.listdir(f'work/lu/{name}'))
FR = {k: frames(k) for k in ('a', 'b1', 'b2', 'b3', 'c', 'd', 'e')}
def clip(name, t, speed=1.0):
    fs = FR[name]; i = max(0, min(int(t * speed * FPS), len(fs) - 1))
    return Image.open(f'work/lu/{name}/{fs[i]}').convert('RGB')

_g = Image.new('L', (1, H))
for y in range(H): _g.putpixel((0, y), int(170 * max(0, 1 - y / 640)))
TOPG = _g.resize((W, H))
def darken_top(im): return Image.composite(Image.new('RGB', (W, H), (10, 6, 24)), im, TOPG)

POP = lambda s: R.F(R.POP, s)
def title(im, lines, y, t, size=84, start=0.0):
    R.headline(im, lines, y, t, size, start=start)

def stamp(im, text, t, x, y, rot=-6):
    """etiqueta tipo sello 'Luego lo apunto' que cae y rebota"""
    k = (t) / 0.28
    if k < 0: return
    s = 1.25 - 0.25 * min(1, ease(min(k, 1)))
    f = POP(int(46 * s)); d0 = ImageDraw.Draw(im)
    tw = d0.textlength(text, font=f); bw, bh = tw + 56, 46 * s + 40
    lay = Image.new('RGBA', (int(bw) + 20, int(bh) + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    a = int(255 * min(1, k * 2))
    d.rounded_rectangle((10, 10, 10 + bw, 10 + bh), 22, fill=(255, 255, 255, a))
    d.text((38, 10 + (bh - 46 * s * 1.25) / 2), text, font=f, fill=(124, 44, 222, a))
    lay = lay.rotate(rot, resample=Image.BICUBIC, expand=True)
    im.paste(lay, (int(x - lay.size[0] / 2), int(y - lay.size[1] / 2)), lay)

# ---------------- pantalla de voz (composer) ----------------
SW, SH = R.SW, R.SH; I = R.I
VOICE = dict(sheet=0.2, tap_mic=0.6, listen=0.8, words=1.0, done=2.0, card=2.3, tap_ok=3.5, ok=3.8)
PH_IN = 1.5   # antes, se la ve sacando el móvil
SAID = "160 € en ropa"
def _mic(d, cx, cy, col, w=2):
    d.rounded_rectangle((cx - 7, cy - 10, cx + 7, cy + 10), 7, outline=col, width=w); d.arc((cx - 12, cy - 2, cx + 12, cy + 18), 0, 180, fill=col, width=w)
def scr_voice(t):
    v = VOICE
    s = Image.new('RGB', (SW, SH), L.LIGHT); d = ImageDraw.Draw(s, 'RGBA')
    L._home(s, d); L._nav(d, s)
    if t < v['sheet']:
        L.tap(d, SW / 2, SH - 78, t, 0.15); return s
    p = ease((t - v['sheet']) / 0.35)
    d.rectangle((0, 0, SW, SH), fill=(10, 8, 25, int(110 * p)))
    grow = ease((t - v['card'] + 0.1) / 0.4) if t >= v['card'] - 0.1 else 0
    sh_h = 470 + 300 * grow; top = SH - sh_h + (1 - p) * sh_h
    R.rrect(d, (0, top, SW, SH + 40), 30, fill=(255, 255, 255))
    d.rounded_rectangle((SW / 2 - 30, top + 12, SW / 2 + 30, top + 18), 3, fill=(210, 208, 220))
    d.text((26, top + 40), "Registrar", font=I("SemiBold", 27), fill=L.DARKTXT)
    d.text((26, top + 80), "Añade un movimiento para revisar.", font=I("Regular", 18), fill=(90, 88, 105))
    cy = top + 122
    listening = v['listen'] <= t < v['done']
    R.rrect(d, (22, cy, SW - 22, cy + 70), 35, fill=(255, 255, 255), outline=(170, 110, 240), width=3)
    d.ellipse((34, cy + 11, 82, cy + 59), fill=(240, 233, 255))
    d.line((48, cy + 35, 68, cy + 35), fill=L.PURP_D, width=3); d.line((58, cy + 25, 58, cy + 45), fill=L.PURP_D, width=3)
    mx = SW - 56
    if listening:
        pul = 1 + 0.12 * np.sin((t - v['listen']) * 9)
        r = 26 * pul; d.ellipse((mx - r, cy + 35 - r, mx + r, cy + 35 + r), fill=(124, 44, 222))
        _mic(d, mx, cy + 33, (255, 255, 255), 3)
    else:
        _mic(d, mx, cy + 33, L.PURP_D)
    n = 0
    if t >= v['words']:
        n = min(len(SAID), int((t - v['words']) / ((v['done'] - 0.3 - v['words']) / len(SAID))) + 1)
    if n:
        d.text((98, cy + 22), SAID[:n], font=I("Medium", 22), fill=L.DARKTXT)
    elif listening:
        d.text((98, cy + 22), "Escuchando…", font=I("Regular", 21), fill=(124, 44, 222))
    else:
        d.text((98, cy + 22), "Cuéntale a Propera qué pasó", font=I("Regular", 21), fill=(110, 105, 130))
    if listening:   # onda de voz
        for i in range(26):
            hh = 6 + 26 * abs(np.sin(t * 7 + i * 0.7)) * (0.4 + 0.6 * abs(np.sin(i * 1.3)))
            x = 60 + i * 16; d.rounded_rectangle((x, cy + 120 - hh / 2, x + 7, cy + 120 + hh / 2), 3, fill=(170, 110, 240))
    L.tap(d, mx, cy + 35, t, v['tap_mic'])
    if t >= v['card']:   # movimiento preparado para revisar
        q = ease((t - v['card']) / 0.4); y0 = cy + 96 + (1 - q) * 40
        d.rectangle((0, cy + 86, SW, SH), fill=(255, 255, 255))
        d.text((26, y0), "Hemos preparado 1 movimiento", font=I("SemiBold", 21), fill=(40, 35, 60, int(255 * q)))
        R.rrect(d, (22, y0 + 40, SW - 22, y0 + 210), 20, fill=(255, 255, 255, int(255 * q)), outline=(225, 220, 240, int(255 * q)), width=2)
        d.text((44, y0 + 58), "Ropa", font=I("SemiBold", 22), fill=(25, 18, 50, int(255 * q)))
        d.text((44, y0 + 92), "−160,00 €", font=I("Bold", 30), fill=(25, 18, 50, int(255 * q)))
        d.text((44, y0 + 136), "Hoy · Gasto", font=I("Regular", 17), fill=(110, 105, 130, int(255 * q)))
        ok = t >= v['ok']
        by = y0 + 232
        R.rrect(d, (22, by, SW - 22, by + 58), 16, fill=(30, 140, 90, int(255 * q)) if ok else (76, 26, 140, int(255 * q)))
        lab = "✓ Registrado" if ok else "Registrar movimiento"
        f = I("SemiBold", 21); d.text(((SW - d.textlength(lab, font=f)) / 2, by + 15), lab, font=f, fill=(255, 255, 255, int(255 * q)))
        L.tap(d, SW / 2, by + 29, t, v['tap_ok'])
    return s

# ---------------- escenas ----------------
def sA(t):
    im = darken_top(clip('a', t))
    title(im, [("Luego lo apunto.", R.WHITE)], 170, t, 92)
    return im
CUTT = [0.0, 1.35, 2.65]
CUTS = [('b1', 'Las compras'), ('b2', 'La tarjeta'), ('b3', 'El taxi')]
def sB(t):
    k = max(i for i, c in enumerate(CUTT) if c <= t); lt = t - CUTT[k]
    name, lab = CUTS[k]
    im = darken_top(clip(name, lt))
    stamp(im, "Luego lo apunto", lt - 0.35, W / 2, 1180, rot=-6 + 4 * k)
    return im
BANK_LUEGO = [("Tienda de ropa · 28/11", "−160,00"), ("Pago con tarjeta · 27/11", "−38,50"), ("Taxi · 26/11", "−14,20"),
              ("Cafetería · 26/11", "−6,80"), ("Compra online · 24/11", "−49,99"), ("Pago con tarjeta · 22/11", "−27,30"),
              ("Taxi · 21/11", "−11,60"), ("Cafetería · 20/11", "−4,90")]
def scr_bank_luego(t):
    s = Image.new("RGB", (SW, SH), (255, 255, 255)); d = ImageDraw.Draw(s, "RGBA")
    R.status_bar(d)
    d.text((32, 84), "Mi banco", font=I("SemiBold", 26), fill=(30, 30, 40))
    R.rrect(d, (20, 136, SW - 20, 300), 24, fill=(30, 60, 120))
    d.text((44, 160), "Saldo disponible", font=I("Regular", 20), fill=(200, 210, 235))
    d.text((44, 196), "212,40 €", font=I("Bold", 56), fill=(255, 255, 255))
    d.text((32, 324), "Movimientos", font=I("SemiBold", 22), fill=(30, 30, 40))
    off = 70 * ease((t - 1.0) / 1.6)              # se desplaza por la lista
    for n, (a, b) in enumerate(BANK_LUEGO):
        y = 368 + n * 64 - off
        if y < 350 or y > SH - 40: continue
        d.text((32, y), a, font=I("Regular", 21), fill=(50, 50, 60))
        d.text((SW - 32 - d.textlength(b + " €", font=I("Medium", 21)), y), b + " €", font=I("Medium", 21), fill=(60, 60, 70))
        d.line((32, y + 44, SW - 32, y + 44), fill=(238, 238, 242), width=2)
    return s
def sC(t):
    im = clip('c', t, speed=0.55)                                  # cámara lenta
    z = 1 + 0.10 * ease(t / 3.3)                                   # zoom suave hacia ella
    cw, ch = W / z, H / z; cx, cy = W * 0.47, H * 0.42
    x0 = min(max(cx - cw / 2, 0), W - cw); y0 = min(max(cy - ch / 2, 0), H - ch)
    im = im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(0.3); im = ImageEnhance.Brightness(im).enhance(0.75)
    im = darken_top(im); d = ImageDraw.Draw(im, 'RGBA')
    p = ease(t / 0.4)
    R.rrect(d, (W / 2 - 120, 150 + (1 - p) * 20, W / 2 + 120, 240 + (1 - p) * 20), 45, fill=(255, 255, 255, int(235 * p)))
    f = POP(52); d.text(((W - d.textlength("Día 30", font=f)) / 2, 160 + (1 - p) * 20), "Día 30", font=f, fill=(124, 44, 222, int(255 * p)))
    q = ease((t - 0.6) / 0.5)                                      # lo que ve en el móvil
    if q > 0:
        ph = R.phone(scr_bank_luego(max(0, t - 0.6)), 0.56)
        R.paste_phone(im, ph, W * 0.73, 470 + (1 - q) * 1500)
    return im

def sD(t):
    raw = clip('d', t, speed=0.9)
    b = ease((t - PH_IN + 0.3) / 0.5)
    if b <= 0: return darken_top(raw)
    bg = Image.blend(raw, Image.blend(raw.filter(ImageFilter.GaussianBlur(12)), Image.new('RGB', raw.size, (14, 9, 32)), 0.35), b)
    q = ease((t - PH_IN) / 0.55)
    R.paste_phone(bg, R.phone(scr_voice(max(0, t - PH_IN)), 1.02), W / 2, 150 + (1 - q) * 1700)
    return bg
def sE(t):
    im = darken_top(clip('e', t))
    title(im, [("Sin escribir.", R.WHITE), ("Sin «luego».", R.PURPLE)], 170, t, 92)
    return im
def sF(t): return EC.endcard(t, cta_at=0.9, link_at=1.8, cta="Pruébalo gratis")

SCENES = [('A', sA), ('B', sB), ('C', sC), ('D', sD), ('E', sE), ('F', sF)]
XF = 0.22
def caption(im, t):
    for txt, a, b in CAPS:
        if a <= t < b:
            d = ImageDraw.Draw(im, 'RGBA'); f = R.F(R.POP, 50)
            lines = R.wrap(d, txt, f, 900); y = 1500 - len(lines) * 66
            for i, ln in enumerate(lines):
                w = d.textlength(ln, font=f); x = (W - w) / 2
                d.rounded_rectangle((x - 22, y + i * 66 - 8, x + w + 22, y + i * 66 + 60), 16, fill=(12, 8, 28, 190))
                d.text((x, y + i * 66), ln, font=f, fill=(255, 255, 255))
def frame(t):
    keys = [k for k, _ in SCENES]
    idx = max(i for i, k in enumerate(keys) if T[k] <= t)
    k, fn = SCENES[idx]; im = fn(t - T[k])
    if idx + 1 < len(SCENES):
        k2, fn2 = SCENES[idx + 1]; dt = T[k2] - t
        if dt < XF: im = Image.blend(fn2(t - T[k2] + XF * 0 if False else 0).convert('RGB'), im, dt / XF) if False else im
    if idx > 0 and t - T[k] < XF:
        kp, fnp = SCENES[idx - 1]; a = (t - T[k]) / XF
        im = Image.blend(fnp(t - T[kp]).convert('RGB'), im.convert('RGB'), a)
    im = im.convert('RGB')
    if k != 'F': caption(im, t)
    return im

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    only = os.environ.get('ONLY')
    ts = [float(x) for x in only.split(',')] if only else [i / FPS for i in range(int(DUR * FPS))]
    for t in ts:
        frame(t).save(f'{out}/{int(round(t * FPS)):04d}.png' if not only else f'{out}/{t:06.2f}.png')

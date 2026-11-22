"""Reel «La ganga» (Black Friday). Voz de la protagonista (ElevenLabs) + textos en pantalla. 1080x1920, 30 fps.

Protagonista: la chica de la sesión de Mikhail Nilov (Pexels) del mismo piso que Marcos. Es un personaje, no una clienta real.
Uso: python3 bf.py WORK_DIR OUT_DIR    (ONLY=1.0,5.2 genera solo esos segundos)
"""
import json, math, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
WORK, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1080, 1920, 30
POP = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
INT = "/usr/share/fonts/opentype/inter/Inter-%s.otf"
_fc = {}
def F(path, size):
    if (path, size) not in _fc: _fc[(path, size)] = ImageFont.truetype(path, size)
    return _fc[(path, size)]
def I(w, s): return F(INT % w, s)
WHITE = (255, 255, 255); PURPLE = (196, 140, 255); PURP_D = (110, 60, 210); INK = (25, 18, 50)
RED = (200, 50, 80); GREEN = (40, 150, 90); NIGHT = (14, 9, 32); GREY = (120, 115, 140)

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def clamp(x): return max(0.0, min(1.0, x))
def eur(v):
    s = f"{abs(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("−" if v < 0 else "") + s + " €"

def _brand():
    bg = Image.new("RGB", (W, H), NIGHT); glow = Image.new("RGB", (W, H), (0, 0, 0))
    ImageDraw.Draw(glow).ellipse((140, 300, 940, 1300), fill=(70, 35, 140))
    return ImageChops.add(bg, glow.filter(ImageFilter.GaussianBlur(220)))
BRAND = _brand()
END = Image.open(os.path.join(HERE, "..", "reel-javi", "assets", "end.png")).convert("RGB")
LOGO = Image.open(os.path.join(HERE, "..", "reel-javi", "assets", "logo_small.png")).convert("RGBA")

_clips = {}
def clip(name, t):
    if name not in _clips: _clips[name] = sorted(os.listdir(f"{WORK}/{name}"))
    fs = _clips[name]
    return Image.open(f"{WORK}/{name}/{fs[max(0, min(int(t * FPS), len(fs) - 1))]}").convert("RGB")

def zoom(im, s, cx=0.5, cy=0.5):
    if s <= 1.0: return im
    w, h = W / s, H / s
    x0 = min(max(cx * W - w / 2, 0), W - w); y0 = min(max(cy * H - h / 2, 0), H - h)
    return im.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((W, H), Image.LANCZOS)

def scrim(im, top=True, h=560, a=160):
    g = Image.new("L", (1, h))
    for y in range(h): g.putpixel((0, y), int(a * (1 - y / h) ** 1.5))
    g = g.resize((W, h)); dark = Image.new("RGB", (W, h), NIGHT)
    if top: im.paste(dark, (0, 0), g)
    else: im.paste(dark, (0, H - h), g.transpose(Image.FLIP_TOP_BOTTOM))

def pill(im, lines, y, t, size=66, start=0.0, alpha=1.0):
    d = ImageDraw.Draw(im, "RGBA"); f = F(POP, size)
    p = ease((t - start) / 0.35) * alpha
    if p <= 0: return
    lh = int(size * 1.22); w = max(d.textlength(s, font=f) for s, _ in lines) + 76; h = len(lines) * lh + 34
    yy = y + (1 - ease((t - start) / 0.35)) * 30
    d.rounded_rectangle(((W - w) / 2, yy, (W + w) / 2, yy + h), 34, fill=NIGHT + (int(220 * p),))
    for i, (s, col) in enumerate(lines):
        d.text(((W - d.textlength(s, font=f)) / 2, yy + 12 + i * lh), s, font=f, fill=col + (int(255 * p),))

def text_lines(im, lines, y, t, size, start=0.0):
    d = ImageDraw.Draw(im, "RGBA"); f = F(POP, size)
    for i, (s, col) in enumerate(lines):
        p = ease((t - start - i * 0.15) / 0.4)
        if p <= 0: continue
        x = (W - d.textlength(s, font=f)) / 2; yy = y + i * int(size * 1.16) + (1 - p) * 30
        d.text((x + 3, yy + 5), s, font=f, fill=(0, 0, 0, int(100 * p))); d.text((x, yy), s, font=f, fill=col + (int(255 * p),))

def card(im, box, a=1.0, r=40):
    x0, y0, x1, y1 = [int(v) for v in box]
    sh = Image.new("RGBA", (x1 - x0 + 120, y1 - y0 + 120), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((60, 75, x1 - x0 + 60, y1 - y0 + 70), r, fill=(0, 0, 0, int(110 * a)))
    sh = sh.filter(ImageFilter.GaussianBlur(28)); im.paste(sh, (x0 - 60, y0 - 60), sh)
    d = ImageDraw.Draw(im, "RGBA"); d.rounded_rectangle(box, r, fill=(255, 255, 255, int(250 * a)))
    return d

def chip_value_pos(label, value, y):
    """Centro de la cifra del contador (destino del «+X €» que vuela desde la etiqueta)."""
    d = ImageDraw.Draw(BRAND.copy()); fl = I("SemiBold", 32); fv = F(POP, 56)
    lw, vw = d.textlength(label, font=fl), d.textlength(value, font=fv); w = lw + vw + 100
    return (W - w) / 2 + 40 + lw + 20 + vw / 2, y + 48

def counter_chip(im, label, value, col, y, a=1.0, scale=1.0):
    d = ImageDraw.Draw(im, "RGBA"); fl = I("SemiBold", int(32 * scale)); fv = F(POP, int(56 * scale))
    y = y - 48 * (scale - 1)
    w = d.textlength(label, font=fl) + d.textlength(value, font=fv) + 100 * scale; h = 96 * scale
    d.rounded_rectangle(((W - w) / 2, y, (W + w) / 2, y + h), h / 2, fill=(255, 255, 255, int(245 * a)))
    x = (W - w) / 2 + 40 * scale
    d.text((x, y + (h - 34 * scale) / 2 - 2), label, font=fl, fill=GREY + (int(255 * a),))
    d.text((x + d.textlength(label, font=fl) + 20 * scale, y + (h - 64 * scale) / 2), value, font=fv, fill=col + (int(255 * a),))

# ---------- datos de la historia ----------
ITEMS = [  # (clip, artículo, precio, antes)
    ("m1", "Chaqueta de punto", 69.99, 129.99),
    ("m2", "Zapatillas", 69.99, 99.99),
    ("m3", "Auriculares", 59.99, 79.99),
    ("m4", "Freidora de aire", 54.99, 64.99),
]
AHORRO = sum(b - a for _, _, a, b in ITEMS)      # 120,00
GASTO = sum(a for _, _, a, _ in ITEMS)          # 254,96
DISP = 180.00                                   # disponible real hasta cobrar

# ---------- escenas ----------
def s_hook(t):
    im = clip("hook", t); scrim(im, True, 620, 170)
    pill(im, [("El Black Friday pasado", WHITE), ("ahorré 120 €.", PURPLE)], 150, t, 74, 0.15)
    return im

def s_montage(t):
    k = max(i for i, a in enumerate(MDS) if t >= a); lt = t - MDS[k]
    name, art, price, before = ITEMS[k]; disc = before - price
    im = clip(name, lt); scrim(im, True, 520, 150); scrim(im, False, 700, 170)
    prev = sum(b - a for _, _, a, b in ITEMS[:k])
    g = ease((lt - FLY1 + 0.05) / 0.3)                       # suma al llegar el «+X €»
    pulse = 1.0 + 0.1 * math.sin(math.pi * clamp((lt - FLY1 + 0.05) / 0.35))
    counter_chip(im, "Ahorro total", eur(prev + disc * g), GREEN, 170, 1.0, pulse)
    p = ease(lt / 0.25); y0 = 1250 + (1 - p) * 40
    d = card(im, (110, y0, W - 110, y0 + 210), p); A = int(255 * p)
    d.text((150, y0 + 30), art, font=F(POP, 50), fill=INK + (A,))
    old = eur(before); fo = I("Medium", 34)
    d.text((150, y0 + 112), old, font=fo, fill=GREY + (A,))
    ow = d.textlength(old, font=fo); d.line((150, y0 + 134, 150 + ow, y0 + 134), fill=GREY + (A,), width=3)
    d.text((150 + ow + 24, y0 + 100), eur(price), font=F(POP, 52), fill=INK + (A,))
    tag = f"−{int(round(before - price))} €"; ft = F(POP, 44); tw = d.textlength(tag, font=ft) + 44
    d.rounded_rectangle((W - 150 - tw, y0 + 32, W - 150, y0 + 100), 34, fill=(225, 245, 232, A))
    d.text((W - 150 - tw + 22, y0 + 38), tag, font=ft, fill=GREEN + (A,))
    if FLY0 <= lt < FLY1 + 0.05:                             # «+60 €» salta de la etiqueta al contador
        u = clamp((lt - FLY0) / (FLY1 - FLY0)); e = u * u * (3 - 2 * u)
        sx, sy = W - 150 - tw / 2, y0 + 66
        ex, ey = chip_value_pos("Ahorro total", eur(prev + disc), 170)
        x = sx + (ex - sx) * e + 90 * math.sin(math.pi * e); y = sy + (ey - sy) * e
        sc = 1.15 - 0.4 * e; a = 1 - clamp((u - 0.8) / 0.2)
        fp = F(POP, int(48 * sc)); s_ = f"+{int(round(disc))} €"; dd = ImageDraw.Draw(im, "RGBA")
        bw = dd.textlength(s_, font=fp) + 40 * sc; bh = 74 * sc
        dd.rounded_rectangle((x - bw / 2, y - bh / 2, x + bw / 2, y + bh / 2), bh / 2, fill=GREEN + (int(250 * a),))
        dd.text((x - bw / 2 + 20 * sc, y - bh / 2 + 6 * sc), s_, font=fp, fill=WHITE + (int(255 * a),))
    return im

def s_haul(t):
    im = clip("haul", t); scrim(im, True, 620, 170)
    counter_chip(im, "Ahorro total", eur(AHORRO), GREEN, 170)   # el contador sigue igual: corte en seco
    pill(im, [("Me sentía", WHITE), ("la reina de las gangas.", PURPLE)], 330, t, 62, 0.4)
    return im

def s_twist(t):
    im = zoom(clip("twist", t), 1.55 + 0.08 * t / 7.0, 0.72, 0.66)
    im = ImageEnhance.Color(im).enhance(0.6); scrim(im, True, 700, 190); scrim(im, False, 1000, 215)
    f = ease((t - TW_FLIP) / 0.4)   # el contador cambia de verde a rojo
    if t < TW_FLIP:
        counter_chip(im, "Ahorro total", eur(AHORRO), GREEN, 170)
    else:
        counter_chip(im, "Gastado", eur(GASTO), RED, 170, 1.0, 1.0 + 0.15 * (1 - f))
    pill(im, [("Hasta que miré el banco.", WHITE)], 300, t, 58, 0.1)
    text_lines(im, [("Supuestamente ahorré 120 €…", WHITE)], 1000, t, 56, TW_TXT1)
    text_lines(im, [("pero en realidad gasté", WHITE)], 1090, t, 56, TW_FLIP)
    text_lines(im, [("254,96 €", (255, 110, 140))], 1160, t, 112, TW_FLIP + 0.25)
    text_lines(im, [("que no tenía planeado gastar.", WHITE)], 1300, t, 52, TW_TXT4)
    return im

def s_fix(t):
    bg = clip("fixbg", t).filter(ImageFilter.GaussianBlur(12))
    im = ImageEnhance.Brightness(bg).enhance(0.38)
    text_lines(im, [("Este año, antes de comprar,", WHITE), ("miro lo que realmente", WHITE), ("puedo gastar.", PURPLE)], 150, t, 60, 0.1)
    # tarjeta de Propera
    p = ease((t - FX_CARD) / 0.35); y0 = 560 + (1 - p) * 40
    if p > 0:
        d = card(im, (110, y0, W - 110, y0 + 250), p); A = int(255 * p)
        lg = LOGO.resize((36, 43)); im.paste(lg, (150, int(y0 + 34)), lg)
        d.text((198, y0 + 30), "propera", font=F(POP, 34), fill=INK + (A,))
        d.text((W - 150 - d.textlength("27 nov", font=I("Regular", 26)), y0 + 38), "27 nov", font=I("Regular", 26), fill=(150, 145, 165, A))
        d.text((150, y0 + 100), "Disponible real hasta cobrar", font=I("Regular", 30), fill=GREY + (A,))
        d.text((146, y0 + 138), eur(DISP), font=I("Bold", 84), fill=PURP_D + (A,))
    # mi lista
    q = ease((t - FX_LIST) / 0.35); y1 = 870 + (1 - q) * 40
    if q > 0:
        d = card(im, (110, y1, W - 110, y1 + 520), q); A = int(255 * q)
        d.text((150, y1 + 30), "Mi lista de Black Friday", font=F(POP, 40), fill=INK + (A,))
        for i, (_, art, price, _) in enumerate(ITEMS):
            yy = y1 + 112 + i * 92; ok = i == 0
            c = ease((t - FX_CHECK - i * FX_STEP) / 0.25)
            col = INK if (ok or c < 1) else (170, 165, 185)
            d.text((150, yy), art, font=I("Medium", 36), fill=col + (A,))
            if c >= 1 and not ok:
                aw = d.textlength(art, font=I("Medium", 36)); d.line((150, yy + 24, 150 + aw, yy + 24), fill=(170, 165, 185, A), width=3)
            pt = eur(price); d.text((W - 230 - d.textlength(pt, font=I("Medium", 36)), yy), pt, font=I("Medium", 36), fill=col + (A,))
            if c > 0:
                cx, cy = W - 175, yy + 22; r = 26
                d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=((225, 245, 232) if ok else (252, 228, 236)) + (int(A * c),))
                mc = (GREEN if ok else RED) + (int(A * c),)
                if ok: d.line((cx - 11, cy + 1, cx - 3, cy + 10, cx + 12, cy - 9), fill=mc, width=5, joint="curve")
                else:
                    d.line((cx - 9, cy - 9, cx + 9, cy + 9), fill=mc, width=5); d.line((cx - 9, cy + 9, cx + 9, cy - 9), fill=mc, width=5)
        r_ = ease((t - FX_MSG) / 0.35)
        if r_ > 0:
            msg = f"Me quedan {eur(DISP - ITEMS[0][2])} hasta cobrar"; fm = I("SemiBold", 32)
            d.rounded_rectangle((150, y1 + 448, W - 150, y1 + 500), 26, fill=(243, 238, 255, int(A * r_)))
            d.text(((W - d.textlength(msg, font=fm)) / 2, y1 + 455), msg, font=fm, fill=PURP_D + (int(A * r_),))
    return im

def s_happy(t):
    im = clip("happy", t); scrim(im, False, 760, 180)
    pill(im, [("Solo la chaqueta.", WHITE), ("Y llego a fin de mes.", PURPLE)], 1300, t, 62, 0.15)
    return im

def s_punch(t):
    im = BRAND.copy()
    text_lines(im, [("Si la ganga no cabe", WHITE), ("en lo que realmente", WHITE), ("puedes gastar,", WHITE)], 640, t, 72, PU_1)
    text_lines(im, [("no es una ganga.", PURPLE)], 930, t, 84, PU_2)
    return im

def s_end(t): return END.copy()

T = json.load(open(os.path.join(HERE, "timeline.json")))
SCENES = [(T["hook"], T["montage"], s_hook), (T["montage"], T["haul"], s_montage), (T["haul"], T["twist"], s_haul),
          (T["twist"], T["fix"], s_twist), (T["fix"], T["happy"], s_fix), (T["happy"], T["punch"], s_happy),
          (T["punch"], T["end"], s_punch), (T["end"], T["DUR"], s_end)]
XF = 0.2
CUT = {T["haul"], T["twist"]}  # en seco: de la caja a abrazar la chaqueta (corte en la acción) y el giro

# tiempos dentro de cada escena (s desde que empieza); timeline.json "beats" los ajusta a la voz
BT = T.get("beats", {})
MDS = BT.get("montage", [0.0, 1.65, 3.3, 4.95])   # entrada de cada compra
FLY0, FLY1 = 0.45, 0.95                            # vuelo del «+X €» hasta el contador
TW_TXT1, TW_FLIP, TW_TXT4 = BT.get("twist", [1.6, 3.6, 5.2])
FX_CARD, FX_LIST, FX_CHECK, FX_STEP, FX_MSG = BT.get("fix", [1.8, 4.2, 4.8, 0.45, 6.3])
PU_1, PU_2 = BT.get("punch", [0.1, 1.6])

def frame(t):
    for i, (a, b, fn) in enumerate(SCENES):
        if a <= t < b or (i == len(SCENES) - 1 and t >= a):
            im = fn(t - a)
            if i > 0 and t - a < XF and a not in CUT:
                pa, pb, pfn = SCENES[i - 1]
                im = Image.blend(pfn(pb - pa - 0.001), im, (t - a) / XF)
            return im

if __name__ == "__main__":
    only = os.environ.get("ONLY")
    ks = range(int(T["DUR"] * FPS)) if not only else [int(float(x) * FPS) for x in only.split(",")]
    for k in ks:
        frame(k / FPS).save(f"{OUT}/{k:04d}.png")

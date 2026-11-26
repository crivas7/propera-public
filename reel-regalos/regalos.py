"""Reel «Los regalos» (Black Friday + Navidad). Voz de la protagonista (ElevenLabs) + textos en pantalla. 1080x1920, 30 fps.

Protagonista: la chica de la sesión navideña de Pexels (clips verticales 6173679–6174040). Es un personaje, no una clienta real.
Uso: python3 regalos.py WORK_DIR OUT_DIR    (ONLY=1.0,5.2 genera solo esos segundos)
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
RED = (200, 50, 80); GREEN = (40, 150, 90); NIGHT = (14, 9, 32); GREY = (120, 115, 140); SOFT_RED = (255, 120, 150)

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
        d.text((x + 3, yy + 5), s, font=f, fill=(0, 0, 0, int(110 * p))); d.text((x, yy), s, font=f, fill=col + (int(255 * p),))

def card(im, box, a=1.0, r=40):
    x0, y0, x1, y1 = [int(v) for v in box]
    sh = Image.new("RGBA", (x1 - x0 + 120, y1 - y0 + 120), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((60, 75, x1 - x0 + 60, y1 - y0 + 70), r, fill=(0, 0, 0, int(110 * a)))
    sh = sh.filter(ImageFilter.GaussianBlur(28)); im.paste(sh, (x0 - 60, y0 - 60), sh)
    d = ImageDraw.Draw(im, "RGBA"); d.rounded_rectangle(box, r, fill=(255, 255, 255, int(250 * a)))
    return d

def counter_chip(im, label, value, col, y, a=1.0, scale=1.0):
    d = ImageDraw.Draw(im, "RGBA"); fl = I("SemiBold", int(32 * scale)); fv = F(POP, int(56 * scale))
    y = y - 48 * (scale - 1)
    w = d.textlength(label, font=fl) + d.textlength(value, font=fv) + 100 * scale; h = 96 * scale
    d.rounded_rectangle(((W - w) / 2, y, (W + w) / 2, y + h), h / 2, fill=(255, 255, 255, int(245 * a)))
    x = (W - w) / 2 + 40 * scale
    d.text((x, y + (h - 34 * scale) / 2 - 2), label, font=fl, fill=GREY + (int(255 * a),))
    d.text((x + d.textlength(label, font=fl) + 20 * scale, y + (h - 64 * scale) / 2), value, font=fv, fill=col + (int(255 * a),))

def check(d, cx, cy, ok, a):
    r = 24
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=((225, 245, 232) if ok else (252, 228, 236)) + (int(a),))
    mc = (GREEN if ok else RED) + (int(a),)
    if ok: d.line((cx - 10, cy + 1, cx - 3, cy + 9, cx + 11, cy - 8), fill=mc, width=5, joint="curve")
    else: d.line((cx - 8, cy - 8, cx + 8, cy + 8), fill=mc, width=5); d.line((cx - 8, cy + 8, cx + 8, cy - 8), fill=mc, width=5)

# ---------- datos de la historia ----------
GIFTS = [("Mamá", 45.00), ("Papá", 39.00), ("Mi hermana", 60.00), ("Amigo invisible", 20.00)]
CAPRICHO = ("Un capricho para mí", 129.00)
ITEMS = GIFTS + [CAPRICHO]
TOTAL = sum(p for _, p in ITEMS)                 # 293,00
REGALOS = sum(p for _, p in GIFTS)               # 164,00
DISP = 210.00                                    # disponible real hasta cobrar (27 nov)

# ---------- escenas ----------
def s_hook(t):
    im = clip("hook", t); scrim(im, True, 640, 175)
    pill(im, [("Hoy es Black Friday:", WHITE), ("día de adelantar", WHITE), ("los regalos de Navidad.", PURPLE)], 150, t, 64, 0.15)
    return im

def s_list(t):
    if t < LI_SWITCH: im = zoom(clip("list1", t), LI_ZOOM[0], LI_ZOOM[1], LI_ZOOM[2])   # plano más cerrado que el gancho; la lista no le tapa la cara
    else: im = clip("list2", t - LI_SWITCH)
    scrim(im, True, 520, 160); scrim(im, False, 1100, 190)
    n_in = [ease((t - s) / 0.3) for s in LI_ITEMS]
    total = sum(p * ease((t - s - 0.15) / 0.35) for (_, p), s in zip(ITEMS, LI_ITEMS))
    pulse = 1.0 + 0.06 * max([math.sin(math.pi * clamp((t - s - 0.15) / 0.35)) for s in LI_ITEMS] + [0])
    counter_chip(im, "Total", eur(total), INK, 170, 1.0, pulse)
    y0 = 1050; d = card(im, (110, y0, W - 110, y0 + 430), 1.0)
    d.text((150, y0 + 30), "Regalos de Navidad", font=F(POP, 40), fill=INK + (255,))
    for i, ((name, p), q) in enumerate(zip(ITEMS, n_in)):
        if q <= 0: continue
        yy = y0 + 104 + i * 62 + (1 - q) * 18; A = int(255 * q); cap = i == len(ITEMS) - 1
        col = PURP_D if cap else INK
        d.text((150, yy), name, font=I("SemiBold" if cap else "Medium", 34), fill=col + (A,))
        pt = eur(p); d.text((W - 150 - d.textlength(pt, font=I("Medium", 34)), yy), pt, font=I("Medium", 34), fill=col + (A,))
    return im

def s_lastyear(t):
    name, lt = ("ly1", t) if t < LY_SWITCH else ("ly2", t - LY_SWITCH)
    im = ImageEnhance.Color(clip(name, lt)).enhance(0.35); im = ImageEnhance.Brightness(im).enhance(0.9)
    scrim(im, True, 520, 170); scrim(im, False, 1100, 235)
    pill(im, [("El año pasado", WHITE)], 170, t, 54, 0.05)
    text_lines(im, [("hice lo mismo…", WHITE)], 1060, t, 62, LY_T1)
    text_lines(im, [("y llegué a enero", WHITE)], 1160, t, 62, LY_T2)
    text_lines(im, [("sin un euro.", SOFT_RED)], 1240, t, 96, LY_T2 + 0.3)
    return im

def s_fix(t):
    bg = clip("fixbg", t).filter(ImageFilter.GaussianBlur(12))
    im = ImageEnhance.Brightness(bg).enhance(0.36)
    text_lines(im, [("Este año, antes de pagar,", WHITE), ("miro lo que realmente", WHITE), ("puedo gastar.", PURPLE)], 150, t, 60, 0.1)
    p = ease((t - FX_CARD) / 0.35); y0 = 540 + (1 - p) * 40
    if p > 0:
        d = card(im, (110, y0, W - 110, y0 + 250), p); A = int(255 * p)
        lg = LOGO.resize((36, 43)); im.paste(lg, (150, int(y0 + 34)), lg)
        d.text((198, y0 + 30), "propera", font=F(POP, 34), fill=INK + (A,))
        d.text((W - 150 - d.textlength("27 nov", font=I("Regular", 26)), y0 + 38), "27 nov", font=I("Regular", 26), fill=(150, 145, 165, A))
        d.text((150, y0 + 100), "Disponible real hasta cobrar", font=I("Regular", 30), fill=GREY + (A,))
        d.text((146, y0 + 138), eur(DISP), font=I("Bold", 84), fill=PURP_D + (A,))
    q = ease((t - FX_LIST) / 0.35); y1 = 850 + (1 - q) * 40
    if q > 0:
        d = card(im, (110, y1, W - 110, y1 + 590), q); A = int(255 * q)
        d.text((150, y1 + 30), "Regalos de Navidad", font=F(POP, 40), fill=INK + (A,))
        for i, (name, pr) in enumerate(ITEMS):
            yy = y1 + 108 + i * 74; cap = i == len(ITEMS) - 1
            c = ease((t - (FX_CAP if cap else FX_CHECK + i * FX_STEP)) / 0.25)
            off = cap and c >= 1
            col = (170, 165, 185) if off else INK
            d.text((150, yy), name, font=I("Medium", 34), fill=col + (A,))
            if off:
                aw = d.textlength(name, font=I("Medium", 34)); d.line((150, yy + 22, 150 + aw, yy + 22), fill=(170, 165, 185, A), width=3)
            pt = eur(pr); d.text((W - 220 - d.textlength(pt, font=I("Medium", 34)), yy), pt, font=I("Medium", 34), fill=col + (A,))
            if c > 0: check(d, W - 168, yy + 20, not cap, A * c)
            if cap and c > 0:  # etiqueta: el capricho espera a las rebajas
                tg = "→ rebajas de enero"; ft = I("SemiBold", 26); tw = d.textlength(tg, font=ft) + 30
                d.rounded_rectangle((150, yy + 50, 150 + tw, yy + 92), 21, fill=(243, 238, 255, int(A * c)))
                d.text((165, yy + 56), tg, font=ft, fill=PURP_D + (int(A * c),))
        r_ = ease((t - FX_MSG) / 0.35)
        if r_ > 0:
            msg = f"Regalos: {eur(REGALOS)} · me quedan {eur(DISP - REGALOS)}"; fm = I("SemiBold", 30)
            d.rounded_rectangle((140, y1 + 508, W - 140, y1 + 562), 27, fill=(225, 245, 232, int(A * r_)))
            d.text(((W - d.textlength(msg, font=fm)) / 2, y1 + 518), msg, font=fm, fill=GREEN + (int(A * r_),))
    return im

def s_happy(t):
    im = clip("happy", t); scrim(im, False, 760, 185)
    pill(im, [("Los mismos regalos.", WHITE), ("Sin cuesta de enero.", PURPLE)], 1290, t, 62, 0.15)
    return im

def s_end(t): return END.copy()

T = json.load(open(os.path.join(HERE, "timeline.json")))
SCENES = [(T["hook"], T["list"], s_hook), (T["list"], T["lastyear"], s_list), (T["lastyear"], T["fix"], s_lastyear),
          (T["fix"], T["happy"], s_fix), (T["happy"], T["end"], s_happy), (T["end"], T["DUR"], s_end)]
XF = 0.2
CUT = {T["lastyear"]}  # «el año pasado» entra en seco

BT = T.get("beats", {})
LI_SWITCH = BT.get("list_switch", 2.6)                       # cambio de plano dentro de la lista (99 = un solo plano)
LI_ZOOM = BT.get("list_zoom", [1.45, 0.5, 0.58])              # zoom, centro x, centro y del plano de la lista
LI_ITEMS = BT.get("list_items", [0.3, 1.1, 1.9, 2.8, 3.9])  # entrada de cada regalo (cuando lo nombra)
LY_SWITCH, LY_T1, LY_T2 = BT.get("lastyear", [1.6, 0.6, 1.9])
FX_CARD, FX_LIST, FX_CHECK, FX_STEP, FX_CAP, FX_MSG = BT.get("fix", [2.3, 4.4, 4.6, 0.3, 6.0, 6.7])

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

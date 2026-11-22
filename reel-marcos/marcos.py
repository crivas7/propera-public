"""Reel «Día 30» (Marcos) v2. Genera los fotogramas 1080x1920 a 30 fps.

Marcos es siempre el mismo actor: una sola sesión de Mikhail Nilov en Pexels (IDs 68980xx-68981xx).
Uso: python3 marcos.py WORK_DIR OUT_DIR   (WORK_DIR con las carpetas de fotogramas que prepara build.sh)
Variables: ONLY=1.0,5.2 genera solo esos segundos. SUBS=1 añade los subtítulos de la voz.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
WORK, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

W, H, FPS = 1080, 1920, 30
POP = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
INT = "/usr/share/fonts/opentype/inter/Inter-%s.otf"
_fc = {}
def F(path, size):
    k = (path, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]
def I(w, s): return F(INT % w, s)

PURPLE = (196, 140, 255); WHITE = (255, 255, 255)
INK = (25, 18, 50); PURP_D = (110, 60, 210); RED = (176, 60, 110); CYAN = (56, 189, 248)
GREEN = (40, 140, 90); NIGHT = (14, 9, 32)

def ease(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def clamp(x): return max(0.0, min(1.0, x))
def rrect(d, box, r, **kw): d.rounded_rectangle(box, r, **kw)

def eur(v, sign=True):
    s = f"{abs(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("−" if v < 0 and sign else "") + s + " €"

# ---------- recursos ----------
def _brand():
    bg = Image.new("RGB", (W, H), NIGHT)
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    ImageDraw.Draw(glow).ellipse((140, 300, 940, 1300), fill=(70, 35, 140))
    return ImageChops.add(bg, glow.filter(ImageFilter.GaussianBlur(220)))
BRAND = _brand()
END = Image.open(os.path.join(HERE, "..", "reel-javi", "assets", "end.png")).convert("RGB")
LOGO_S = Image.open(os.path.join(HERE, "..", "reel-javi", "assets", "logo_small.png")).convert("RGBA")

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

def scrim(im, top=True, h=520, a=150):
    g = Image.new("L", (1, h))
    for y in range(h): g.putpixel((0, y), int(a * (1 - y / h) ** 1.6))
    g = g.resize((W, h))
    dark = Image.new("RGB", (W, h), NIGHT)
    if top: im.paste(dark, (0, 0), g)
    else: im.paste(dark, (0, H - h), g.transpose(Image.FLIP_TOP_BOTTOM))
    return im

# ---------- texto ----------
def headline(im, lines, y, t, size=78, start=0.0):
    d = ImageDraw.Draw(im, "RGBA"); f = F(POP, size)
    for i, (s, col) in enumerate(lines):
        p = ease((t - start - i * 0.12) / 0.45)
        if p <= 0: continue
        w = d.textlength(s, font=f); x = (W - w) / 2
        yy = y + i * int(size * 1.18) + (1 - p) * 40; a = int(255 * p)
        if sum(col) > 450: d.text((x + 3, yy + 4), s, font=f, fill=(0, 0, 0, int(a * 0.35)))
        d.text((x, yy), s, font=f, fill=col + (a,))

def pill(im, lines, y, t, size=64, start=0.0):
    """Titular sobre píldora oscura, para planos de vídeo."""
    d = ImageDraw.Draw(im, "RGBA"); f = F(POP, size)
    p = ease((t - start) / 0.4)
    if p <= 0: return
    lh = int(size * 1.22)
    w = max(d.textlength(s, font=f) for s, _ in lines) + 76
    h = len(lines) * lh + 34
    yy = y + (1 - p) * 30
    rrect(d, ((W - w) / 2, yy, (W + w) / 2, yy + h), 34, fill=NIGHT + (int(215 * p),))
    for i, (s, col) in enumerate(lines):
        d.text(((W - d.textlength(s, font=f)) / 2, yy + 12 + i * lh), s, font=f, fill=col + (int(255 * p),))

def wrap(d, text, font, width):
    out, line = [], ""
    for w in text.split(" "):
        tt = (line + " " + w).strip()
        if d.textlength(tt, font=font) <= width: line = tt
        else: out.append(line); line = w
    out.append(line); return out

# ---------- móvil (pantallas simuladas) ----------
PW, PH, SW, SH = 560, 1160, 528, 1128
def phone(screen, scale=1.0):
    ph = Image.new("RGBA", (PW, PH), (0, 0, 0, 0)); d = ImageDraw.Draw(ph)
    rrect(d, (0, 0, PW - 1, PH - 1), 78, fill=(28, 28, 32), outline=(70, 70, 78), width=3)
    m = Image.new("L", screen.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, SW - 1, SH - 1), 64, fill=255)
    ph.paste(screen, (16, 16), m)
    d.rounded_rectangle((PW / 2 - 64, 30, PW / 2 + 64, 66), 18, fill=(0, 0, 0))
    if scale != 1.0: ph = ph.resize((int(PW * scale), int(PH * scale)), Image.LANCZOS)
    return ph

def paste_shadowed(im, ph, x, y):
    sh = Image.new("RGBA", (ph.size[0] + 160, ph.size[1] + 160), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((80, 100, ph.size[0] + 80, ph.size[1] + 90), 60, fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(40))
    im.paste(sh, (int(x - 80), int(y - 80)), sh)
    im.paste(ph, (int(x), int(y)), ph)

def status_bar(d, c=(20, 20, 25)):
    d.text((44, 28), "9:41", font=I("SemiBold", 24), fill=c)
    for i, h in enumerate([8, 12, 16, 20]): d.rectangle((400 + i * 9, 50 - h, 406 + i * 9, 50), fill=c)
    rrect(d, (450, 34, 488, 52), 5, outline=c, width=2); d.rectangle((454, 38, 480, 48), fill=c)

def propera_header(s, d, sub):
    status_bar(d)
    lg = LOGO_S.resize((40, 48)); s.paste(lg, (28, 74), lg)
    d.text((74, 72), "propera", font=F(POP, 38), fill=INK)
    d.text((76, 124), sub, font=I("Regular", 20), fill=(120, 115, 140))
    d.ellipse((440, 82, 488, 130), fill=(236, 228, 255))
    d.text((457, 92), "M", font=I("SemiBold", 22), fill=PURP_D)

def hero(d, label, value, chip, chip_col):
    rrect(d, (18, 170, SW - 18, 390), 30, fill=(20, 14, 42))
    d.text((44, 196), label, font=I("Regular", 21), fill=(190, 185, 215))
    d.text((42, 232), value, font=I("Bold", 64), fill=CYAN)
    cw = d.textlength(chip, font=I("Medium", 18)) + 56
    rrect(d, (44, 330, 44 + cw, 364), 17, fill=(55, 38, 110))
    d.ellipse((56, 342, 66, 352), fill=chip_col)
    d.text((74, 336), chip, font=I("Medium", 18), fill=WHITE)

def mic(d, cx, cy, active, t=0.0, r0=26):
    if active:
        r = r0 + 4 + 6 * abs(((t * 2.2) % 2) - 1)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(233, 222, 255))
    d.ellipse((cx - r0, cy - r0, cx + r0, cy + r0), fill=PURP_D if active else (240, 232, 255))
    mc = WHITE if active else PURP_D
    rrect(d, (cx - 7, cy - 16, cx + 7, cy + 4), 7, fill=mc)
    d.arc((cx - 13, cy - 10, cx + 13, cy + 12), 0, 180, fill=mc, width=3)
    d.line((cx, cy + 12, cx, cy + 18), fill=mc, width=3)

def composer(d):
    rrect(d, (18, SH - 112, SW - 18, SH - 36), 38, outline=(160, 90, 240), width=3, fill=WHITE)
    mic(d, 62, SH - 74, False)
    d.text((108, SH - 88), "Cuéntale a Propera qué pasó", font=I("Regular", 20), fill=(150, 145, 165))

RES0 = 3.1  # «alquiler» en la voz
FIJOS = [("Alquiler", -650), ("Luz", -55), ("Internet", -30), ("Gimnasio", -35), ("Móvil", -15)]
def day1_screen(t):
    s = Image.new("RGB", (SW, SH), (246, 245, 251)); d = ImageDraw.Draw(s)
    propera_header(s, d, "1 de diciembre · día de cobro")
    n = sum(1 for i in range(len(FIJOS)) if t > RES0 + i * 0.45)
    val = 1400 + sum(v for _, v in FIJOS[:n]); done = n == len(FIJOS)
    hero(d, "Disponible real", eur(val), "Pagos del mes reservados" if done else "Reservando pagos fijos…",
         (120, 220, 150) if done else (160, 150, 200))
    d.text((36, 420), "Reservado el día 1", font=I("SemiBold", 22), fill=INK)
    y = 458
    rrect(d, (18, y, SW - 18, y + 70), 18, fill=WHITE, outline=(230, 228, 238), width=2)
    d.text((44, y + 21), "Nómina", font=I("Regular", 22), fill=(60, 55, 80))
    v = "+1.400,00 €"; d.text((SW - 44 - d.textlength(v, font=I("Medium", 22)), y + 21), v, font=I("Medium", 22), fill=GREEN)
    y += 82
    for i, (a, b) in enumerate(FIJOS):
        pp = ease((t - RES0 - i * 0.45) / 0.3)
        if pp <= 0: continue
        yy = y + (1 - pp) * 20
        rrect(d, (18, yy, SW - 18, yy + 70), 18, fill=WHITE, outline=(230, 228, 238), width=2)
        d.text((44, yy + 21), a, font=I("Regular", 22), fill=(60, 55, 80))
        bt = eur(b); d.text((SW - 44 - d.textlength(bt, font=I("Medium", 22)), yy + 21), bt, font=I("Medium", 22), fill=RED)
        rrect(d, (250, yy + 22, 360, yy + 48), 13, fill=(243, 238, 255))
        d.text((262, yy + 24), "reservado", font=I("Medium", 16), fill=PURP_D)
        y += 82
    composer(d)
    return s

# ---------- tarjetas flotantes sobre vídeo ----------
def card_base(im, box, a=1.0):
    x0, y0, x1, y1 = box
    sh = Image.new("RGBA", (int(x1 - x0) + 120, int(y1 - y0) + 120), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((60, 75, x1 - x0 + 60, y1 - y0 + 70), 40, fill=(0, 0, 0, int(110 * a)))
    sh = sh.filter(ImageFilter.GaussianBlur(28)); im.paste(sh, (int(x0 - 60), int(y0 - 60)), sh)
    d = ImageDraw.Draw(im, "RGBA")
    rrect(d, box, 40, fill=(255, 255, 255, int(248 * a)))
    return d

def bank_card(im, t, y=1290):
    """Notificación de una app de banco genérica (sin marca) el día 30."""
    p = ease((t - 0.7) / 0.4)
    if p <= 0: return
    yy = y + (1 - p) * 60; x0, x1 = 110, W - 110
    d = card_base(im, (x0, yy, x1, yy + 300), p); A = int(255 * p)
    rrect(d, (x0 + 40, yy + 38, x0 + 96, yy + 94), 16, fill=(36, 52, 84, A))
    d.text((x0 + 56, yy + 46), "€", font=I("Bold", 34), fill=(255, 255, 255, A))
    d.text((x0 + 120, yy + 36), "Mi banco", font=I("SemiBold", 34), fill=(30, 40, 60, A))
    d.text((x0 + 120, yy + 78), "Cuenta corriente · 30 nov", font=I("Regular", 26), fill=(120, 125, 140, A))
    q = ease((t - 1.2) / 1.7)
    v = 1400 - (1400 - 12.40) * q
    d.text((x0 + 40, yy + 150), eur(v), font=I("Bold", 92), fill=((200, 40, 60) if q >= 1 else (30, 40, 60)) + (A,))
    d.text((x0 + 44, yy + 252), "Saldo disponible", font=I("Regular", 24), fill=(120, 125, 140, A))

def voice_card(im, t, y=1320):
    p = ease((t - VA) / 0.3)  # aparece con el corte al plano en que dicta
    if p <= 0: return
    yy = y + (1 - p) * 50; x0, x1 = 90, W - 90
    d = card_base(im, (x0, yy, x1, yy + 250), p); A = int(255 * p)
    lg = LOGO_S.resize((34, 41)); im.paste(lg, (x0 + 40, int(yy + 30)), lg)
    d.text((x0 + 86, yy + 28), "propera", font=F(POP, 32), fill=INK + (A,))
    done = t > 5.38
    if not done:
        mic(d, x0 + 76, int(yy + 160), True, t, 34)
        say = "Décimo de lotería, veinte euros"; n = int(clamp((t - 2.85) / 2.15) * len(say))
        d.text((x0 + 140, yy + 112), "Te escucho…", font=I("Regular", 26), fill=(120, 115, 140, A))
        d.text((x0 + 140, yy + 150), say[:n], font=I("SemiBold", 40), fill=INK + (A,))
    else:
        q = ease((t - 5.38) / 0.3)
        d.text((x0 + 40, yy + 100), "Lotería de Navidad", font=I("SemiBold", 44), fill=INK + (A,))
        d.text((x0 + 40, yy + 156), "Efectivo · hoy", font=I("Regular", 26), fill=(120, 115, 140, A))
        v = "−20,00 €"; f = I("Bold", 50)
        d.text((x1 - 40 - d.textlength(v, font=f), yy + 98), v, font=f, fill=RED + (A,))
        ok = "✓ Registrado"; f2 = I("SemiBold", 28)
        w2 = d.textlength(ok, font=f2) + 36
        rrect(d, (x1 - 40 - w2, yy + 168, x1 - 40, yy + 214), 23, fill=(225, 245, 232, int(255 * q)))
        d.text((x1 - 40 - w2 + 18, yy + 174), ok, font=f2, fill=GREEN + (int(255 * q),))
    d.text((x1 - 40 - d.textlength("12 dic", font=I("Regular", 24)), yy + 34), "12 dic", font=I("Regular", 24), fill=(150, 145, 165, A))

def day30_card(im, t, y=1280):
    p = ease((t - 0.3) / 0.4)
    if p <= 0: return
    yy = y + (1 - p) * 60; x0, x1 = 110, W - 110
    d = card_base(im, (x0, yy, x1, yy + 310), p); A = int(255 * p)
    lg = LOGO_S.resize((34, 41)); im.paste(lg, (x0 + 40, int(yy + 30)), lg)
    d.text((x0 + 86, yy + 28), "propera", font=F(POP, 32), fill=INK + (A,))
    d.text((x1 - 40 - d.textlength("30 dic", font=I("Regular", 24)), yy + 34), "30 dic", font=I("Regular", 24), fill=(150, 145, 165, A))
    d.text((x0 + 40, yy + 98), "Disponible real", font=I("Regular", 28), fill=(120, 115, 140, A))
    d.text((x0 + 38, yy + 134), "85,00 €", font=I("Bold", 92), fill=PURP_D + (A,))
    chip = "Cierras el mes en positivo"; f = I("SemiBold", 26)
    w2 = d.textlength(chip, font=f) + 64
    rrect(d, (x0 + 40, yy + 246, x0 + 40 + w2, yy + 290), 22, fill=(225, 245, 232, A))
    d.ellipse((x0 + 58, yy + 262, x0 + 70, yy + 274), fill=(60, 180, 110, A))
    d.text((x0 + 82, yy + 252), chip, font=f, fill=GREEN + (A,))

# ---------- escenas ----------
def s_hook(t):
    im = zoom(clip("hook", t), 1.0 + 0.10 * clamp(t / 4.5), 0.5, 0.42)
    scrim(im, True, 460, 140)
    pill(im, [("POV: es día 30", WHITE)], 120, t, 74, start=0.1)
    bank_card(im, t)
    return im

# Recuerdos: cada gasto cae como una foto sobre un montón y el contador suma lo gastado.
MEM = [  # carpeta, fecha, concepto, importe, giro, recorte vertical (y0 del 3:4)
    ("r1", "28 nov", "Pedido a domicilio", -18.90, -3.0, 250),
    ("r2", "21 nov", "Compra online", -59.90, 2.5, 120),
    ("r3", "15 nov", "Cena a domicilio", -24.50, -2.0, 300),
    ("r4", "9 nov", "Otro pedido", -32.00, 3.0, 280),
]
MEM_T = [0.4, 2.85, 4.15, 4.9]  # entrada de cada recuerdo (s desde el inicio de la escena)
FINAL = 5.45       # remate con el total del mes («y así todo el mes»)
TOTAL = 1400 - 12.40
CW, CH = 720, 960  # foto 3:4

def mem_photo(name, lt, fecha, y0):
    fr = clip(name, lt).crop((0, y0, 1080, y0 + 1440)).resize((CW, CH), Image.LANCZOS)
    fr = ImageEnhance.Color(fr).enhance(0.8)
    warm = Image.new("RGB", fr.size, (255, 190, 120))
    fr = Image.blend(fr, warm, 0.08)
    d = ImageDraw.Draw(fr)
    st = fecha.upper(); f = I("Bold", 40)
    x = CW - 34 - d.textlength(st, font=f)
    d.text((x + 2, 32), st, font=f, fill=(90, 40, 0))
    d.text((x, 30), st, font=f, fill=(255, 160, 50))
    card = Image.new("RGBA", (CW + 36, CH + 36), (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle((0, 0, CW + 35, CH + 35), 26, fill=(250, 248, 244, 255))
    m = Image.new("L", (CW, CH), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, CW - 1, CH - 1), 16, fill=255)
    card.paste(fr, (18, 18), m)
    return card

def place(im, card, cx, cy, rot, scale=1.0, dim=1.0, alpha=1.0):
    if scale != 1.0: card = card.resize((int(card.width * scale), int(card.height * scale)), Image.LANCZOS)
    if dim < 1.0:
        rgb = ImageEnhance.Brightness(card.convert("RGB")).enhance(dim)
        rgb.putalpha(card.getchannel("A")); card = rgb
    card = card.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1.0: card.putalpha(card.getchannel("A").point(lambda v: int(v * alpha)))
    sh = Image.new("RGBA", card.size, (0, 0, 0, 0)); sh.putalpha(card.getchannel("A").point(lambda v: int(v * 0.55)))
    sh = sh.filter(ImageFilter.GaussianBlur(22))
    im.paste(sh, (int(cx - card.width / 2 + 10), int(cy - card.height / 2 + 26)), sh)
    im.paste(card, (int(cx - card.width / 2), int(cy - card.height / 2)), card)

def sticker(im, y0, fecha, que, v, p):
    dd = card_base(im, (110, y0, W - 110, y0 + 150), p); A = int(255 * p)
    dd.text((150, y0 + 28), fecha, font=I("Medium", 30), fill=(120, 115, 140, A))
    dd.text((150, y0 + 68), que, font=F(POP, 46), fill=INK + (A,))
    bt = eur(v); f = F(POP, 54)
    dd.text((W - 150 - dd.textlength(bt, font=f), y0 + 44), bt, font=f, fill=RED + (A,))

def s_rewind(t):
    im = BRAND.copy()
    d = ImageDraw.Draw(im, "RGBA")
    headline(im, [("¿En qué se me ha ido", WHITE), ("el sueldo?", PURPLE)], 90, t, 64)
    # contador de lo gastado
    shown = 0.0
    for i, m in enumerate(MEM):
        shown += -m[3] * ease((t - MEM_T[i] - 0.3) / 0.35)
    fin = ease((t - FINAL - 0.15) / 0.6)
    shown += (TOTAL - sum(-m[3] for m in MEM)) * fin
    lab = "Gastado en noviembre"; fl = I("Medium", 32)
    pa = ease((t - 0.2) / 0.4)
    d.text(((W - d.textlength(lab, font=fl)) / 2, 268), lab, font=fl, fill=(200, 185, 240, int(255 * pa)))
    val = eur(shown); fv = F(POP, 84 + int(16 * fin))
    col = tuple(int(a + (b - a) * fin) for a, b in zip(WHITE, (255, 95, 120)))
    d.text(((W - d.textlength(val, font=fv)) / 2, 306), val, font=fv, fill=col + (int(255 * pa),))
    # montón de fotos
    cur = max([i for i, st in enumerate(MEM_T) if t >= st] or [0])
    pile = 1.0 - 0.5 * fin
    for i, (name, fecha, que, v, rot, y0) in enumerate(MEM):
        st = MEM_T[i]
        if t < st: break
        lt = t - st
        if i < cur or t >= FINAL:
            age = (cur - i) if t < FINAL else (len(MEM) - 1 - i)
            card = mem_photo(name, (MEM_T + [FINAL])[i + 1] - st, fecha, y0)
            place(im, card, 540 - 14 * age, 1000 - 20 * age, rot, 0.96 * (1 - 0.06 * fin), (0.62 if age else 1.0) * pile)
        else:
            p = ease(lt / 0.4)
            card = mem_photo(name, lt, fecha, y0)
            place(im, card, 540 + 460 * (1 - p), 1000 + 60 * (1 - p), rot * p - 8 * (1 - p), 0.96 * (1.12 - 0.12 * p))
            sticker(im, 1418 + 30 * (1 - ease((lt - 0.25) / 0.3)), fecha, que, v, ease((lt - 0.25) / 0.3))
    # remate: el resto del mes
    if t >= FINAL:
        q = ease((t - FINAL) / 0.35)
        pill(im, [("+ alquiler, facturas,", WHITE), ("el Black Friday", WHITE), ("y 36 gastos más", PURPLE)], 840, t - FINAL, 62)
    return im

def s_next(t):
    im = BRAND.copy()
    headline(im, [("Mes siguiente.", WHITE)], 760, t, 96, start=0.1)
    headline(im, [("Día 1.", PURPLE)], 900, t, 96, start=0.7)
    return im

def s_day1(t):
    bg = clip("d1bg", t).filter(ImageFilter.GaussianBlur(10))
    im = ImageEnhance.Brightness(bg).enhance(0.42)
    headline(im, [("Propera reserva", WHITE), ("lo fijo primero", PURPLE)], 110, t, 72)
    pin = ease(t / 0.5)
    paste_shadowed(im, phone(day1_screen(t), 1.0), (W - PW) / 2, 360 + (1 - pin) * 160)
    return im

VA = 2.6   # plano 1: coge el móvil; plano 2 (corte): le dicta el gasto. Todo a velocidad normal
def s_voice(t):
    im = clip("voice_a", t) if t < VA else clip("voice_b", t - VA)
    scrim(im, False, 900, 170)
    pill(im, [("Lo que pago en efectivo,", WHITE), ("se lo digo", PURPLE)], 1010, t, 60)
    voice_card(im, t)
    return im

def s_day30(t):
    im = clip("d30", t)
    scrim(im, False, 900, 170)
    pill(im, [("30 de diciembre:", WHITE), ("sin sustos", PURPLE)], 1040, t, 62)
    day30_card(im, t, 1290)
    return im

def s_end(t): return END.copy()

T = json.load(open(os.path.join(HERE, "timeline.json")))
SCENES = [(T["hook"], T["rewind"], s_hook), (T["rewind"], T["next"], s_rewind), (T["next"], T["day1"], s_next),
          (T["day1"], T["voice"], s_day1), (T["voice"], T["day30"], s_voice), (T["day30"], T["end"], s_day30),
          (T["end"], T["DUR"], s_end)]
XF = 0.2

def subs(im, t):
    cue = next((c for c in T["CAPS"] if c[1] <= t < c[2]), None)
    if not cue: return im
    a = ease((t - cue[1]) / 0.12) * (1 - ease((t - (cue[2] - 0.12)) / 0.12))
    d = ImageDraw.Draw(im, "RGBA"); f = F(POP, 58)
    lines = wrap(d, cue[0], f, 920); lh = 74; h = len(lines) * lh + 30; y0 = 1800 - h
    w = max(d.textlength(l, font=f) for l in lines) + 60
    rrect(d, ((W - w) / 2, y0, (W + w) / 2, y0 + h), 28, fill=NIGHT + (int(215 * a),))
    for i, l in enumerate(lines):
        d.text(((W - d.textlength(l, font=f)) / 2, y0 + 10 + i * lh), l, font=f, fill=(255, 255, 255, int(255 * a)))
    return im

def frame(t):
    for i, (a, b, fn) in enumerate(SCENES):
        if a <= t < b or (i == len(SCENES) - 1 and t >= a):
            im = fn(t - a)
            if i > 0 and t - a < XF:
                pa, pb, pfn = SCENES[i - 1]
                im = Image.blend(pfn(pb - pa - 0.001), im, (t - a) / XF)
            return subs(im, t) if os.environ.get("SUBS") else im

if __name__ == "__main__":
    only = os.environ.get("ONLY")
    ks = range(int(T["DUR"] * FPS)) if not only else [int(float(x) * FPS) for x in only.split(",")]
    for k in ks:
        frame(k / FPS).save(f"{OUT}/{k:04d}.png")

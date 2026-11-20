"""Reel «Día 30» (Marcos). Genera los fotogramas 1080x1920 a 30 fps.

Uso: python3 marcos.py WORK_DIR OUT_DIR
  WORK_DIR debe tener c_movil/%04d.jpg (clip de la mano con el móvil a 1080x1920, 30 fps).
Variables: ONLY=1.0,5.2 genera solo esos segundos (pruebas). SUBS=1 añade subtítulos de la voz.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

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

def ease(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def clamp(x): return max(0.0, min(1.0, x))
def rrect(d, box, r, **kw): d.rounded_rectangle(box, r, **kw)

# ---------- fondos ----------
def _brand():
    bg = Image.new("RGB", (W, H), (14, 9, 32))
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    ImageDraw.Draw(glow).ellipse((140, 300, 940, 1300), fill=(70, 35, 140))
    return ImageChops.add(bg, glow.filter(ImageFilter.GaussianBlur(220)))
BRAND = _brand()
END = Image.open(os.path.join(HERE, "..", "reel-javi", "assets", "end.png")).convert("RGB")
LOGO_S = Image.open(os.path.join(HERE, "..", "reel-javi", "assets", "logo_small.png")).convert("RGBA")

MOV = sorted(os.listdir(f"{WORK}/c_movil"))
def movil(t):
    i = int(t * FPS) % (2 * len(MOV) - 2)  # ida y vuelta si el clip se queda corto
    if i >= len(MOV): i = 2 * len(MOV) - 2 - i
    return Image.open(f"{WORK}/c_movil/{MOV[i]}").convert("RGB")

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

def wrap(d, text, font, width):
    out, line = [], ""
    for w in text.split(" "):
        tt = (line + " " + w).strip()
        if d.textlength(tt, font=font) <= width: line = tt
        else: out.append(line); line = w
    out.append(line); return out

# ---------- móvil ----------
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

def paste_phone(im, ph, cx, top):
    sh = Image.new("RGBA", (ph.size[0] + 160, ph.size[1] + 160), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((80, 100, ph.size[0] + 80, ph.size[1] + 90), 80, fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(40))
    im.paste(sh, (int(cx - ph.size[0] / 2 - 80), int(top - 80)), sh)
    im.paste(ph, (int(cx - ph.size[0] / 2), int(top)), ph)

def status_bar(d, c=(20, 20, 25)):
    d.text((44, 28), "9:41", font=I("SemiBold", 24), fill=c)
    for i, h in enumerate([8, 12, 16, 20]): d.rectangle((400 + i * 9, 50 - h, 406 + i * 9, 50), fill=c)
    rrect(d, (450, 34, 488, 52), 5, outline=c, width=2); d.rectangle((454, 38, 480, 48), fill=c)

def eur(v):
    s = f"{abs(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("−" if v < 0 else "") + s + " €"

# ---------- pantallas ----------
def bank_screen(t):
    """App de banco genérica (sin marca) el día 30."""
    s = Image.new("RGB", (SW, SH), (240, 242, 246)); d = ImageDraw.Draw(s); status_bar(d)
    d.text((36, 84), "Mi banco", font=I("SemiBold", 28), fill=(30, 40, 60))
    rrect(d, (18, 140, SW - 18, 360), 26, fill=(36, 52, 84))
    d.text((44, 166), "Cuenta corriente · 30 nov", font=I("Regular", 20), fill=(190, 200, 220))
    p = ease((t - 0.6) / 1.4)
    v = 1400 - (1400 - 12.40) * p
    d.text((42, 204), eur(v), font=I("Bold", 66), fill=WHITE if p < 1 else (255, 120, 120))
    d.text((44, 300), "Saldo disponible", font=I("Regular", 20), fill=(190, 200, 220))
    d.text((36, 400), "Últimos movimientos", font=I("SemiBold", 22), fill=(30, 40, 60))
    rows = [("Cañas", -24.0), ("Glovo", -18.9), ("Bizum a Dani", -30.0), ("Suscripción", -12.99), ("Tienda de ropa", -59.9)]
    y = 444
    for a, b in rows:
        rrect(d, (18, y, SW - 18, y + 74), 16, fill=WHITE)
        d.text((40, y + 22), a, font=I("Regular", 22), fill=(50, 55, 70))
        bt = eur(b); d.text((SW - 40 - d.textlength(bt, font=I("Medium", 22)), y + 22), bt, font=I("Medium", 22), fill=(60, 60, 70))
        y += 86
    return s

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

def composer(d, text="Cuéntale a Propera qué pasó", active=False, t=0.0):
    rrect(d, (18, SH - 112, SW - 18, SH - 36), 38, outline=(160, 90, 240), width=3, fill=WHITE)
    cx, cy = 62, SH - 74
    if active:
        r = 30 + 6 * abs(((t * 2.2) % 2) - 1)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(233, 222, 255))
    d.ellipse((cx - 26, cy - 26, cx + 26, cy + 26), fill=PURP_D if active else (240, 232, 255))
    mc = WHITE if active else PURP_D  # micrófono
    rrect(d, (cx - 7, cy - 16, cx + 7, cy + 4), 7, fill=mc)
    d.arc((cx - 13, cy - 10, cx + 13, cy + 12), 0, 180, fill=mc, width=3)
    d.line((cx, cy + 12, cx, cy + 18), fill=mc, width=3)
    d.text((108, SH - 88), text, font=I("Regular", 20), fill=(40, 35, 60) if active else (150, 145, 165))

FIJOS = [("Alquiler", -650), ("Luz", -55), ("Internet", -30), ("Gimnasio", -35), ("Móvil", -15)]
def day1_screen(t):
    s = Image.new("RGB", (SW, SH), (246, 245, 251)); d = ImageDraw.Draw(s)
    propera_header(s, d, "1 de diciembre · día de cobro")
    n = sum(1 for i in range(len(FIJOS)) if t > 1.0 + i * 0.45)
    val = 1400 + sum(v for _, v in FIJOS[:n])
    done = n == len(FIJOS)
    hero(d, "Disponible real", eur(val), "Pagos del mes reservados" if done else "Reservando pagos fijos…",
         (120, 220, 150) if done else (160, 150, 200))
    d.text((36, 420), "Reservado el día 1", font=I("SemiBold", 22), fill=INK)
    y = 458
    rrect(d, (18, y, SW - 18, y + 70), 18, fill=WHITE, outline=(230, 228, 238), width=2)
    d.text((44, y + 21), "Nómina", font=I("Regular", 22), fill=(60, 55, 80))
    v = "+1.400,00 €"; d.text((SW - 44 - d.textlength(v, font=I("Medium", 22)), y + 21), v, font=I("Medium", 22), fill=(40, 140, 90))
    y += 82
    for i, (a, b) in enumerate(FIJOS):
        pp = ease((t - 1.0 - i * 0.45) / 0.3)
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

SAY = "Café, dos cincuenta"
def voice_screen(t):
    s = Image.new("RGB", (SW, SH), (246, 245, 251)); d = ImageDraw.Draw(s)
    propera_header(s, d, "12 de diciembre")
    confirmed = t > 3.1
    hero(d, "Disponible real", eur(402.30 - (2.5 if confirmed else 0)), "Al día", (120, 220, 150))
    d.text((36, 420), "Hoy", font=I("SemiBold", 22), fill=INK)
    # tarjeta propuesta
    if t > 1.7:
        p = ease((t - 1.7) / 0.35); y = 460 + (1 - p) * 30
        rrect(d, (18, y, SW - 18, y + 190), 22, fill=WHITE, outline=(200, 175, 255) if not confirmed else (230, 228, 238), width=3)
        d.text((44, y + 22), "Café", font=I("SemiBold", 26), fill=INK)
        d.text((44, y + 60), "Ocio · hoy", font=I("Regular", 19), fill=(120, 115, 140))
        v = "−2,50 €"; d.text((SW - 44 - d.textlength(v, font=I("Bold", 28)), y + 26), v, font=I("Bold", 28), fill=RED)
        if not confirmed:
            pressed = t > 2.8
            rrect(d, (44, y + 112, SW - 44, y + 166), 27, fill=(90, 40, 190) if pressed else PURP_D)
            b = "Confirmar"; d.text(((SW - d.textlength(b, font=I("SemiBold", 22))) / 2, y + 125), b, font=I("SemiBold", 22), fill=WHITE)
        else:
            b = "✓ Registrado"; d.text((44, y + 125), b, font=I("SemiBold", 22), fill=(40, 140, 90))
    listening = 0.3 < t < 1.7
    n = int(clamp((t - 0.5) / 1.0) * len(SAY))
    composer(d, SAY[:n] if listening and n else ("Escuchando…" if listening else "Cuéntale a Propera qué pasó"), listening, t)
    return s

def day30_screen(t):
    s = Image.new("RGB", (SW, SH), (246, 245, 251)); d = ImageDraw.Draw(s)
    propera_header(s, d, "30 de diciembre")
    hero(d, "Disponible real", "85,00 €", "Cierras el mes en positivo", (120, 220, 150))
    d.text((36, 420), "Este mes", font=I("SemiBold", 22), fill=INK)
    rows = [("Nómina", "+1.400,00 €", (40, 140, 90)), ("Pagos fijos", "−785,00 €", RED),
            ("Gastos del día a día", "−530,00 €", RED)]
    y = 458
    for i, (a, b, c) in enumerate(rows):
        pp = ease((t - 0.3 - i * 0.18) / 0.35)
        if pp <= 0: continue
        rrect(d, (18, y, SW - 18, y + 74), 18, fill=WHITE, outline=(230, 228, 238), width=2)
        d.text((44, y + 22), a, font=I("Regular", 22), fill=(60, 55, 80))
        d.text((SW - 44 - d.textlength(b, font=I("Medium", 22)), y + 22), b, font=I("Medium", 22), fill=c)
        y += 88
    composer(d)
    return s

# ---------- escenas ----------
REWIND = [("28 nov", "Cañas", -24.0), ("25 nov", "Glovo", -18.9), ("21 nov", "Bizum a Dani", -30.0),
          ("15 nov", "Suscripción que no uso", -12.99), ("9 nov", "Tienda de ropa", -59.9), ("4 nov", "Cena fuera", -42.0)]

def s_hook(t):
    im = movil(t)
    headline(im, [("POV: es día 30", INK)], 130, t, 84, start=0.1)
    ph = phone(bank_screen(t), 1.0); pin = ease(t / 0.5)
    paste_phone(im, ph, W / 2, 300 + (1 - pin) * 220)
    return im

def s_rewind(t):
    im = BRAND.copy(); d = ImageDraw.Draw(im, "RGBA")
    headline(im, [("¿En qué se me", WHITE), ("ha ido el sueldo?", PURPLE)], 170, t, 78)
    # icono rebobinar
    a = int(200 * ease(t / 0.4))
    for k in range(2):
        x = 460 + k * 70
        d.polygon([(x + 70, 440), (x + 70, 520), (x, 480)], fill=(196, 140, 255, a))
    y = 560
    for i, (fecha, que, v) in enumerate(REWIND):
        p = ease((t - 0.5 - i * 0.55) / 0.3)
        if p <= 0: continue
        x0 = 90 + (1 - p) * -140
        rrect(d, (x0, y, x0 + 900, y + 118), 30, fill=(255, 255, 255, int(235 * p)))
        d.text((x0 + 40, y + 20), fecha, font=I("Medium", 26), fill=(120, 115, 140, int(255 * p)))
        d.text((x0 + 40, y + 56), que, font=F(POP, 38), fill=INK + (int(255 * p),))
        bt = eur(v); f = F(POP, 42)
        d.text((x0 + 860 - d.textlength(bt, font=f), y + 34), bt, font=f, fill=RED + (int(255 * p),))
        y += 128
    return im

def s_next(t):
    im = BRAND.copy()
    headline(im, [("Mes siguiente.", WHITE)], 760, t, 96, start=0.1)
    headline(im, [("Día 1.", PURPLE)], 900, t, 96, start=0.7)
    return im

def s_day1(t):
    im = BRAND.copy()
    headline(im, [("Propera reserva", WHITE), ("lo fijo primero", PURPLE)], 110, t, 72)
    paste_phone(im, phone(day1_screen(t), 1.0), W / 2, 360)
    return im

def s_voice(t):
    im = movil(t + 4)
    headline(im, [("Y cada gasto,", INK), ("se lo digo", PURP_D)], 110, t, 72)
    paste_phone(im, phone(voice_screen(t), 1.0), W / 2, 360)
    return im

def s_day30(t):
    im = BRAND.copy()
    headline(im, [("Día 30:", WHITE), ("sin sustos", PURPLE)], 110, t, 76)
    paste_phone(im, phone(day30_screen(t), 1.0), W / 2, 360)
    return im

def s_end(t):
    return END.copy()

T = json.load(open(os.path.join(HERE, "timeline.json")))
SCENES = [(T["hook"], T["rewind"], s_hook), (T["rewind"], T["next"], s_rewind), (T["next"], T["day1"], s_next),
          (T["day1"], T["voice"], s_day1), (T["voice"], T["day30"], s_voice), (T["day30"], T["end"], s_day30),
          (T["end"], T["DUR"], s_end)]
XF = 0.25

def subs(im, t):
    cue = next((c for c in T["CAPS"] if c[1] <= t < c[2]), None)
    if not cue: return im
    a = ease((t - cue[1]) / 0.12) * (1 - ease((t - (cue[2] - 0.12)) / 0.12))
    d = ImageDraw.Draw(im, "RGBA"); f = F(POP, 54)
    lines = wrap(d, cue[0], f, 900); lh = 70; h = len(lines) * lh + 36; y0 = 1745 - h
    w = max(d.textlength(l, font=f) for l in lines) + 64
    rrect(d, ((W - w) / 2, y0, (W + w) / 2, y0 + h), 30, fill=(14, 9, 32, int(215 * a)))
    for i, l in enumerate(lines):
        d.text(((W - d.textlength(l, font=f)) / 2, y0 + 12 + i * lh), l, font=f, fill=(255, 255, 255, int(255 * a)))
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

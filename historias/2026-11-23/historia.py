"""Historias de Instagram para el lunes 23 de noviembre de 2026 (empieza la semana de Black Friday).

Uso: python3 historia.py  -> historia_a.png, historia_b.png, historia_c.png (1080x1920)
Zona segura de historias: nada importante por encima de y=250 ni por debajo de y=1670 (ahí van la barra y la respuesta).
"""
import os, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
W, H = 1080, 1920
POP = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
INT = "/usr/share/fonts/opentype/inter/Inter-%s.otf"
WHITE = (255, 255, 255); PURPLE = (196, 140, 255); PURP_D = (110, 60, 210); INK = (25, 18, 50)
RED = (176, 60, 110); GREEN = (40, 140, 90); NIGHT = (14, 9, 32); FUCSIA = (236, 72, 153)
LOGO = Image.open(os.path.join(ROOT, "reel-javi", "assets", "logo_small.png")).convert("RGBA")
def P(s): return ImageFont.truetype(POP, s)
def I(w, s): return ImageFont.truetype(INT % w, s)

def brand():
    bg = Image.new("RGB", (W, H), NIGHT)
    glow = Image.new("RGB", (W, H), (0, 0, 0)); g = ImageDraw.Draw(glow)
    g.ellipse((100, 500, 980, 1400), fill=(70, 35, 140)); g.ellipse((600, 1300, 1200, 1900), fill=(60, 20, 70))
    return ImageChops.add(bg, glow.filter(ImageFilter.GaussianBlur(230)))

def center(d, txt, y, font, fill):
    d.text(((W - d.textlength(txt, font=font)) / 2, y), txt, font=font, fill=fill)

def chip(d, txt, y, bg=(55, 38, 110), fg=WHITE, font=None):
    font = font or I("SemiBold", 30); w = d.textlength(txt, font=font) + 64
    d.rounded_rectangle(((W - w) / 2, y, (W + w) / 2, y + 62), 31, fill=bg)
    center(d, txt, y + 13, font, fg)

def lines(d, ls, y, size):
    f = P(size)
    for i, (s, col) in enumerate(ls):
        x = (W - d.textlength(s, font=f)) / 2; yy = y + i * int(size * 1.16)
        d.text((x + 3, yy + 5), s, font=f, fill=(0, 0, 0, 110)); d.text((x, yy), s, font=f, fill=col)

def shadow_box(im, box, r=44, a=130):
    x0, y0, x1, y1 = [int(v) for v in box]
    sh = Image.new("RGBA", (x1 - x0 + 160, y1 - y0 + 160), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((80, 100, x1 - x0 + 80, y1 - y0 + 90), r, fill=(0, 0, 0, a))
    sh = sh.filter(ImageFilter.GaussianBlur(34)); im.paste(sh, (x0 - 80, y0 - 80), sh)

def cta(d, y=1560):
    chip(d, "propera.life", y, bg=PURP_D, font=P(40))

def eur(v):
    s = f"{abs(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("−" if v < 0 else "") + s + " €"

# ---------- A · Antes de comprar ----------
a = brand(); d = ImageDraw.Draw(a, "RGBA")
chip(d, "SEMANA DE BLACK FRIDAY", 270, bg=(236, 72, 153, 60), fg=(255, 200, 230))
lines(d, [("Antes de comprar,", WHITE), ("mira lo que realmente", WHITE), ("puedes gastar.", PURPLE)], 380, 74)
x0, y0, x1, y1 = 110, 720, W - 110, 1250
shadow_box(a, (x0, y0, x1, y1)); d = ImageDraw.Draw(a, "RGBA")
d.rounded_rectangle((x0, y0, x1, y1), 44, fill=(255, 255, 255, 250))
lg = LOGO.resize((40, 48)); a.paste(lg, (x0 + 44, y0 + 40), lg)
d.text((x0 + 96, y0 + 36), "propera", font=P(36), fill=INK)
d.text((x1 - 44 - d.textlength("23 nov", font=I("Regular", 28)), y0 + 44), "23 nov", font=I("Regular", 28), fill=(150, 145, 165))
rows = [("Ingresos del mes", 1400.00, GREEN), ("Ya comprometido", -785.00, RED), ("Gastado hasta hoy", -378.60, RED)]
y = y0 + 130
for lab, v, col in rows:
    d.text((x0 + 44, y), lab, font=I("Regular", 32), fill=(90, 85, 110))
    t = ("+" if v > 0 else "") + eur(v); d.text((x1 - 44 - d.textlength(t, font=I("SemiBold", 32)), y), t, font=I("SemiBold", 32), fill=col)
    y += 62
d.line((x0 + 44, y + 8, x1 - 44, y + 8), fill=(230, 228, 238), width=3)
d.text((x0 + 44, y + 36), "Disponible real", font=I("Medium", 32), fill=(120, 115, 140))
d.text((x0 + 40, y + 78), "236,40 €", font=I("Bold", 104), fill=PURP_D)
lines(d, [("Si el chollo no cabe aquí,", WHITE), ("no es un chollo.", PURPLE)], 1340, 56)
cta(d)
a.save(os.path.join(HERE, "historia_a.png"))

# ---------- B · Encuesta (el sticker se pone a mano en Instagram) ----------
b = brand(); d = ImageDraw.Draw(b, "RGBA")
chip(d, "BLACK FRIDAY · VIERNES 27", 270, bg=(236, 72, 153, 60), fg=(255, 200, 230))
lines(d, [("¿Vas a comprar algo", WHITE), ("este Black Friday?", PURPLE)], 390, 80)
# hueco para la encuesta: 820–1180 (aquí va el sticker de encuesta)
lines(d, [("Antes de responder:", WHITE), ("¿sabes cuánto puedes", WHITE), ("gastar de verdad?", PURPLE)], 1240, 54)
cta(d)
b.save(os.path.join(HERE, "historia_b.png"))

# ---------- C · Adelanto del reel del lunes 30 ----------
with tempfile.TemporaryDirectory() as td:
    p = f"{td}/f.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "2.5", "-i", os.path.join(ROOT, "media", "marcos", "pexels_nilov_6898111.mp4"), "-frames:v", "1", p], check=True)
    c = Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
g = Image.new("L", (1, 1150))
for yy in range(1150): g.putpixel((0, yy), int(240 * min(1, 1.35 * (1 - yy / 1150)) ** 1.2))
c.paste(Image.new("RGB", (W, 1150), NIGHT), (0, 0), g.resize((W, 1150)))
g2 = Image.new("L", (1, 700))
for yy in range(700): g2.putpixel((0, yy), int(200 * (yy / 700) ** 1.5))
c.paste(Image.new("RGB", (W, 700), NIGHT), (0, H - 700), g2.resize((W, 700)))
d = ImageDraw.Draw(c, "RGBA")
chip(d, "EL LUNES 30, EN REELS", 270, bg=(110, 60, 210, 200))
lines(d, [("Día 30.", WHITE), ("Y me quedan…", PURPLE)], 380, 96)
x0, x1, yy0 = 300, W - 300, 1180
shadow_box(c, (x0, yy0, x1, yy0 + 190), 34); d = ImageDraw.Draw(c, "RGBA")
d.rounded_rectangle((x0, yy0, x1, yy0 + 190), 34, fill=(255, 255, 255, 250))
center(d, "Saldo disponible", yy0 + 24, I("Medium", 30), (120, 115, 140))
center(d, "12,40 €", yy0 + 64, P(84), RED)
lines(d, [("¿Te suena?", WHITE)], 1440, 56)
cta(d)
c.save(os.path.join(HERE, "historia_c.png"))
print("ok")

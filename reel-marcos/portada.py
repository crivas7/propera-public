"""Portadas del reel «Día 30» (Marcos), en el estilo de las anteriores (foto a sangre, Poppins Bold blanco/violeta, etiqueta con cifra).

Uso: python3 portada.py   -> portada_a.png, portada_b.png, portada_c.png (1080x1920)
Los textos quedan dentro del centro 3:4 (y 240–1680), que es lo que se ve en la cuadrícula del perfil.
"""
import os, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(HERE, "..", "media", "marcos")
W, H = 1080, 1920
POP = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
INTER = "/usr/share/fonts/opentype/inter/Inter-%s.otf"
WHITE = (255, 255, 255); PURPLE = (196, 140, 255); INK = (25, 18, 50); RED = (176, 60, 110); NIGHT = (14, 9, 32)

def frame(clip, t, cx=None):
    with tempfile.TemporaryDirectory() as td:
        p = f"{td}/f.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", f"{M}/pexels_nilov_{clip}.mp4", "-frames:v", "1", p], check=True)
        im = Image.open(p).convert("RGB")
    if im.width > im.height:  # recorte vertical de un clip 16:9
        w = im.height * 9 / 16; c = cx * im.width / 1920
        im = im.crop((int(c - w / 2), 0, int(c + w / 2), im.height))
    im = im.resize((W, H), Image.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))

def scrim(im, h=900, a=190, top=True):
    g = Image.new("L", (1, h))
    for y in range(h): g.putpixel((0, y), int(a * (1 - y / h) ** 1.5))
    g = g.resize((W, h)); dark = Image.new("RGB", (W, h), NIGHT)
    if top: im.paste(dark, (0, 0), g)
    else: im.paste(dark, (0, H - h), g.transpose(Image.FLIP_TOP_BOTTOM))

def title(im, lines, y, size=96):
    d = ImageDraw.Draw(im, "RGBA"); f = ImageFont.truetype(POP, size)
    for i, (s, col) in enumerate(lines):
        x = (W - d.textlength(s, font=f)) / 2; yy = y + i * int(size * 1.15)
        d.text((x + 3, yy + 5), s, font=f, fill=(0, 0, 0, 110))
        d.text((x, yy), s, font=f, fill=col)

def tag(im, txt, cx, cy, col=INK, label=None, size=78):
    d = ImageDraw.Draw(im, "RGBA"); f = ImageFont.truetype(POP, size)
    w = d.textlength(txt, font=f) + 80; h = size + 56 + (44 if label else 0)
    sh = Image.new("RGBA", (int(w) + 120, int(h) + 120), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((60, 75, w + 60, h + 70), 34, fill=(0, 0, 0, 120))
    sh = sh.filter(ImageFilter.GaussianBlur(26)); im.paste(sh, (int(cx - w / 2 - 60), int(cy - h / 2 - 60)), sh)
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), 34, fill=(255, 255, 255, 250))
    y = cy - h / 2 + 22
    if label:
        fl = ImageFont.truetype(INTER % "Medium", 30)
        d.text((cx - d.textlength(label, font=fl) / 2, y), label, font=fl, fill=(120, 115, 140)); y += 44
    d.text((cx - d.textlength(txt, font=f) / 2, y), txt, font=f, fill=col)

# A · el agobio: día 30 junto a la ventana
a = frame("6898111", 2.5); scrim(a, 1000, 215)
title(a, [("Día 30.", WHITE), ("Y me quedan…", PURPLE)], 300)
tag(a, "12,40 €", W / 2, 1300, RED, "Saldo disponible")
a.save(os.path.join(HERE, "portada_a.png"))

# B · la paz: la sonrisa del día 30
b = frame("6898010", 13.8, 700); scrim(b, 760, 175); scrim(b, 700, 150, top=False)
title(b, [("Día 30", WHITE), ("y sin sustos.", PURPLE)], 300)
tag(b, "85,00 €", W / 2, 1420, (110, 60, 210), "Disponible real")
b.save(os.path.join(HERE, "portada_b.png"))

# C · la pregunta: los pedidos a domicilio
c = frame("6898113", 9.5); scrim(c, 900, 200)
title(c, [("¿En qué se me ha ido", WHITE), ("el sueldo?", PURPLE)], 300, 86)
tag(c, "1.387,60 €", W / 2, 1400, RED, "Gastado en noviembre", 74)
c.save(os.path.join(HERE, "portada_c.png"))
print("ok")

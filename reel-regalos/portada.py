"""Portada del reel «Los regalos». Uso: python3 portada.py -> portada.png (1080x1920). Textos dentro del recorte 3:4 del perfil (y 240–1680)."""
import os, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
POP = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
WHITE = (255, 255, 255); PURPLE = (196, 140, 255); NIGHT = (14, 9, 32)
with tempfile.TemporaryDirectory() as td:
    p = f"{td}/f.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "2.0", "-i", os.path.join(HERE, "..", "media", "regalos", "pexels_xmas_6173883.mp4"), "-frames:v", "1", p], check=True)
    im = Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
g = Image.new("L", (1, 640))
for y in range(640): g.putpixel((0, y), int(225 * (1 - y / 640) ** 1.4))
im.paste(Image.new("RGB", (W, 640), NIGHT), (0, 0), g.resize((W, 640)))
d = ImageDraw.Draw(im, "RGBA")
for i, (s, col, size) in enumerate([("Regalos de Navidad", WHITE, 78), ("en el Black Friday…", PURPLE, 78)]):
    f = ImageFont.truetype(POP, size); x = (W - d.textlength(s, font=f)) / 2; y = 262 + i * 92
    d.text((x + 3, y + 5), s, font=f, fill=(0, 0, 0, 120)); d.text((x, y), s, font=f, fill=col)
txt = "¿y en enero?"; f = ImageFont.truetype(POP, 76); w = d.textlength(txt, font=f) + 90; cx, cy = W / 2, 1520
sh = Image.new("RGBA", (int(w) + 120, 250), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((60, 75, w + 60, 205), 34, fill=(0, 0, 0, 120))
sh = sh.filter(ImageFilter.GaussianBlur(26)); im.paste(sh, (int(cx - w / 2 - 60), int(cy - 125)), sh)
d.rounded_rectangle((cx - w / 2, cy - 65, cx + w / 2, cy + 65), 34, fill=(255, 255, 255, 250))
d.text((cx - d.textlength(txt, font=f) / 2, cy - 54), txt, font=f, fill=(200, 50, 80))
im.save(os.path.join(HERE, "portada.png")); print("ok")

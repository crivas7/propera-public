"""Portada del reel «La ganga» (Black Friday). Uso: python3 portada.py -> portada.png (1080x1920)."""
import os, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
POP = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"; INTER = "/usr/share/fonts/opentype/inter/Inter-%s.otf"
WHITE = (255, 255, 255); PURPLE = (196, 140, 255); NIGHT = (14, 9, 32); GREEN = (40, 150, 90)
with tempfile.TemporaryDirectory() as td:
    p = f"{td}/f.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "15.8", "-i", os.path.join(HERE, "..", "media", "blackfriday", "pexels_nilov_6898098.mp4"), "-frames:v", "1", p], check=True)
    im = Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
g = Image.new("L", (1, 900))
for y in range(900): g.putpixel((0, y), int(210 * (1 - y / 900) ** 1.5))
im.paste(Image.new("RGB", (W, 900), NIGHT), (0, 0), g.resize((W, 900)))
d = ImageDraw.Draw(im, "RGBA")
for i, (s, col, size) in enumerate([("En el Black Friday", WHITE, 84), ("ahorré 120 €…", PURPLE, 96)]):
    f = ImageFont.truetype(POP, size); x = (W - d.textlength(s, font=f)) / 2; y = 300 + i * 104
    d.text((x + 3, y + 5), s, font=f, fill=(0, 0, 0, 110)); d.text((x, y), s, font=f, fill=col)
txt = "¿o no?"; f = ImageFont.truetype(POP, 78); w = d.textlength(txt, font=f) + 90; cx, cy = W / 2, 1380
sh = Image.new("RGBA", (int(w) + 120, 250), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((60, 75, w + 60, 205), 34, fill=(0, 0, 0, 120))
sh = sh.filter(ImageFilter.GaussianBlur(26)); im.paste(sh, (int(cx - w / 2 - 60), int(cy - 125)), sh)
d.rounded_rectangle((cx - w / 2, cy - 65, cx + w / 2, cy + 65), 34, fill=(255, 255, 255, 250))
d.text((cx - d.textlength(txt, font=f) / 2, cy - 56), txt, font=f, fill=(200, 50, 80))
im.save(os.path.join(HERE, "portada.png")); print("ok")

import numpy as np, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
OUT = '/home/claude/out/propera_push'; os.makedirs(OUT, exist_ok=True)
ICON = Image.open('/home/claude/out/icono_propera_final_1024.png').convert('RGB')
MONO = Image.open('/home/claude/out/propera_icono_splash/android/res/mipmap-xxxhdpi/ic_launcher_monochrome.png').convert('RGBA')
MONO = MONO.crop(MONO.getbbox())
LILA = (124, 44, 222)
INT = '/usr/share/fonts/opentype/inter/Inter-%s.otf'
F = lambda w, s: ImageFont.truetype(INT % w, s)
# ---------- icono de estado de Android (blanco sobre transparente, 24dp con 2dp de margen)
def stat_icon(px):
    im = Image.new('RGBA', (px * 4, px * 4), (0, 0, 0, 0)); h = px * 4 * 20 / 24
    m = MONO.resize((round(h * MONO.width / MONO.height), round(h)), Image.LANCZOS)
    im.alpha_composite(m, ((im.width - m.width) // 2, (im.height - m.height) // 2))
    return im.resize((px, px), Image.LANCZOS)
for dn, px in (('mdpi', 24), ('hdpi', 36), ('xhdpi', 48), ('xxhdpi', 72), ('xxxhdpi', 96)):
    p = f'{OUT}/android/res/drawable-{dn}/ic_stat_propera.png'; os.makedirs(os.path.dirname(p), exist_ok=True); stat_icon(px).save(p)
os.makedirs(f'{OUT}/android/res/values', exist_ok=True)
open(f'{OUT}/android/res/values/propera_notifications.xml', 'w').write('''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="notification_accent">#7C2CDE</color>
</resources>
''')
# ---------- maquetas
NOTIFS = [
    ("Nuevo mes, cuentas claras", "Hemos reservado tus pagos planificados de diciembre (540,99 €). Tu disponible real: 99,01 €.", "ahora"),
    ("Mañana se cobra Netflix", "9,99 € · ya estaba reservado, tu disponible real no cambia.", "hace 2 h"),
    ("¿Algo que apuntar hoy?", "Díselo a Propera con la voz y solo tendrás que confirmarlo.", "ayer"),
]
SW, SH = 1170, 2532
def wall():
    y, x = np.mgrid[0:SH, 0:SW] / np.array([SH, SW])[:, None, None]
    c1, c2, c3 = np.array((24, 30, 60)), np.array((80, 58, 128)), np.array((200, 150, 140))
    t = y[..., None]; c = np.where(t < 0.6, c1 + (c2 - c1) * (t / 0.6), c2 + (c3 - c2) * ((t - 0.6) / 0.4))
    return Image.fromarray(np.clip(c, 0, 255).astype(np.uint8))
def rmask(s, r):
    m = Image.new('L', (s * 4, s * 4), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, s * 4 - 1, s * 4 - 1), r * 4, fill=255); return m.resize((s, s), Image.LANCZOS)
def wrap(d, text, font, width):
    out, line = [], ''
    for w in text.split():
        t = (line + ' ' + w).strip()
        if d.textlength(t, font=font) <= width: line = t
        else: out.append(line); line = w
    out.append(line); return out
def glass(s, box, r):
    x0, y0, x1, y1 = map(int, box); reg = s.crop(box).filter(ImageFilter.GaussianBlur(40))
    reg = Image.blend(reg, Image.new('RGB', reg.size, (245, 245, 250)), 0.62)
    s.paste(reg, (x0, y0), rmask(x1 - x0, r).resize((x1 - x0, y1 - y0)) if False else Image.fromarray(np.array(Image.new('L', (x1 - x0, y1 - y0), 0))))
    m = Image.new('L', (x1 - x0, y1 - y0), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, x1 - x0 - 1, y1 - y0 - 1), r, fill=255); s.paste(reg, (x0, y0), m)
def ios():
    s = wall(); d = ImageDraw.Draw(s)
    d.text((SW / 2, 260), "martes, 1 de diciembre", font=F('SemiBold', 50), fill='white', anchor='mm')
    d.text((SW / 2, 470), "9:41", font=F('Bold', 260), fill='white', anchor='mm')
    y = 1180
    for i, (ti, bo, when) in enumerate(NOTIFS):
        f1, f2 = F('SemiBold', 44), F('Regular', 44)
        lines = wrap(d, bo, f2, SW - 2 * 60 - 200)
        h = 70 + 56 + len(lines) * 56 + 40
        glass(s, (40, y, SW - 40, y + h), 56); d = ImageDraw.Draw(s)
        s.paste(ICON.resize((110, 110), Image.LANCZOS), (78, y + (h - 110) // 2), rmask(110, 25))
        d.text((220, y + 36), ti, font=f1, fill=(20, 20, 28))
        d.text((SW - 84, y + 40), when, font=F('Regular', 38), fill=(90, 90, 100), anchor='ra')
        for k, ln in enumerate(lines): d.text((220, y + 36 + 58 + k * 56), ln, font=f2, fill=(30, 30, 40))
        y += h + 22
    return s
def android():
    s = wall(); d = ImageDraw.Draw(s)
    # barra de estado con el icono pequeño
    d.text((70, 60), "9:41", font=F('Medium', 44), fill='white')
    si = stat_icon(48); s.paste(Image.new('RGB', si.size, 'white'), (200, 64), si)
    d.text((SW / 2, 420), "9:41", font=F('Regular', 230), fill='white', anchor='mm')
    d.text((SW / 2, 600), "mar., 1 dic.", font=F('Regular', 50), fill='white', anchor='mm')
    y = 1080
    for i, (ti, bo, when) in enumerate(NOTIFS):
        f1, f2 = F('SemiBold', 44), F('Regular', 42)
        lines = wrap(d, bo, f2, SW - 2 * 60 - 220)
        h = 60 + 50 + 60 + len(lines) * 54 + 40
        d.rounded_rectangle((40, y, SW - 40, y + h), 48, fill=(250, 248, 255)); 
        # cabecera: icono pequeño en el color de acento + "Propera • ahora"
        d.ellipse((76, y + 34, 136, y + 94), fill=LILA)
        si = stat_icon(40); s.paste(Image.new('RGB', si.size, 'white'), (86, y + 44), si)
        d.text((160, y + 44), f"Propera  •  {when}", font=F('Regular', 36), fill=(90, 85, 110))
        d.text((90, y + 120), ti, font=f1, fill=(20, 18, 30))
        for k, ln in enumerate(lines): d.text((90, y + 180 + k * 54), ln, font=f2, fill=(55, 50, 70))
        s.paste(ICON.resize((120, 120), Image.LANCZOS), (SW - 40 - 160, y + 110), rmask(120, 60))   # icono grande opcional
        y += h + 20
    return s
def phone(scr):
    B = 36; Wd, Hd = SW + 2 * B, SH + 2 * B
    ph = Image.new('RGBA', (Wd, Hd), (0, 0, 0, 0)); d = ImageDraw.Draw(ph)
    d.rounded_rectangle((0, 0, Wd - 1, Hd - 1), 200, fill=(22, 22, 26))
    m = Image.new('L', (SW, SH), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, SW - 1, SH - 1), 165, fill=255); ph.paste(scr, (B, B), m)
    return ph
out = Image.new('RGB', (2800, 2900), (236, 234, 242)); d = ImageDraw.Draw(out)
for i, (scr, lab) in enumerate([(ios(), 'iPhone'), (android(), 'Android')]):
    p = phone(scr)
    if lab == 'iPhone': ImageDraw.Draw(p).rounded_rectangle((p.width / 2 - 190, 72, p.width / 2 + 190, 176), 52, fill=(0, 0, 0))
    else: ImageDraw.Draw(p).ellipse((p.width / 2 - 28, 60, p.width / 2 + 28, 116), fill=(0, 0, 0))
    x = 120 + i * 1360; out.paste(p, (x, 50), p); d.text((x + p.width / 2, 2730), lab, font=F('SemiBold', 64), fill=(50, 45, 75), anchor='mt')
out.resize((1400, 1450), Image.LANCZOS).save('/home/claude/out/push_maqueta.png')
# icono de estado ampliado
z = Image.new('RGB', (520, 200), (40, 36, 60)); dz = ImageDraw.Draw(z)
for k, px in enumerate((24, 48, 96)):
    si = stat_icon(px); z.paste(Image.new('RGB', si.size, 'white'), (40 + k * 150, 100 - px // 2), si)
z.save('/tmp/stat.png')

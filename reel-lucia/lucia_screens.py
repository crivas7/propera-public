import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import render as R

SW, SH = R.SW, R.SH
I = R.I
LOGO = R.LOGO_S
DARKTXT = (25, 18, 50); PURP_D = (110, 60, 210); LIGHT = (246, 245, 251)
RED = (176, 60, 110); GREEN = (30, 140, 90)

def tap(d, x, y, t, t0):
    k = (t - t0) / 0.5
    if 0 <= k <= 1:
        r = 18 + 40 * k
        d.ellipse((x - r, y - r, x + r, y + r), outline=(110, 60, 210, int(220 * (1 - k))), width=5)
        d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=(110, 60, 210, int(160 * (1 - k))))

# generic (unbranded) bank app screen
BANK_MOVES = [("Bizum Marta", "−22,00"), ("Glovo", "−14,90"), ("Mercadona", "−43,80"), ("Café", "−3,20"),
              ("Amazon", "−19,99"), ("Gasolinera", "−35,00"), ("Bizum cena", "−18,00"), ("Farmacia", "−9,45"),
              ("Cine", "−8,50"), ("Netflix", "−17,99"), ("Gimnasio", "−25,00"), ("Uber", "−11,30")]
def scr_bank(t):
    s = Image.new("RGB", (SW, SH), (255, 255, 255)); d = ImageDraw.Draw(s, "RGBA")
    R.status_bar(d)
    d.text((32, 84), "Mi banco", font=I("SemiBold", 26), fill=(30, 30, 40))
    R.rrect(d, (20, 136, SW - 20, 300), 24, fill=(30, 60, 120))
    d.text((44, 160), "Saldo disponible", font=I("Regular", 20), fill=(200, 210, 235))
    d.text((44, 196), "640,00 €", font=I("Bold", 56), fill=(255, 255, 255))
    d.text((32, 324), "Movimientos", font=I("SemiBold", 22), fill=(30, 30, 40))
    off = min(1.0, max(0.0, (t - 0.6) / 3.0)) * 260
    y0 = 368 - off
    for n, (a, b) in enumerate(BANK_MOVES * 2):
        y = y0 + n * 64
        if y < 350 or y > SH - 40: continue
        d.text((32, y), a, font=I("Regular", 21), fill=(50, 50, 60))
        d.text((SW - 32 - d.textlength(b + " €", font=I("Medium", 21)), y), b + " €", font=I("Medium", 21), fill=(60, 60, 70))
        d.line((32, y + 44, SW - 32, y + 44), fill=(238, 238, 242), width=2)
    return s

DETECT = [("Bizum Marta", "−22,00 €", None), ("Glovo", "−14,90 €", None), ("Mercadona", "−43,80 €", None),
          ("Amazon", "−19,99 €", None), ("Gasolinera", "−35,00 €", None), ("Bizum cena", "−18,00 €", None),
          ("Netflix", "−17,99 €", "Se repite · próximo cobro el día 28"), ("Gimnasio", "−25,00 €", "Se repite · próximo cobro el día 28")]
CAP = dict(tap=0.5, read=0.9, lst=2.0, hl=3.6, conf=4.3)
def scr_capture(t):
    """0..0.6 empty upload; 0.6 tap; 0.9..2.0 reading; 2.0.. list appears; planned highlighted ~3.6"""
    s = Image.new("RGB", (SW, SH), LIGHT); d = ImageDraw.Draw(s, "RGBA")
    R.status_bar(d)
    s.paste(LOGO.resize((40, 48)), (28, 74))
    d.text((74, 72), "propera", font=R.F(R.POP, 38), fill=DARKTXT)
    d.text((32, 146), "Entrada inteligente", font=I("SemiBold", 25), fill=DARKTXT)
    R.rrect(d, (24, 190, SW - 24, 300), 22, fill=(255, 255, 255), outline=(200, 180, 245), width=3)
    c = CAP
    if t < c['read']:
        lb = "Subir captura del banco"
        d.text(((SW - d.textlength(lb, font=I("Medium", 23))) / 2, 230), lb, font=I("Medium", 23), fill=PURP_D)
        tap(d, SW / 2, 245, t, c['tap'])
    else:
        R.rrect(d, (42, 204, 112, 286), 8, fill=(225, 230, 240))
        for k in range(4):
            d.rectangle((52, 218 + k * 16, 102 - (k % 2) * 16, 224 + k * 16), fill=(170, 178, 195))
        prog = R.ease((t - c['read']) / 1.0)
        d.text((132, 214), "captura_banco.png", font=I("Medium", 21), fill=(60, 55, 80))
        R.rrect(d, (132, 252, SW - 44, 262), 5, fill=(235, 230, 245))
        R.rrect(d, (132, 252, 132 + (SW - 176) * prog, 262), 5, fill=PURP_D)
        lab = "Leyendo movimientos…" if prog < 1 else "8 movimientos detectados"
        d.text((132, 270), lab, font=I("Regular", 17), fill=(120, 115, 140))
    y = 320
    for n, (a, b, tag) in enumerate(DETECT):
        p = R.ease((t - c['lst'] - n * 0.12) / 0.3)
        if p <= 0: continue
        hl = tag and t > c['hl']
        yy = y + (1 - p) * 16
        R.rrect(d, (24, yy, SW - 24, yy + 72), 16, fill=(243, 236, 255) if hl else (255, 255, 255),
                outline=(190, 160, 245) if hl else (230, 228, 238), width=3 if hl else 2)
        d.ellipse((40, yy + 22, 66, yy + 48), fill=(233, 222, 255))
        d.text((46, yy + 21), "✓", font=I("Bold", 19), fill=PURP_D)
        d.text((80, yy + (12 if tag else 22)), a, font=I("Regular", 21), fill=(60, 55, 80))
        if tag:
            d.text((80, yy + 40), tag, font=I("SemiBold", 16), fill=PURP_D)
        d.text((SW - 44 - d.textlength(b, font=I("Medium", 21)), yy + 22), b, font=I("Medium", 21), fill=RED)
        y += 80
    if t > c['conf']:
        p = R.ease((t - c['conf']) / 0.3)
        R.rrect(d, (24, SH - 110, SW - 24, SH - 40), 35, fill=PURP_D + (int(255 * p),))
        lb = "Confirmar todo"
        d.text(((SW - d.textlength(lb, font=I("SemiBold", 24))) / 2, SH - 90), lb, font=I("SemiBold", 24), fill=(255, 255, 255, int(255 * p)))
        tap(d, SW / 2, SH - 75, t, c['conf'] + 0.7)
    return s

def scr_available(t):
    s = Image.new("RGB", (SW, SH), LIGHT); d = ImageDraw.Draw(s)
    R.status_bar(d)
    s.paste(LOGO.resize((40, 48)), (28, 74))
    d.text((74, 72), "propera", font=R.F(R.POP, 38), fill=DARKTXT)
    d.text((76, 124), "Tu situación hoy", font=I("Regular", 20), fill=(120, 115, 140))
    R.rrect(d, (18, 170, SW - 18, 390), 30, fill=(20, 14, 42))
    d.text((44, 196), "Disponible real", font=I("Regular", 21), fill=(190, 185, 215))
    p = R.ease((t - 0.5) / 1.6)
    val = 640.00 - (640.00 - 99.01) * p
    txt = f"{val:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")
    d.text((42, 232), txt, font=I("Bold", 64), fill=(56, 189, 248))
    rows = [("Dinero actual", "640,00 €", DARKTXT), ("Alquiler", "−450,00 €", RED), ("Luz", "−48,00 €", RED),
            ("Gimnasio", "−25,00 €", RED), ("Netflix", "−17,99 €", RED)]
    d.text((36, 420), "Así se calcula", font=I("SemiBold", 22), fill=DARKTXT)
    y = 460
    for n, (a, b, c) in enumerate(rows):
        pp = R.ease((t - 0.2 - n * 0.15) / 0.3)
        if pp <= 0: continue
        R.rrect(d, (18, y, SW - 18, y + 70), 16, fill=(255, 255, 255), outline=(230, 228, 238), width=2)
        d.text((44, y + 21), a, font=I("Regular", 21), fill=(60, 55, 80))
        d.text((SW - 44 - d.textlength(b, font=I("Medium", 21)), y + 21), b, font=I("Medium", 21), fill=c)
        y += 80
    if t > 2.2:
        R.rrect(d, (18, y + 6, SW - 18, y + 90), 22, fill=(238, 230, 255))
        d.text((44, y + 33), "Disponible real", font=I("SemiBold", 23), fill=PURP_D)
        v = "99,01 €"
        d.text((SW - 44 - d.textlength(v, font=I("Bold", 27)), y + 29), v, font=I("Bold", 27), fill=(90, 40, 190))
    return s

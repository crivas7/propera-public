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
          ("Netflix", "−17,99 €", "Pago planificado detectado ✓"), ("Gimnasio", "−25,00 €", "Pago planificado detectado ✓")]
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

# ---------------- real composer flow ----------------
CAP2 = dict(tap_reg=1.2, sheet=1.6, tap_plus=2.5, opts=2.9, tap_img=3.9, read=4.4, lst=6.1, hl=6.9, conf=7.7, pend=8.5)
NAV = [("Inicio", "home"), ("Movimientos", "mov"), ("Registrar", "plus"), ("Pagos", "cal"), ("Ahorros", "wallet")]
def _nav(d, s, active="Inicio"):
    y0 = SH - 118
    d.rectangle((0, y0, SW, SH), fill=(255, 255, 255)); d.line((0, y0, SW, y0), fill=(235, 233, 242), width=2)
    n = len(NAV); cw = SW / n
    for k, (lab, ic) in enumerate(NAV):
        cx = cw * k + cw / 2; cy = y0 + 40
        col = PURP_D if lab == active else (70, 70, 85)
        if ic == "plus":
            R.rrect(d, (cx - 26, cy - 26, cx + 26, cy + 26), 14, fill=(120, 60, 220))
            d.line((cx - 11, cy, cx + 11, cy), fill=(255, 255, 255), width=4); d.line((cx, cy - 11, cx, cy + 11), fill=(255, 255, 255), width=4)
        else:
            if lab == active: R.rrect(d, (cx - 24, cy - 22, cx + 24, cy + 22), 12, fill=(240, 233, 255))
            if ic == "home":
                d.polygon([(cx - 11, cy - 1), (cx, cy - 11), (cx + 11, cy - 1)], outline=col); d.rectangle((cx - 8, cy - 1, cx + 8, cy + 10), outline=col, width=2)
            elif ic == "mov":
                d.line((cx - 5, cy - 10, cx - 5, cy + 10), fill=col, width=2); d.line((cx + 5, cy - 10, cx + 5, cy + 10), fill=col, width=2)
                d.polygon([(cx - 9, cy - 5), (cx - 5, cy - 11), (cx - 1, cy - 5)], fill=col); d.polygon([(cx + 1, cy + 5), (cx + 5, cy + 11), (cx + 9, cy + 5)], fill=col)
            elif ic == "cal":
                d.rounded_rectangle((cx - 10, cy - 9, cx + 10, cy + 10), 3, outline=col, width=2); d.line((cx - 10, cy - 3, cx + 10, cy - 3), fill=col, width=2)
            else:
                d.rounded_rectangle((cx - 11, cy - 8, cx + 11, cy + 9), 3, outline=col, width=2); d.rectangle((cx + 3, cy - 2, cx + 11, cy + 4), outline=col, width=2)
        f = I("Medium" if lab == active else "Regular", 15)
        d.text((cx - d.textlength(lab, font=f) / 2, y0 + 74), lab, font=f, fill=col)

def _home(s, d):
    R.status_bar(d)
    s.paste(LOGO.resize((40, 48)), (28, 74))
    d.text((74, 72), "propera", font=R.F(R.POP, 38), fill=DARKTXT)
    d.text((32, 150), "Hola, Lucía", font=I("SemiBold", 28), fill=DARKTXT)
    R.rrect(d, (20, 200, SW - 20, 360), 26, fill=(20, 14, 42))
    d.text((44, 224), "Disponible real", font=I("Regular", 20), fill=(190, 185, 215))
    d.text((44, 258), "Sin actualizar", font=I("Bold", 40), fill=(150, 145, 175))
    d.text((44, 316), "Último movimiento: hace 12 días", font=I("Regular", 18), fill=(150, 145, 175))
    R.rrect(d, (20, 384, SW - 20, 470), 20, fill=(255, 255, 255), outline=(230, 228, 238), width=2)
    d.text((44, 412), "Tienes movimientos sin revisar", font=I("Medium", 21), fill=(60, 55, 80))

def _composer(d, y, active=False):
    R.rrect(d, (22, y, SW - 22, y + 70), 35, fill=(255, 255, 255), outline=(170, 110, 240), width=3)
    d.ellipse((34, y + 11, 82, y + 59), fill=(240, 233, 255))
    d.line((48, y + 35, 68, y + 35), fill=PURP_D, width=3); d.line((58, y + 25, 58, y + 45), fill=PURP_D, width=3)
    d.text((98, y + 22), "Cuéntale a Propera qué pasó", font=I("Regular", 21), fill=(110, 105, 130))
    mx = SW - 56
    d.rounded_rectangle((mx - 7, y + 20, mx + 7, y + 40), 7, outline=PURP_D, width=2); d.arc((mx - 12, y + 28, mx + 12, y + 48), 0, 180, fill=PURP_D, width=2)
    d.text((26, y + 82), "Por texto o voz, un movimiento cada vez.", font=I("Regular", 16), fill=(90, 88, 105))

def _options(d, y, t_hl=None):
    R.rrect(d, (22, y, SW - 22, y + 300), 22, fill=(255, 255, 255), outline=(230, 228, 238), width=2)
    d.text((44, y + 18), "CAPTURA", font=I("SemiBold", 15), fill=(110, 105, 130))
    bw = (SW - 44 - 16 - 36) / 2
    def btn(x, yy, label, hl=False, pink=False):
        R.rrect(d, (x, yy, x + bw, yy + 58), 14, fill=(240, 233, 255) if hl else (255, 255, 255), outline=(230, 228, 238), width=2)
        d.ellipse((x + 12, yy + 15, x + 40, yy + 43), fill=(250, 232, 242) if pink else (240, 233, 255))
        d.text((x + 52, yy + 17), label, font=I("Medium", 19), fill=(40, 35, 60))
    x1 = 40; x2 = 40 + bw + 16
    btn(x1, y + 44, "Tomar foto"); btn(x2, y + 44, "Elegir imagen", hl=t_hl)
    d.text((44, y + 120), "MANUAL", font=I("SemiBold", 15), fill=(110, 105, 130))
    btn(x1, y + 146, "Gasto"); btn(x2, y + 146, "Ingreso")
    btn(x1, y + 216, "Pago planificado", pink=True); btn(x2, y + 216, "Ahorro", pink=True)
    return (x2 + bw / 2, y + 73)

def scr_capture2(t):
    c = CAP2
    if t < c['read']:
        s = Image.new("RGB", (SW, SH), LIGHT); d = ImageDraw.Draw(s, "RGBA")
        _home(s, d); _nav(d, s)
        if t < c['sheet']:
            tap(d, SW / 2, SH - 78, t, c['tap_reg'])
            return s
        # dim + sheet
        p = R.ease((t - c['sheet']) / 0.35)
        d.rectangle((0, 0, SW, SH), fill=(10, 8, 25, int(110 * p)))
        has_opts = t >= c['opts']
        sh_h = 640 if has_opts else 300
        top = SH - sh_h + (1 - p) * sh_h
        R.rrect(d, (0, top, SW, SH + 40), 30, fill=(255, 255, 255))
        d.rounded_rectangle((SW / 2 - 30, top + 12, SW / 2 + 30, top + 18), 3, fill=(210, 208, 220))
        d.text((26, top + 40), "Registrar", font=I("SemiBold", 27), fill=DARKTXT)
        d.text((26, top + 80), "Añade un movimiento para revisar.", font=I("Regular", 18), fill=(90, 88, 105))
        d.text((SW - 46, top + 42), "×", font=I("Regular", 26), fill=(110, 105, 130))
        cy = top + 122
        _composer(d, cy)
        tap(d, 58, cy + 35, t, c['tap_plus'])
        if has_opts:
            q = R.ease((t - c['opts']) / 0.3)
            bx, by = _options(d, cy + 118 + (1 - q) * 30, t_hl=t > c['tap_img'])
            tap(d, bx, by + (1 - q) * 30, t, c['tap_img'])
        return s
    # after choosing the image: reading + detected list (reuse scr_capture layout)
    if t >= c['pend']:
        return scr_pending(t - c['pend'])
    CAP.update(tap=-10, read=c['read'], lst=c['lst'], hl=c['hl'], conf=c['conf'])
    return scr_capture(t)


PENDING = [("Seguro del coche", "día 24", "−380,00 €"), ("Agua", "día 25", "−32,00 €"), ("Luz", "día 26", "−48,00 €"),
           ("Teléfono", "día 27", "−70,00 €"), ("Spotify", "día 28", "−10,99 €")]
def scr_pending(t):
    s = Image.new("RGB", (SW, SH), LIGHT); d = ImageDraw.Draw(s, "RGBA")
    R.status_bar(d)
    s.paste(LOGO.resize((40, 48)), (28, 74))
    d.text((74, 72), "propera", font=R.F(R.POP, 38), fill=DARKTXT)
    R.rrect(d, (20, 146, SW - 20, 220), 18, fill=(225, 245, 233))
    d.text((44, 168), "✓ Movimientos al día", font=I("SemiBold", 22), fill=(30, 120, 80))
    d.text((32, 250), "Aún por pasar este mes", font=I("SemiBold", 23), fill=DARKTXT)
    d.text((32, 284), "Reservado desde el día 1", font=I("Regular", 17), fill=(120, 115, 140))
    y = 322
    for n, (a, day, amt) in enumerate(PENDING):
        p = R.ease((t - 0.3 - n * 0.22) / 0.3)
        if p <= 0: continue
        yy = y + (1 - p) * 14
        R.rrect(d, (20, yy, SW - 20, yy + 70), 16, fill=(255, 255, 255), outline=(230, 228, 238), width=2)
        d.ellipse((36, yy + 21, 64, yy + 49), fill=(250, 232, 242))
        d.text((78, yy + 12), a, font=I("Medium", 21), fill=(60, 55, 80))
        d.text((78, yy + 40), day, font=I("Regular", 16), fill=(130, 125, 150))
        d.text((SW - 44 - d.textlength(amt, font=I("Medium", 21)), yy + 22), amt, font=I("Medium", 21), fill=RED)
        y += 80
    if t > 2.4:
        p = R.ease((t - 2.4) / 0.4)
        R.rrect(d, (20, y + 10, SW - 20, y + 190), 26, fill=(20, 14, 42))
        d.text((44, y + 32), "Disponible real", font=I("Regular", 20), fill=(190, 185, 215))
        d.text((44, y + 64), "640,00 € − 540,99 €", font=I("Regular", 18), fill=(150, 145, 175))
        v = "99,01 €"
        d.text((44, y + 98), v, font=I("Bold", 58), fill=(56, 189, 248, int(255 * p)))
    return s

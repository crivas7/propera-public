import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import render as R

W, H, FPS = 1080, 1920, 30
T = dict(H=0.0, P1=6.0, P2=13.0, P3=18.0, P4=23.0, END=30.0, DUR=34.0)
if os.environ.get('TIMES'):
    T.update({k: float(v) for k, v in (kv.split('=') for kv in os.environ['TIMES'].split(','))})

C2 = sorted(os.listdir('work/c2g'))
def clip(t):
    return Image.open('work/c2g/' + C2[max(0, min(int(t * FPS), len(C2) - 1))]).convert('RGB')

DARKTXT = (25, 18, 50); PURP_D = (110, 60, 210); LIGHT = (246, 245, 251)
SW, SH = R.SW, R.SH
I = R.I
LOGO = R.LOGO_S

def tap(d, x, y, t, t0):
    """ripple tap indicator at (x,y) starting at t0"""
    k = (t - t0) / 0.5
    if 0 <= k <= 1:
        r = 18 + 40 * k
        d.ellipse((x - r, y - r, x + r, y + r), outline=(110, 60, 210, int(220 * (1 - k))), width=5)
        d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=(110, 60, 210, int(160 * (1 - k))))

def header(d, s, title, sub=None):
    R.status_bar(d)
    d.text(((SW - d.textlength(title, font=I("SemiBold", 26))) / 2, 84), title, font=I("SemiBold", 26), fill=(20, 20, 25))
    if sub:
        d.text(((SW - d.textlength(sub, font=I("Regular", 19))) / 2, 120), sub, font=I("Regular", 19), fill=(140, 140, 150))
    d.line((0, 160, SW, 160), fill=(236, 236, 240), width=2)

# ---------- screens ----------
MOVES = [("Nómina", "+1.450,00 €", (30, 140, 90)), ("Alquiler", "−450,00 €", (176, 60, 110)),
         ("Supermercado", "−43,80 €", (176, 60, 110)), ("Gimnasio", "−25,00 €", (176, 60, 110))]
def scr_upload(t):
    s = Image.new("RGB", (SW, SH), LIGHT); d = ImageDraw.Draw(s, "RGBA")
    R.status_bar(d)
    s.paste(LOGO.resize((40, 48)), (28, 74))
    d.text((74, 72), "propera", font=R.F(R.POP, 38), fill=DARKTXT)
    d.text((32, 150), "Entrada inteligente", font=I("SemiBold", 26), fill=DARKTXT)
    d.text((32, 188), "Sube una captura de tu banco", font=I("Regular", 20), fill=(120, 115, 140))
    # upload card
    up = R.ease((t - 1.2) / 0.4)
    R.rrect(d, (24, 236, SW - 24, 420), 24, fill=(255, 255, 255), outline=(200, 180, 245), width=3)
    if up < 1:
        d.text((SW / 2 - 70, 300), "＋ Captura", font=I("Medium", 26), fill=PURP_D)
    if up > 0:
        # fake screenshot thumbnail
        a = int(255 * up)
        R.rrect(d, (48, 256, 150, 400), 10, fill=(225, 230, 240, a))
        for i in range(5):
            d.rectangle((60, 276 + i * 24, 138 - (i % 2) * 20, 284 + i * 24), fill=(170, 178, 195, a))
        d.text((170, 290), "captura_banco.png", font=I("Medium", 21), fill=(60, 55, 80, a))
        prog = R.ease((t - 1.6) / 1.2)
        R.rrect(d, (170, 334, SW - 48, 346), 6, fill=(235, 230, 245))
        R.rrect(d, (170, 334, 170 + (SW - 218) * prog, 346), 6, fill=PURP_D)
        lab = "Leyendo movimientos…" if prog < 1 else "4 movimientos detectados"
        d.text((170, 360), lab, font=I("Regular", 19), fill=(120, 115, 140))
    y = 450
    for i, (a_, b_, c_) in enumerate(MOVES):
        p = R.ease((t - 3.0 - i * 0.25) / 0.35)
        if p <= 0: continue
        yy = y + (1 - p) * 20
        R.rrect(d, (24, yy, SW - 24, yy + 76), 18, fill=(255, 255, 255, int(255 * p)), outline=(230, 228, 238), width=2)
        d.ellipse((40, yy + 24, 68, yy + 52), fill=(233, 222, 255))
        d.text((47, yy + 23), "✓", font=I("Bold", 20), fill=PURP_D)
        d.text((84, yy + 24), a_, font=I("Regular", 22), fill=(60, 55, 80))
        d.text((SW - 44 - d.textlength(b_, font=I("Medium", 22)), yy + 24), b_, font=I("Medium", 22), fill=c_)
        y += 88
    if t > 4.4:
        p = R.ease((t - 4.4) / 0.3)
        R.rrect(d, (24, SH - 120, SW - 24, SH - 44), 38, fill=PURP_D + (int(255 * p),))
        lb = "Confirmar"; d.text(((SW - d.textlength(lb, font=I("SemiBold", 24))) / 2, SH - 98), lb, font=I("SemiBold", 24), fill=(255, 255, 255, int(255 * p)))
        tap(d, SW / 2, SH - 82, t, 5.4)
    return s

SIGN = Image.open('work/signup_es.png').convert('RGB')
_sw = SW; _sh = int(SIGN.size[1] * SW / SIGN.size[0])
SIGN_S = SIGN.resize((_sw, _sh), Image.LANCZOS)
_k = SW / SIGN.size[0]
def scr_signup(t):
    s = Image.new("RGB", (SW, SH), (255, 255, 255)); d = ImageDraw.Draw(s, "RGBA")
    R.status_bar(d)
    oy = 70
    s.paste(SIGN_S, (0, oy))
    d = ImageDraw.Draw(s, "RGBA")
    # type an email into the field (field box in crop coords ~ (193,1112)-(997,1247))
    q = "tu@email.com"[:int(R.clamp((t - 1.3) / 1.0) * 12)]
    if q:
        fx0, fy0, fx1, fy1 = 211 * _k, oy + 1201 * _k, 1072 * _k, oy + 1342 * _k
        d.rectangle((fx0 + 6, fy0 + 6, fx1 - 6, fy1 - 6), fill=(255, 255, 255))
        d.text((fx0 + 20, fy0 + 12), q, font=I("Regular", 24), fill=(30, 35, 50))
    tap(d, SW / 2, oy + 1462 * _k, t, 2.7)
    return s

def scr_plugins(t):
    """0..1.8 side menu (tap Plugins at 1.1); 1.8.. plugins search 'propera' (tap result at 3.6)"""
    s = Image.new("RGB", (SW, SH), (255, 255, 255)); d = ImageDraw.Draw(s, "RGBA")
    R.status_bar(d)
    if t < 1.8:
        d.text((36, 90), "ChatGPT", font=I("SemiBold", 34), fill=(20, 20, 25))
        rows = ["Programadas", "Biblioteca", "Personalizar", "Explorar", "Proyectos", "Plugins", "Imágenes"]
        for n, r in enumerate(rows):
            y = 170 + n * 76
            hl = r == "Plugins" and t > 1.1
            if hl: R.rrect(d, (16, y - 8, SW - 16, y + 58), 16, fill=(243, 238, 255))
            d.ellipse((38, y + 8, 64, y + 34), outline=PURP_D if hl else (120, 120, 130), width=3)
            d.text((84, y + 6), r, font=I("SemiBold" if hl else "Regular", 25), fill=PURP_D if hl else (30, 30, 35))
        tap(d, 160, 170 + 5 * 76 + 24, t, 1.1)
    else:
        u = t - 1.8
        tt = "Plugins"; d.text(((SW - d.textlength(tt, font=I("SemiBold", 27))) / 2, 84), tt, font=I("SemiBold", 27), fill=(20, 20, 25))
        R.rrect(d, (24, 140, SW - 24, 200), 30, fill=(244, 244, 246))
        q = "propera"[:int(R.clamp((u - 0.2) / 0.8) * 7)]
        d.text((60, 155), q if q else "Buscar plugins", font=I("Regular", 23), fill=(25, 25, 30) if q else (150, 150, 158))
        if u > 1.1:
            p = R.ease((u - 1.1) / 0.35)
            y = 236 + (1 - p) * 20
            R.rrect(d, (16, y - 6, SW - 16, y + 104), 18, fill=(243, 238, 255) if u > 1.8 else (255, 255, 255))
            R.rrect(d, (32, y + 8, 112, y + 88), 20, fill=(255, 255, 255), outline=(230, 228, 238), width=2)
            s.paste(LOGO.resize((44, 52)), (50, int(y + 22)))
            d.text((130, y + 14), "Propera", font=I("SemiBold", 26), fill=(25, 25, 30))
            d.text((130, y + 52), "Organize personal finances", font=I("Regular", 17), fill=(130, 130, 140))
            tap(d, SW / 2, y + 48, u, 1.8)
    return s

def scr_connect(t):
    """0..1.6 Propera plugin page (tap Conectar 1.0); 1.6.. Propera sign-in + authorize (tap 2.2)"""
    s = Image.new("RGB", (SW, SH), (255, 255, 255)); d = ImageDraw.Draw(s, "RGBA")
    R.status_bar(d)
    if t < 1.6:
        tt = "Propera"; d.text(((SW - d.textlength(tt, font=I("SemiBold", 26))) / 2, 84), tt, font=I("SemiBold", 26), fill=(20, 20, 25))
        R.rrect(d, (32, 150, 132, 250), 24, fill=(255, 255, 255), outline=(230, 228, 238), width=2)
        s.paste(LOGO.resize((56, 66)), (54, 167))
        d.text((32, 276), "Propera", font=I("SemiBold", 40), fill=DARKTXT)
        desc = "Consulta tus finanzas y prepara ingresos o gastos para revisarlos en Propera."
        for n, l in enumerate(R.wrap(d, desc, I("Regular", 22), SW - 64)):
            d.text((32, 384 + n * 32), l, font=I("Regular", 22), fill=(60, 60, 70))
        R.rrect(d, (32, SH - 130, SW - 32, SH - 52), 39, fill=(25, 25, 30))
        lb = "Conectar"; d.text(((SW - d.textlength(lb, font=I("SemiBold", 25))) / 2, SH - 107), lb, font=I("SemiBold", 25), fill=(255, 255, 255))
        tap(d, SW / 2, SH - 91, t, 1.0)
    else:
        u = t - 1.6
        s.paste(Image.new("RGB", (SW, SH), LIGHT)); d = ImageDraw.Draw(s, "RGBA")
        R.status_bar(d)
        s.paste(LOGO.resize((56, 66)), (int(SW / 2 - 28), 100))
        tt = "Inicia sesión en Propera"; d.text(((SW - d.textlength(tt, font=I("SemiBold", 27))) / 2, 186), tt, font=I("SemiBold", 27), fill=DARKTXT)
        R.rrect(d, (32, 250, SW - 32, 318), 16, fill=(255, 255, 255), outline=(225, 220, 238), width=2)
        d.text((54, 271), "tu@email.com", font=I("Regular", 22), fill=(60, 55, 80))
        d.text((32, 352), "ChatGPT quiere acceder a tu cuenta:", font=I("Medium", 21), fill=(60, 55, 80))
        perms = ["Consultar tu disponible real", "Ver tus pagos planificados", "Proponer movimientos (los confirmas tú)"]
        for n, pm in enumerate(perms):
            p = R.ease((u - 0.2 - n * 0.15) / 0.3)
            if p <= 0: continue
            y = 396 + n * 62
            d.ellipse((34, y + 4, 62, y + 32), fill=(233, 222, 255, int(255 * p)))
            d.text((41, y + 3), "✓", font=I("Bold", 20), fill=PURP_D + (int(255 * p),))
            d.text((76, y + 4), pm, font=I("Regular", 21), fill=(40, 40, 50, int(255 * p)))
        R.rrect(d, (32, 640, SW - 32, 716), 38, fill=PURP_D)
        lb = "Autorizar"; d.text(((SW - d.textlength(lb, font=I("SemiBold", 24))) / 2, 662), lb, font=I("SemiBold", 24), fill=(255, 255, 255))
        tap(d, SW / 2, 678, u, 1.6)
        if u > 2.1:
            p = R.ease((u - 2.1) / 0.3)
            R.rrect(d, (32, 750, SW - 32, 820), 20, fill=(225, 245, 233, int(255 * p)))
            ok = "✓ Propera conectado a ChatGPT"
            d.text(((SW - d.textlength(ok, font=I("SemiBold", 22))) / 2, 772), ok, font=I("SemiBold", 22), fill=(30, 120, 80, int(255 * p)))
    return s

Q4 = "¿Cuánto tengo disponible de verdad?"
A4 = ("Tienes 210 € disponibles de verdad hasta que cobres el día 28.\n"
      "Ya he descontado lo comprometido: alquiler, luz y gimnasio (430 €).\n"
      "Eso son unos 12 € al día durante 17 días.")
def scr_chat(t):
    R.USER_Q, R.ANSWER = Q4, A4
    return R.chat_screen(t)

# ---------- scene composition ----------
def step_bg():
    return R.BRAND.copy()

def step_label(im, n, label, t):
    d = ImageDraw.Draw(im, "RGBA")
    p = R.ease(t / 0.35)
    pill = f"PASO {n}"
    f = R.F(R.POP, 40); w = d.textlength(pill, font=f) + 56
    x0 = (W - w) / 2; y0 = 150 + (1 - p) * 30
    d.rounded_rectangle((x0, y0, x0 + w, y0 + 70), 35, fill=(150, 90, 240, int(255 * p)))
    d.text((x0 + 28, y0 + 10), pill, font=f, fill=(255, 255, 255, int(255 * p)))
    R.headline(im, [(label, R.WHITE)], 245, t, 60, start=0.15)

PH_SCALE, PH_TOP = 1.18, 350
def put_phone(im, screen, t):
    pin = R.ease(t / 0.45)
    R.paste_phone(im, R.phone(screen, PH_SCALE), W / 2, PH_TOP + (1 - pin) * 900)

def sH(t):
    im = clip(t)
    R.headline(im, [("¿Cuánto tienes de verdad?", DARKTXT)], 150, t, 70, start=0.2)
    R.headline(im, [("Pregúntaselo a ChatGPT", PURP_D)], 245, t, 70, start=1.4)
    return im

def sP1(t):
    im = step_bg(); step_label(im, 1, "¿Sin cuenta? Créala gratis", t); put_phone(im, scr_signup(t), t); return im
def sP2(t):
    im = step_bg(); step_label(im, 2, "Menú > Plugins > Propera", t); put_phone(im, scr_plugins(t), t); return im
def sP3(t):
    im = step_bg(); step_label(im, 3, "Conectar y autorizar", t); put_phone(im, scr_connect(t), t); return im
def sP4(t):
    im = step_bg()
    d = ImageDraw.Draw(im, "RGBA")
    p = R.ease(t / 0.35)
    pill = "¡LISTO!"; f = R.F(R.POP, 40); w = d.textlength(pill, font=f) + 56
    x0 = (W - w) / 2; y0 = 150 + (1 - p) * 30
    d.rounded_rectangle((x0, y0, x0 + w, y0 + 70), 35, fill=(56, 189, 248, int(255 * p)))
    d.text((x0 + 28, y0 + 10), pill, font=f, fill=(14, 9, 32, int(255 * p)))
    R.headline(im, [("Pregunta lo que quieras", R.WHITE)], 245, t, 60, start=0.15)
    put_phone(im, scr_chat(t), t)
    return im
def sEND(t):
    im = R.END.copy()
    R.headline(im, [("Pruébalo gratis, sin tarjeta", R.WHITE)], 1400, t, 56, start=0.9)
    R.headline(im, [("Link en la bio", R.PURPLE)], 1478, t, 56, start=2.8)
    return im

def scenes():
    return [(T['H'], T['P1'], sH), (T['P1'], T['P2'], sP1), (T['P2'], T['P3'], sP2),
            (T['P3'], T['P4'], sP3), (T['P4'], T['END'], sP4), (T['END'], T['DUR'], sEND)]

if __name__ == '__main__':
    R.SCENES[:] = scenes()
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    only = os.environ.get('ONLY')
    ks = range(int(T['DUR'] * FPS)) if not only else [int(float(x) * FPS) for x in only.split(',')]
    for k in ks:
        R.frame(k / FPS).save(f'{out}/{k:04d}.png')

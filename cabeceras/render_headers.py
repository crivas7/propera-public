"""Exporta la cabecera A (Disponible real, oscuro) en PNG para X, Facebook y YouTube."""
from PIL import Image, ImageDraw, ImageFont

POP = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
INTER = "/usr/share/fonts/opentype/inter/Inter-%s.otf"
def P(s): return ImageFont.truetype(POP, s)
def I(w, s): return ImageFont.truetype(INTER % w, s)
BG = (18, 12, 42); CARD = (28, 21, 64); BORDER = (47, 38, 99)
WHITE = (255, 255, 255); LILA = (196, 140, 255); MUTED = (171, 164, 204); CMUT = (185, 178, 217)
BLUE = (56, 189, 248); PINK = (244, 154, 193)
LOGO = Image.open('/home/claude/work/headers/logo_hq.png').convert('RGBA')

def render(W, H, k, lx, ly, cx, cy, cw, gap_dots, out, S=2, lema=True):
    """k = escala tipográfica; (lx,ly) bloque izq.; (cx,cy,cw) tarjeta. Dibuja a S× y reduce."""
    im = Image.new('RGB', (W * S, H * S), BG); d = ImageDraw.Draw(im)
    for y in range(gap_dots // 2, H, gap_dots):
        for x in range(gap_dots // 2, W, gap_dots):
            r = 1.2 * S
            d.ellipse((x * S - r, y * S - r, x * S + r, y * S + r), fill=(38, 32, 62))
    s = lambda v: int(round(v * S))
    # logo + marca
    lh = 76 * k
    lg = LOGO.resize((s(lh * LOGO.width / LOGO.height), s(lh)), Image.LANCZOS)
    im.paste(lg, (s(lx), s(ly)), lg)
    f = P(s(44 * k))
    tx = lx + lh * LOGO.width / LOGO.height + 16 * k
    d.text((s(tx), s(ly + lh / 2)), "propera", font=f, fill=WHITE, anchor='lm')
    # titular
    f = P(s(48 * k)); y = ly + 110 * k
    d.text((s(lx), s(y)), "Una cosa es el saldo.", font=f, fill=WHITE)
    d.text((s(lx), s(y + 58 * k)), "Otra, lo que puedes gastar.", font=f, fill=LILA)
    # lema + web
    f1, f2 = I('Regular', s(20 * k)), I('SemiBold', s(20 * k))
    y = ly + 262 * k; a = "Prosperar comienza con orden. · "
    if lema:
        d.text((s(lx), s(y)), a, font=f1, fill=MUTED)
        d.text((s(lx) + d.textlength(a, font=f1), s(y)), "propera.life", font=f2, fill=WHITE)
    # tarjeta
    p = 30 * k; ch = 272 * k
    d.rounded_rectangle((s(cx), s(cy), s(cx + cw), s(cy + ch)), s(28 * k), fill=CARD, outline=BORDER, width=max(1, s(1)))
    x0, x1 = cx + p, cx + cw - p; y = cy + 30 * k
    d.text((s(x0), s(y)), "Disponible real", font=I('Regular', s(17 * k)), fill=CMUT)
    d.text((s(x0 - 3 * k), s(y + 30 * k)), "99,01 €", font=I('Bold', s(62 * k)), fill=BLUE)
    yl = y + 122 * k
    d.line((s(x0), s(yl), s(x1), s(yl)), fill=BORDER, width=max(1, s(1)))
    fr, fb = I('Regular', s(17 * k)), I('SemiBold', s(17 * k))
    for i, (a, b, c) in enumerate([("Saldo en el banco", "640,00 €", WHITE), ("Pagos planificados", "−540,99 €", PINK)]):
        yy = yl + (24 + i * 40) * k
        d.text((s(x0), s(yy)), a, font=fr, fill=CMUT)
        d.text((s(x1) - d.textlength(b, font=fb), s(yy)), b, font=fb, fill=c)
    im.resize((W, H), Image.LANCZOS).save(out, optimize=True)

O = '/home/claude/out/'
render(1500, 500, 1.0, 120, 62, 1010, 92, 370, 28, O + 'cabecera_x_1500x500.png', lema=False)
render(1640, 624, 1.05, 210, 112, 1070, 160, 370, 30, O + 'portada_facebook_1640x624.png')
render(2560, 1440, 1.32, 560, 516, 1600, 522, 440, 40, O + 'banner_youtube_2560x1440.png')
print('ok')

# foto de perfil: fondo de marca, águila centrada con margen para el recorte circular
av = Image.new('RGB', (1600, 1600), BG)
h = 940; lg = LOGO.resize((round(h * LOGO.width / LOGO.height), h), Image.LANCZOS)
av.paste(lg, ((1600 - lg.width) // 2 + 12, (1600 - h) // 2), lg)
av.resize((800, 800), Image.LANCZOS).save(O + 'foto_perfil_800x800.png', optimize=True)
av.resize((400, 400), Image.LANCZOS).save(O + 'foto_perfil_400x400.png', optimize=True)
print('avatar ok')

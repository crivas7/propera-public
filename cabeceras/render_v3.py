"""Cabeceras v3: fondo oscuro liso, marca solo con la palabra 'propera' y texto grande."""
from PIL import Image, ImageDraw, ImageFont
POP = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
INTER = "/usr/share/fonts/opentype/inter/Inter-%s.otf"
def P(s): return ImageFont.truetype(POP, s)
def I(w, s): return ImageFont.truetype(INTER % w, s)
BG = (18, 12, 42); CARD = (28, 21, 64); BORDER = (47, 38, 99)
WHITE = (255, 255, 255); LILA = (196, 140, 255); MUTED = (171, 164, 204); CMUT = (185, 178, 217)
BLUE = (56, 189, 248); PINK = (244, 154, 193)

def wordmark(im, x, y, size, style):
    """y = parte superior. Tracking algo cerrado. Estilos: dot | grad | bar"""
    d = ImageDraw.Draw(im); f = P(size); tr = -size * 0.035
    def run(draw, fill, text="propera"):
        cx = x
        for ch in text:
            draw.text((cx, y), ch, font=f, fill=fill); cx += draw.textlength(ch, font=f) + tr
        return cx
    if style == 'grad':
        m = Image.new('L', im.size, 0); end = run(ImageDraw.Draw(m), 255)
        g = Image.new('RGB', im.size, LILA); gd = ImageDraw.Draw(g)
        for i in range(int(x), int(end) + 1):
            t = (i - x) / max(1, end - x)
            gd.line((i, 0, i, im.size[1]), fill=tuple(int(LILA[c] + (BLUE[c] - LILA[c]) * t) for c in range(3)))
        im.paste(g, (0, 0), m); return
    end = run(d, WHITE)
    if style == 'dot':
        r = size * 0.085; by = y + size * 1.02
        d.ellipse((end + size * 0.06, by - 2 * r, end + size * 0.06 + 2 * r, by), fill=BLUE)
    if style == 'bar':
        d.rounded_rectangle((x + size * 0.04, y + size * 1.42, x + size * 1.3, y + size * 1.42 + size * 0.11), size * 0.06, fill=LILA)

def render(W, H, k, lx, ly, cx, cy, cw, out, kc, lema=True, style='dot', S=3):
    im = Image.new('RGB', (W * S, H * S), BG); d = ImageDraw.Draw(im)
    s = lambda v: int(round(v * S))
    wordmark(im, s(lx), s(ly), s(54 * k), style); d = ImageDraw.Draw(im)
    f = P(s(48 * k)); y = ly + 110 * k
    d.text((s(lx), s(y)), "Una cosa es el saldo.", font=f, fill=WHITE)
    d.text((s(lx), s(y + 58 * k)), "Otra, lo que puedes gastar.", font=f, fill=LILA)
    if lema:
        f1, f2 = I('Regular', s(20 * k)), I('SemiBold', s(20 * k)); y = ly + 262 * k; a = "Prosperar comienza con orden. · "
        d.text((s(lx), s(y)), a, font=f1, fill=MUTED); d.text((s(lx) + d.textlength(a, font=f1), s(y)), "propera.life", font=f2, fill=WHITE)
    k = kc; p = 30 * k; ch = 272 * k
    d.rounded_rectangle((s(cx), s(cy), s(cx + cw), s(cy + ch)), s(28 * k), fill=CARD, outline=BORDER, width=s(1.5))
    x0, x1 = cx + p, cx + cw - p; y = cy + 30 * k
    d.text((s(x0), s(y)), "Disponible real", font=I('Regular', s(17 * k)), fill=CMUT)
    d.text((s(x0 - 3 * k), s(y + 30 * k)), "99,01 €", font=I('Bold', s(62 * k)), fill=BLUE)
    yl = y + 122 * k; d.line((s(x0), s(yl), s(x1), s(yl)), fill=BORDER, width=s(1.5))
    fr, fb = I('Regular', s(17 * k)), I('SemiBold', s(17 * k))
    for i, (a, b, c) in enumerate([("Saldo en el banco", "640,00 €", WHITE), ("Pagos planificados", "−540,99 €", PINK)]):
        yy = yl + (24 + i * 40) * k
        d.text((s(x0), s(yy)), a, font=fr, fill=CMUT); d.text((s(x1) - d.textlength(b, font=fb), s(yy)), b, font=fb, fill=c)
    im.resize((W, H), Image.LANCZOS).save(out, optimize=True)

if __name__ == '__main__':
    O = '/home/claude/out/'
    for st in ('dot', 'grad', 'bar'):
        render(1500, 500, 1.15, 90, 36, 985, 62, 440, f'/tmp/x_{st}.png', 1.3, lema=False, style=st)
    render(1500, 500, 1.15, 90, 36, 985, 62, 440, O + 'cabecera_x_v3_1500x500.png', 1.3, lema=False)
    render(1640, 624, 1.15, 200, 150, 1020, 142, 430, O + 'portada_facebook_v3_1640x624.png', 1.25)
    render(2560, 1440, 1.5, 540, 545, 1565, 522, 480, O + 'banner_youtube_v3_2560x1440.png', 1.45, lema=False, S=2)
    print('ok')

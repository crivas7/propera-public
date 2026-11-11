import math, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
DUR = 21.0
OUT = sys.argv[1] if len(sys.argv) > 1 else "work/frames"
os.makedirs(OUT, exist_ok=True)

POP = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
POPM = "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"
INT = "/usr/share/fonts/opentype/inter/Inter-%s.otf"
_fc = {}
def F(path, size):
    k = (path, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]
def I(w, s): return F(INT % w, s)

PURPLE = (196, 140, 255)
WHITE = (255, 255, 255)
DARK = (17, 11, 38)

def ease(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def clamp(x): return max(0.0, min(1.0, x))

# ---------- backgrounds ----------
def brand_bg():
    bg = Image.new("RGB", (W, H), (14, 9, 32))
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(glow)
    d.ellipse((140, 300, 940, 1300), fill=(70, 35, 140))
    glow = glow.filter(ImageFilter.GaussianBlur(220))
    return Image.blend(bg, Image.eval(glow, lambda v: v), 0.0) if False else Image.composite(glow, bg, Image.new("L", (W, H), 0)) if False else _add(bg, glow)
def _add(a, b):
    from PIL import ImageChops
    return ImageChops.add(a, b)
BRAND = brand_bg()

def placeholder_bg(t):
    im = BRAND.copy()
    d = ImageDraw.Draw(im)
    # dashed slot
    x0, y0, x1, y1 = 90, 560, 990, 1500
    dash = 28
    for x in range(x0, x1, dash * 2):
        d.line((x, y0, min(x + dash, x1), y0), fill=(120, 95, 180), width=4)
        d.line((x, y1, min(x + dash, x1), y1), fill=(120, 95, 180), width=4)
    for y in range(y0, y1, dash * 2):
        d.line((x0, y, x0, min(y + dash, y1)), fill=(120, 95, 180), width=4)
        d.line((x1, y, x1, min(y + dash, y1)), fill=(120, 95, 180), width=4)
    f = I("Medium", 34)
    for i, s in enumerate(["CLIP DE PEXELS", "hombre con zapatillas en una tienda"]):
        w = d.textlength(s, font=f)
        d.text(((W - w) / 2, 1430 + i * 44 - 44), s, font=f, fill=(140, 120, 190))
    return im

BGF = sorted(os.listdir("work/bg")) if os.path.isdir("work/bg") else []
def video_bg(t):
    i = min(int(t * FPS), len(BGF) - 1)
    return Image.open("work/bg/" + BGF[i]).convert("RGB")

# ---------- text helpers ----------
def headline(im, lines, y, t, size=78, start=0.0, center=True):
    """lines: list of (text, color). Fade + slide up, staggered."""
    d = ImageDraw.Draw(im, "RGBA")
    f = F(POP, size)
    for i, (s, col) in enumerate(lines):
        p = ease((t - start - i * 0.12) / 0.45)
        if p <= 0: continue
        w = d.textlength(s, font=f)
        x = (W - w) / 2 if center else 80
        yy = y + i * int(size * 1.18) + (1 - p) * 40
        a = int(255 * p)
        if sum(col) > 450: d.text((x + 3, yy + 4), s, font=f, fill=(0, 0, 0, int(a * 0.35)))
        d.text((x, yy), s, font=f, fill=col + (a,))

def rrect(d, box, r, **kw): d.rounded_rectangle(box, r, **kw)

# ---------- phone ----------
PW, PH = 560, 1160
def phone(screen, scale=1.0):
    """screen: PIL image 528x1128. Returns RGBA phone."""
    ph = Image.new("RGBA", (PW, PH), (0, 0, 0, 0))
    d = ImageDraw.Draw(ph)
    rrect(d, (0, 0, PW - 1, PH - 1), 78, fill=(28, 28, 32), outline=(70, 70, 78), width=3)
    mask = Image.new("L", screen.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, screen.size[0] - 1, screen.size[1] - 1), 64, fill=255)
    ph.paste(screen, (16, 16), mask)
    d.rounded_rectangle((PW / 2 - 64, 30, PW / 2 + 64, 66), 18, fill=(0, 0, 0))
    if scale != 1.0:
        ph = ph.resize((int(PW * scale), int(PH * scale)), Image.LANCZOS)
    return ph

def paste_phone(im, ph, cx, top, t_in=None):
    shadow = Image.new("RGBA", (ph.size[0] + 160, ph.size[1] + 160), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((80, 100, ph.size[0] + 80, ph.size[1] + 90), 80, fill=(0, 0, 0, 150))
    shadow = shadow.filter(ImageFilter.GaussianBlur(40))
    im.paste(shadow, (int(cx - ph.size[0] / 2 - 80), int(top - 80)), shadow)
    im.paste(ph, (int(cx - ph.size[0] / 2), int(top)), ph)

SW, SH = 528, 1128
def status_bar(d, dark=False):
    c = (20, 20, 25)
    d.text((44, 28), "9:41", font=I("SemiBold", 24), fill=c)
    for i, h in enumerate([8, 12, 16, 20]):
        d.rectangle((400 + i * 9, 50 - h, 406 + i * 9, 50), fill=c)
    rrect(d, (450, 34, 488, 52), 5, outline=c, width=2)
    d.rectangle((454, 38, 480, 48), fill=c)

LOGO_S = Image.open("assets/logo_small.png").convert("RGB")

def wrap(d, text, font, width):
    out = []
    for para in text.split("\n"):
        line = ""
        for w in para.split(" "):
            tt = (line + " " + w).strip()
            if d.textlength(tt, font=font) <= width: line = tt
            else:
                out.append(line); line = w
        out.append(line)
    return out

USER_Q = "¿Me puedo comprar unas zapatillas de 90 €?"
ANSWER = ("Tienes 640 € en el banco, pero 430 € ya están comprometidos: alquiler, luz y gimnasio.\n"
          "Tu disponible real es de 210 € hasta que cobres el día 28.\n"
          "Puedes comprarlas, pero te quedarían 120 € para 17 días.")

def chat_screen(t):
    """t local seconds within the chat scene."""
    s = Image.new("RGB", (SW, SH), (255, 255, 255))
    d = ImageDraw.Draw(s)
    status_bar(d)
    # header
    hf = I("SemiBold", 26)
    title = "Asistente IA"
    d.text(((SW - d.textlength(title, font=hf)) / 2, 84), title, font=hf, fill=(20, 20, 25))
    chip = "Propera conectado"
    cf = I("Medium", 19)
    cw = d.textlength(chip, font=cf) + 64
    cx0 = (SW - cw) / 2
    rrect(d, (cx0, 124, cx0 + cw, 162), 19, fill=(243, 238, 255))
    lg = LOGO_S.resize((22, 26))
    s.paste(lg, (int(cx0 + 14), 130))
    d.text((cx0 + 44, 132), chip, font=cf, fill=(110, 60, 210))
    d.line((0, 182, SW, 182), fill=(236, 236, 240), width=2)

    # input bar
    rrect(d, (24, SH - 110, SW - 24, SH - 42), 34, fill=(244, 244, 246))
    typing_end = 0.6 + len(USER_Q) * 0.05
    sent = t > typing_end + 0.15
    if not sent:
        n = int(clamp((t - 0.6) / (typing_end - 0.6)) * len(USER_Q))
        txt = USER_Q[:n]
        f = I("Regular", 21)
        lines = wrap(d, txt, f, SW - 140) if txt else [""]
        show = lines[-1] if txt else "Pregunta lo que quieras"
        col = (25, 25, 30) if txt else (150, 150, 158)
        d.text((52, SH - 90), show, font=f, fill=col)
        if txt and int(t * 3) % 2 == 0:
            cxp = 52 + d.textlength(show, font=f) + 2
            d.line((cxp, SH - 90, cxp, SH - 62), fill=(110, 60, 210), width=2)
    else:
        d.text((52, SH - 90), "Pregunta lo que quieras", font=I("Regular", 21), fill=(150, 150, 158))
    # send button
    d.ellipse((SW - 92, SH - 102, SW - 36, SH - 50), fill=(25, 25, 30) if not sent else (210, 210, 215))
    d.polygon([(SW - 64, SH - 88), (SW - 74, SH - 74), (SW - 54, SH - 74)], fill=WHITE)
    d.line((SW - 64, SH - 78, SW - 64, SH - 62), fill=WHITE, width=4)

    y = 220
    if sent:
        f = I("Regular", 23)
        lines = wrap(d, USER_Q, f, 330)
        bw = max(d.textlength(l, font=f) for l in lines) + 44
        bh = len(lines) * 32 + 30
        p = ease((t - typing_end - 0.15) / 0.3)
        yy = y + (1 - p) * 30
        rrect(d, (SW - 24 - bw, yy, SW - 24, yy + bh), 26, fill=(236, 236, 241))
        for i, l in enumerate(lines):
            d.text((SW - 24 - bw + 22, yy + 14 + i * 32), l, font=f, fill=(20, 20, 25))
        y += bh + 34
        tc = typing_end + 0.5
        ans_start = tc + 1.6
        if t > tc:
            # tool call chip
            f2 = I("Medium", 20)
            label = "Consultando Propera" + ("…" if t > ans_start else "." * (1 + int(t * 4) % 3))
            if t > ans_start: label = "Consultó Propera"
            lw = d.textlength(label, font=f2) + 70
            rrect(d, (24, y, 24 + lw, y + 46), 23, fill=(247, 244, 255), outline=(225, 214, 255), width=2)
            s.paste(LOGO_S.resize((22, 26)), (40, int(y + 10)))
            d.text((72, y + 11), label, font=f2, fill=(110, 60, 210))
            y += 72
        if t > ans_start:
            f3 = I("Regular", 23)
            fb = I("SemiBold", 23)
            words_total = len(ANSWER.replace("\n", " \n ").split(" "))
            nshow = int((t - ans_start) * 11)
            shown = 0
            for para in ANSWER.split("\n"):
                for l in wrap(d, para, f3, SW - 60):
                    ws = l.split(" ")
                    x = 26
                    for w in ws:
                        if shown >= nshow: break
                        bold = any(k in w for k in ["210", "120"]) or w in ("€",) and False
                        ft = fb if bold else f3
                        col = (110, 60, 210) if bold else (25, 25, 30)
                        d.text((x, y), w, font=ft, fill=col)
                        x += d.textlength(w + " ", font=ft)
                        shown += 1
                    y += 34
                y += 18
    return s

def propera_screen(t):
    s = Image.new("RGB", (SW, SH), (246, 245, 251))
    d = ImageDraw.Draw(s)
    status_bar(d)
    s.paste(LOGO_S.resize((40, 48)), (28, 74))
    d.text((74, 72), "propera", font=F(POP, 38), fill=(25, 18, 50))
    d.text((76, 124), "Tu situación hoy", font=I("Regular", 20), fill=(120, 115, 140))
    d.ellipse((440, 82, 488, 130), fill=(236, 228, 255))
    d.text((457, 92), "C", font=I("SemiBold", 22), fill=(110, 60, 210))
    rrect(d, (18, 170, SW - 18, 390), 30, fill=(20, 14, 42))
    d.text((44, 196), "Disponible real", font=I("Regular", 21), fill=(190, 185, 215))
    p = ease((t - 0.8) / 1.6)
    val = 640 - (640 - 210) * p
    txt = f"{int(val):d},00 €".replace(",00", ",00")
    d.text((42, 232), txt, font=I("Bold", 64), fill=(56, 189, 248))
    rrect(d, (44, 330, 210, 364), 17, fill=(55, 38, 110))
    d.ellipse((56, 342, 66, 352), fill=(250, 200, 80) if p >= 1 else (160, 150, 200))
    d.text((74, 336), "Ajustado" if p >= 1 else "Calculando…", font=I("Medium", 18), fill=WHITE)
    d.text((36, 430), "Así se calcula", font=I("SemiBold", 22), fill=(25, 18, 50))
    rows = [("Dinero actual", "640,00 €", (25, 18, 50)),
            ("Alquiler", "−450,00 €", (176, 60, 110)),
            ("Luz", "−48,00 €", (176, 60, 110)),
            ("Gimnasio", "−25,00 €", (176, 60, 110))]
    # 640 - 450 - 48 - 25 = 117 → use pagos protegidos summary instead to keep 210
    rows = [("Dinero actual", "640,00 €", (25, 18, 50)),
            ("Pagos protegidos", "−430,00 €", (176, 60, 110)),
            ("Ahorro reservado", "0,00 €", (120, 115, 140))]
    y = 470
    for i, (a, b, c) in enumerate(rows):
        pp = ease((t - 0.2 - i * 0.18) / 0.35)
        if pp <= 0: continue
        rrect(d, (18, y, SW - 18, y + 78), 18, fill=WHITE, outline=(230, 228, 238), width=2)
        d.text((44, y + 24), a, font=I("Regular", 22), fill=(60, 55, 80))
        d.text((SW - 44 - d.textlength(b, font=I("Medium", 22)), y + 24), b, font=I("Medium", 22), fill=c)
        y += 92
    if t > 2.5:
        rrect(d, (18, 760, SW - 18, 850), 22, fill=(238, 230, 255))
        d.text((44, 790), "Disponible real", font=I("SemiBold", 23), fill=(110, 60, 210))
        v = "210,00 €"
        d.text((SW - 44 - d.textlength(v, font=I("Bold", 27)), 786), v, font=I("Bold", 27), fill=(90, 40, 190))
    rrect(d, (18, SH - 112, SW - 18, SH - 36), 38, outline=(160, 90, 240), width=3, fill=WHITE)
    d.ellipse((34, SH - 102, 90, SH - 46), fill=(240, 232, 255))
    d.text((52, SH - 98), "+", font=I("Regular", 36), fill=(110, 60, 210))
    d.text((108, SH - 88), "Cuéntale a Propera qué pasó", font=I("Regular", 20), fill=(150, 145, 165))
    return s

END = Image.open("assets/end.png").convert("RGB")

# ---------- scenes ----------
def s1(t):
    im = placeholder_bg(t)
    d = ImageDraw.Draw(im, "RGBA")
    headline(im, [("POV: no llevas tus gastos", WHITE), ("y quieres estas", WHITE), ("zapatillas", PURPLE)], 250, t, 74)
    return im

def s2(t):
    im = placeholder_bg(t + 3)
    d = ImageDraw.Draw(im, "RGBA")
    # price tag
    p = ease(t / 0.4)
    tag_w, tag_h = 420, 170
    x0 = (W - tag_w) / 2; y0 = 900 + (1 - p) * 60
    rrect(d, (x0, y0, x0 + tag_w, y0 + tag_h), 26, fill=(255, 255, 255, int(240 * p)))
    pf = F(POP, 92); s = "89,99 €"
    d.text(((W - d.textlength(s, font=pf)) / 2, y0 + 24), s, font=pf, fill=(25, 18, 50, int(255 * p)))
    headline(im, [("El banco dice 640 €…", WHITE)], 250, t, 74, start=0.5)
    headline(im, [("¿me las puedo", PURPLE), ("permitir?", PURPLE)], 360, t, 74, start=1.1)
    return im

def s3(t):
    im = video_bg(t)
    headline(im, [("Se lo pregunto a mi IA", WHITE), ("con Propera conectado", PURPLE)], 120, t, 62)
    ph = phone(chat_screen(t), 1.24)
    pin = ease(t / 0.5)
    paste_phone(im, ph, W / 2, 340 + (1 - pin) * 200)
    return im

def s4(t):
    im = BRAND.copy()
    d = ImageDraw.Draw(im, "RGBA")
    f = F(POP, 74)
    l1 = "640 € en el banco."
    p = ease(t / 0.45)
    w = d.textlength(l1, font=f)
    d.text(((W - w) / 2, 170 + (1 - p) * 40), l1, font=f, fill=(255, 255, 255, int(255 * p)))
    sp = ease((t - 0.7) / 0.4)
    if sp > 0:
        y = 170 + 52
        d.line(((W - w) / 2 - 10, y, (W - w) / 2 - 10 + (w + 20) * sp, y), fill=PURPLE, width=8)
    headline(im, [("210 € de verdad.", PURPLE)], 270, t, 74, start=1.0)
    paste_phone(im, phone(propera_screen(max(0, t - 0.3)), 1.18), W / 2, 450)
    return im

def s5(t):
    im = END.copy()
    return im

SCENES = [(0.0, 3.0, s1), (3.0, 6.5, s2), (6.5, 13.5, s3), (13.5, 17.0, s4), (17.0, 21.0, s5)]
XF = 0.25

def frame(t):
    for i, (a, b, fn) in enumerate(SCENES):
        if a <= t < b or (i == len(SCENES) - 1 and t >= a):
            im = fn(t - a)
            if i > 0 and t - a < XF:
                pa, pb, pfn = SCENES[i - 1]
                prev = pfn(pb - pa - 0.001)
                im = Image.blend(prev, im, (t - a) / XF)
            return im

if __name__ == "__main__":
    only = os.environ.get("ONLY")
    n = int(DUR * FPS)
    rng = range(n) if not only else [int(float(x) * FPS) for x in only.split(",")]
    for k in rng:
        frame(k / FPS).save(f"{OUT}/{k:04d}.png" if not only else f"{OUT}/test_{k:04d}.png")

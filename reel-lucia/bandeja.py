"""Bandeja de Propera rediseñada a escala de móvil (528x1128): revisión, pagos planificados y registro en grupo."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import render as R, lucia_screens as L

SW, SH = R.SW, R.SH
I = R.I
DARK = (25, 18, 50); GREY = (110, 105, 130); LINE = (228, 225, 238)
BTN = (76, 26, 140); PBOX = (248, 244, 255); POUT = (214, 198, 246); GREEN = (28, 140, 90)
ease = R.ease
CW = SW - 40          # card width
TOP, NAVH = 132, 118  # content viewport

# movimientos de la captura (mismo orden que el banco)
MOVES = [
    dict(k='cafe', name='Café', amt='−3,50 €', date='10/11/2026', kind='edit'),
    dict(k='net', name='Netflix', amt='−9,99 €', date='11/11/2026', kind='plan', pay='Netflix', exp='9,99 €', due='11/11/2026'),
    dict(k='farm', name='Farmacia', amt='−12,80 €', date='12/11/2026', kind='norm'),
    dict(k='gym', name='Gimnasio', amt='−29,90 €', date='13/11/2026', kind='plan', pay='Gimnasio', exp='29,90 €', due='13/11/2026'),
    dict(k='cine', name='Cine', amt='−18,00 €', date='14/11/2026', kind='norm'),
]
# guion (segundos locales de la escena)
B = dict(ready=0.8, tap_edit=2.6, tap_cat=3.6, tap_reg=4.5, scr_net=(4.95, 5.65), hl_net=5.7, tap_net=7.0,
         scr_gym=(7.45, 8.15), tap_gym=9.0, footer=9.55, scr_end=(9.55, 10.2), tap_group=10.5, done=10.85)

def _check(d, x, y, on, s=22):
    if on:
        R.rrect(d, (x, y, x + s, y + s), 5, fill=BTN)
        d.line((x + 5, y + s / 2, x + s / 2 - 1, y + s - 6), fill=(255, 255, 255), width=3)
        d.line((x + s / 2 - 1, y + s - 6, x + s - 5, y + 6), fill=(255, 255, 255), width=3)
    else:
        R.rrect(d, (x, y, x + s, y + s), 5, outline=(180, 175, 195), width=2)

def _btn(d, box, label, primary, size=15):
    if primary: R.rrect(d, box, 12, fill=BTN)
    else: R.rrect(d, box, 12, fill=(255, 255, 255), outline=(210, 206, 224), width=2)
    f = I("SemiBold" if primary else "Medium", size)
    x0, y0, x1, y1 = box
    d.text(((x0 + x1 - d.textlength(label, font=f)) / 2, (y0 + y1) / 2 - size * 0.62), label, font=f,
           fill=(255, 255, 255) if primary else (45, 40, 70))

def _field(d, x, y, w, label, value, focus=False, arrow=False):
    d.text((x, y), label, font=I("Regular", 13), fill=GREY)
    R.rrect(d, (x, y + 20, x + w, y + 58), 10, fill=(255, 255, 255), outline=(150, 100, 235) if focus else (214, 210, 228), width=2)
    d.text((x + 12, y + 29), value, font=I("Regular", 15), fill=DARK)
    if arrow:
        ax, ay = x + w - 20, y + 37
        d.line((ax - 5, ay - 2, ax, ay + 3), fill=GREY, width=2); d.line((ax, ay + 3, ax + 5, ay - 2), fill=GREY, width=2)

def _head(d, m, checked=None):
    d.text((18, 16), m['name'], font=I("SemiBold", 19), fill=DARK)
    if checked is not None: _check(d, CW - 40, 16, checked)

def _base(h, fill=(255, 255, 255), outline=LINE, w=2):
    im = Image.new('RGBA', (CW, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    R.rrect(d, (0, 0, CW - 1, h - 1), 20, fill=fill, outline=outline, width=w)
    return im, d

def card(m, state, t=0.0):
    """returns (image, {button: box in card coords})"""
    btns = {}
    if state == 'done':        # fila compacta tras registrar
        planned = m['kind'] == 'plan'
        im, d = _base(64, fill=(250, 248, 255) if planned else (255, 255, 255), outline=POUT if planned else LINE)
        d.ellipse((16, 18, 44, 46), fill=(232, 222, 255) if planned else (220, 243, 230))
        col = BTN if planned else GREEN
        d.line((23, 32, 28, 38), fill=col, width=3); d.line((28, 38, 37, 25), fill=col, width=3)
        d.text((56, 10), m['name'], font=I("SemiBold", 17), fill=DARK)
        sub = "Pago planificado de noviembre · pagado" if planned else "Registrado"
        d.text((56, 34), sub, font=I("Medium", 13), fill=col)
        d.text((CW - 18 - d.textlength(m['amt'], font=I("SemiBold", 17)), 20), m['amt'], font=I("SemiBold", 17), fill=DARK)
        return im, btns
    if state == 'edit':
        im, d = _base(330, outline=(190, 160, 245))
        _head(d, m)
        d.text((CW - 18 - d.textlength("Cerrar edición", font=I("Medium", 13)), 20), "Cerrar edición", font=I("Medium", 13), fill=BTN)
        fw = (CW - 36 - 12) / 2; x2 = 18 + fw + 12
        _field(d, 18, 52, fw, "Importe", "3,50 €"); _field(d, x2, 52, fw, "Fecha", "10/11/2026")
        cat = "Cafeterías" if t >= B['tap_cat'] + 0.3 else "Sin categoría"
        _field(d, 18, 122, fw, "Tipo", "Gasto", arrow=True)
        _field(d, x2, 122, fw, "Categoría (opcional)", cat, arrow=True, focus=B['tap_cat'] <= t < B['tap_cat'] + 0.9)
        btns['cat'] = (x2, 142, x2 + fw, 180)
        _field(d, 18, 192, CW - 36, "Descripción", "Café")
        b = (18, 268, CW - 18, 310); _btn(d, b, "Registrar movimiento", True); btns['reg'] = b
        return im, btns
    if m['kind'] == 'plan':
        hl = state == 'hl'
        im, d = _base(368, outline=(170, 120, 245) if hl else LINE, w=3 if hl else 2)
        _head(d, m, checked=False)
        d.text((18, 46), m['amt'], font=I("Bold", 27), fill=DARK)
        d.text((18, 86), f"{m['date']} · Gasto", font=I("Regular", 14), fill=GREY)
        bx = (18, 116, CW - 18, 250)
        R.rrect(d, bx, 14, fill=PBOX, outline=POUT, width=2)
        d.ellipse((32, 133, 42, 143), fill=(150, 80, 240))
        d.text((52, 127), "Puede corresponder a un pago planificado", font=I("SemiBold", 14), fill=BTN)
        d.text((52, 149), "Encontramos un pago previsto compatible.", font=I("Regular", 13), fill=GREY)
        d.line((32, 176, CW - 32, 176), fill=POUT, width=1)
        for i, (a, b2) in enumerate([("Pago", m['pay']), ("Importe previsto", m['exp']), ("Vencimiento", m['due'] + " · Recurrente fijo")]):
            y = 184 + i * 21
            d.text((32, y), a + ":", font=I("Regular", 13), fill=GREY)
            d.text((32 + d.textlength(a + ": ", font=I("Regular", 13)), y), b2, font=I("SemiBold", 13), fill=DARK)
        b1 = (18, 264, CW - 18, 306); _btn(d, b1, "Sí, corresponde a este pago", True); btns['yes'] = b1
        b3 = (18, 314, CW - 18, 352); _btn(d, b3, "Registrar normalmente", False, 14)
        return im, btns
    # normal / edit-collapsed
    im, d = _base(178)
    _head(d, m, checked=(m['kind'] == 'norm'))
    d.text((18, 46), m['amt'], font=I("Bold", 27), fill=DARK)
    d.text((18, 86), f"{m['date']} · Gasto", font=I("Regular", 14), fill=GREY)
    chip = "Parece nuevo"; cw = d.textlength(chip, font=I("Medium", 12)) + 18
    x = 18 + d.textlength(f"{m['date']} · Gasto", font=I("Regular", 14)) + 10
    R.rrect(d, (x, 84, x + cw, 106), 8, fill=(240, 238, 246)); d.text((x + 9, 88), chip, font=I("Medium", 12), fill=(80, 75, 100))
    bw = (CW - 36 - 10) / 2
    b1 = (18, 122, 18 + bw, 162); _btn(d, b1, "Editar datos", False, 14); btns['edit'] = b1
    b2 = (28 + bw, 122, CW - 18, 162); _btn(d, b2, "Registrar movimiento", True, 14)
    return im, btns

def _state_times(m):
    """[(time, state)] transitions for each card"""
    k = m['k']
    if k == 'cafe': return [(0, 'norm'), (B['tap_edit'] + 0.1, 'edit'), (B['tap_reg'] + 0.2, 'done')]
    if k == 'net': return [(0, 'plan'), (B['hl_net'], 'hl'), (B['tap_net'] + 0.2, 'done')]
    if k == 'gym': return [(0, 'plan'), (B['tap_gym'] - 1.2, 'hl'), (B['tap_gym'] + 0.2, 'done')]
    return [(0, 'norm'), (B['tap_group'] + 0.25 + (0.12 if k == 'cine' else 0), 'done')]

TR = 0.32
def card_at(m, t):
    st = _state_times(m)
    cur = max(i for i, (tt, _) in enumerate(st) if tt <= t)
    a_img, a_b = card(m, st[cur][1], t)
    if cur > 0 and t - st[cur][0] < TR:
        p = ease((t - st[cur][0]) / TR)
        b_img, _ = card(m, st[cur - 1][1], t)
        h = int(b_img.size[1] + (a_img.size[1] - b_img.size[1]) * p)
        if st[cur][1] == 'hl':   # same size: plain crossfade
            return Image.blend(b_img, a_img, p), a_b
        out = Image.new('RGBA', (CW, h), (0, 0, 0, 0))
        top = b_img.crop((0, 0, CW, min(h, b_img.size[1]))); top.putalpha(top.getchannel('A').point(lambda v: int(v * (1 - p))))
        bot = a_img.crop((0, 0, CW, min(h, a_img.size[1]))); bot.putalpha(bot.getchannel('A').point(lambda v: int(v * p)))
        out.alpha_composite(top); out.alpha_composite(bot)
        d = ImageDraw.Draw(out)   # keep a clean bottom edge while resizing
        R.rrect(d, (0, 0, CW - 1, h - 1), 20, outline=LINE, width=2)
        return out, a_b
    return a_img, a_b

def layout(t):
    """content canvas pieces: list of (m, img, y, buttons) and total height"""
    y = 138; out = []
    for n, m in enumerate(MOVES):
        img, bt = card_at(m, t)
        out.append((m, img, y, bt)); y += img.size[1] + 14
    return out, y + 40

def _target(t_end, key):
    items, total = layout(t_end)
    vh = SH - TOP - NAVH - (110 if t_end >= B['footer'] else 0)
    if key == 'end': return max(0, total - vh)
    y = next(yy for m, _, yy, _ in items if m['k'] == key)
    return max(0, min(y - 12, total - vh))

_KF = None
_TAPS = {}
def scroll(t):
    global _KF
    if _KF is None:
        _KF = [(B['scr_net'], _target(B['scr_net'][1] + 0.4, 'net')), (B['scr_gym'], _target(B['scr_gym'][1] + 0.4, 'gym')),
               (B['scr_end'], _target(B['footer'] + 0.1, 'end')), ((B['done'] + 0.15, B['done'] + 0.75), 0.0)]
    v = 0.0
    for (a, b), tgt in _KF:
        if t >= a: v = v + (tgt - v) * ease((t - a) / (b - a))
    return v

def scr_bandeja(t):
    s = Image.new("RGB", (SW, SH), L.LIGHT); d = ImageDraw.Draw(s, "RGBA")
    # scrolling content
    can = Image.new('RGBA', (SW, 2600), L.LIGHT + (255,)); cd = ImageDraw.Draw(can)
    cd.text((22, 8), "← Volver a movimientos", font=I("Medium", 15), fill=BTN)
    n_left = 5
    cd.text((22, 40), "Hemos preparado 5 movimientos", font=I("Bold", 24), fill=DARK)
    cd.text((22, 76), "Revisa los que quieras registrar antes", font=I("Regular", 15), fill=GREY)
    cd.text((22, 96), "de confirmar.", font=I("Regular", 15), fill=GREY)
    items, total = layout(t)
    taps = _TAPS
    for n, (m, img, y, bt) in enumerate(items):
        p = ease((t - B['ready'] - n * 0.1) / 0.3)
        if p <= 0: continue
        if p < 1:
            img = img.copy(); img.putalpha(img.getchannel('A').point(lambda v: int(v * p)))
        can.alpha_composite(img, (20, int(y + (1 - p) * 18)))
        for name, (x0, y0, x1, y1) in bt.items():
            taps[(m['k'], name)] = (20 + (x0 + x1) / 2, y + (y0 + y1) / 2)
    vh = SH - TOP - NAVH - (110 if t >= B['footer'] else 0)
    sc = max(0, min(scroll(t), total - vh))
    s.paste(can.crop((0, int(sc), SW, int(sc) + SH - TOP)).convert('RGB'), (0, TOP))
    # preparing overlay
    if t < B['ready'] + 0.2:
        a = 1 - ease((t - B['ready']) / 0.2)
        d.rectangle((0, TOP + 130, SW, SH), fill=L.LIGHT + (int(255 * a),))
        pr = ease(t / B['ready'])
        d.text((SW / 2 - d.textlength("Preparando movimientos…", font=I("Medium", 17)) / 2, 470), "Preparando movimientos…",
               font=I("Medium", 17), fill=GREY + (int(255 * a),))
        R.rrect(d, (120, 510, SW - 120, 518), 4, fill=(232, 226, 245, int(255 * a)))
        R.rrect(d, (120, 510, 120 + (SW - 240) * pr, 518), 4, fill=BTN + (int(255 * a),))
    # fixed header
    d.rectangle((0, 0, SW, TOP), fill=L.LIGHT)
    R.status_bar(d)
    s.paste(L.LOGO.resize((40, 48)), (28, 74))
    d.text((74, 72), "propera", font=R.F(R.POP, 38), fill=DARK)
    d.ellipse((SW - 76, 74, SW - 30, 120), fill=(236, 228, 255)); d.text((SW - 59, 85), "L", font=I("SemiBold", 18), fill=BTN)
    d.line((0, TOP - 1, SW, TOP - 1), fill=(236, 234, 244), width=2)
    # sticky group footer
    def sy(k, b):
        x, y = taps[(k, b)]; return x, y - sc + TOP
    if t >= B['footer']:
        p = ease((t - B['footer']) / 0.35)
        fy = SH - NAVH - 110 + (1 - p) * 110
        d.rectangle((0, fy, SW, SH - NAVH), fill=(255, 255, 255)); d.line((0, fy, SW, fy), fill=(232, 230, 240), width=2)
        if t < B['done']:
            d.text((24, fy + 12), "Registro en grupo · Farmacia y Cine", font=I("Regular", 14), fill=GREY)
            _btn(d, (20, fy + 40, SW - 20, fy + 92), "Registrar 2 movimientos", True, 17)
            L.tap(d, SW / 2, fy + 66, t, B['tap_group'])
        else:
            q = ease((t - B['done']) / 0.3)
            R.rrect(d, (20, fy + 26, SW - 20, fy + 86), 14, fill=(232, 247, 238, int(255 * q)))
            lb = "✓  5 movimientos revisados"
            f = I("SemiBold", 18)
            d.text(((SW - d.textlength(lb, font=f)) / 2, fy + 44), lb, font=f, fill=GREEN + (int(255 * q),))
    L._nav(d, s, active="Movimientos")
    # taps
    for k, b, t0 in (('cafe', 'edit', B['tap_edit']), ('cafe', 'cat', B['tap_cat']), ('cafe', 'reg', B['tap_reg']),
                     ('net', 'yes', B['tap_net']), ('gym', 'yes', B['tap_gym'])):
        if t0 - 0.1 <= t <= t0 + 0.55 and (k, b) in taps:
            x, y = sy(k, b); L.tap(d, x, y, t, t0)
    return s

if __name__ == '__main__':
    for tt in [0.3, 1.5, 2.8, 3.95, 4.6, 5.2, 6.2, 7.1, 7.6, 8.4, 9.1, 9.7, 10.4, 10.6, 11.3]:
        R.phone(scr_bandeja(tt), 0.6).save(f'/tmp/b_{tt:05.2f}.png')

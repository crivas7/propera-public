"""Reel Lucía v16: Bandeja rediseñada dentro del móvil (revisión, Netflix y gimnasio como pagos planificados, registro en grupo) y final completo de Lucía."""
import json, os, subprocess, sys
sys.path.insert(0, '/home/claude/work')
os.chdir('/home/claude')
from PIL import Image, ImageDraw, ImageFilter
import render as R, lucia_screens as L, endcard as EC
import lucia_reel as LR   # clips, darken_top, soft, placeholder
import bandeja as BJ

W, H, FPS = 1080, 1920, 30
K = 1.07
V, V2, V4 = 'work/voice/voz_lucia.mp3', 'work/voice/voz_lucia_s2.mp3', 'work/voice/voz_lucia_s4b.mp3'
M = 'propera-public/685446693-60628f34-2042-4e8a-bd58-d5e154bd5059.mp4'
S1 = Image.open('work/01-captura-pendientes_eur.png').convert('RGB')
S2 = Image.open('work/02-revision-confirmacion_eur.png').convert('RGB')
S3 = Image.open('work/03-posible-pago-planificado_eur.png').convert('RGB')

# ---------------- voice timeline ----------------
SEGS = [  # name, input, start, end, subtitle parts (src-relative)
    ('s1', 1, 0.00, 3.33, []),
    ('s2', 2, 0.00, 3.70, [("Día veinte.", 0.0, 0.81), ("El banco dice 640 €…", 1.28, 3.66)]),
    ('s3', 1, 10.70, 16.36, [("¿Apuntarlos uno a uno?", 0.0, 1.29), ("Ni de broma.", 1.6, 2.4),
                             ("Hace una sola captura del banco y se la pasa a Propera.", 2.4, 5.66)]),
    ('s4a', 5, 0.00, 2.40, [("Propera saca todos los movimientos de golpe…", 0.0, 2.36)]),
    ('s4b', 5, 2.64, 7.70, [("…y reconoce el Netflix y el gimnasio…", 0.0, 2.36), ("…como pagos planificados…", 2.36, 3.56),
                            ("…para no contarlos dos veces.", 3.56, 5.01)]),
    ('s5', 1, 23.00, 26.40, [("640 € en el banco…", 0.0, 1.92), ("…99 € de verdad.", 2.26, 3.37)]),
    ('s5b', 6, 0.00, 3.47, [("Y lo ha resuelto en un momento.", 0.0, 1.77)]),
    ('s6', 1, 28.95, 32.68, []),
]
T = dict(A=0.0, B=3.56, C=7.32, D=12.3, E=24.0, F=27.6, G=33.2)
START = {'s1': 0.15, 's2': 3.61, 's3': 7.42, 's4a': 13.05, 's4b': 17.4, 's5': 24.2, 's5b': 29.1, 's6': 33.4}
DUR = 37.6

L.CAP2.update(tap_reg=1.2, sheet=1.5, tap_plus=2.5, opts=2.8, tap_img=4.2, read=99, lst=99, hl=99, conf=99, pend=99)
L.AV.update(box=START['s5'] + 2.26 / K - T['E'])

# ---------------- helpers ----------------
def ease(x): return R.ease(x)
PX0, PY0, PX1, PY1 = 60, 320, 1020, 1320          # panel on the frame
PW, PH = PX1 - PX0, PY1 - PY0
_pmask = Image.new('L', (PW, PH), 0); ImageDraw.Draw(_pmask).rounded_rectangle((0, 0, PW - 1, PH - 1), 40, fill=255)

def panel(im, content):
    """content: PIL image PWxPH"""
    sh = Image.new('RGBA', (PW + 120, PH + 120), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((60, 75, PW + 60, PH + 70), 44, fill=(0, 0, 0, 140))
    sh = sh.filter(ImageFilter.GaussianBlur(30))
    im.paste(sh, (PX0 - 60, PY0 - 60), sh)
    im.paste(content, (PX0, PY0), _pmask)

def window(src, y0, x0=0, cw=640):
    """crop a window of the screenshot (cw wide) scaled to the panel"""
    ch = int(cw * PH / PW)
    y0 = max(0, min(src.size[1] - ch, int(y0)))
    return src.crop((x0, y0, x0 + cw, y0 + ch)).resize((PW, PH), Image.LANCZOS), y0, PW / cw

def tap_at(im, x, y, t, t0):
    d = ImageDraw.Draw(im, 'RGBA'); k = (t - t0) / 0.55
    if 0 <= k <= 1:
        r = 26 + 60 * k
        d.ellipse((x - r, y - r, x + r, y + r), outline=(110, 60, 210, int(230 * (1 - k))), width=7)
        d.ellipse((x - 24, y - 24, x + 24, y + 24), fill=(110, 60, 210, int(150 * (1 - k))))

def label(im, lines, t, start=0.0):
    R.headline(im, lines, 120, t, 66, start=start)

# net card composite (card + its own CTA, from capture 3; the movement it belongs to is not shown)
_card = S3.crop((60, 3340, 580, 3850)); _btn = S3.crop((60, 4795, 580, 4900))
NET = Image.new('RGB', (700, 700 * PH // PW), (255, 255, 255))
NET.paste(_card, (90, 40)); NET.paste(_btn, (90, 40 + _card.size[1] + 30))

# ---------------- scenes ----------------
def bg_time(tg):
    """reloj del clip de fondo: tiempo real hasta la Bandeja y después avance lento, siempre hacia delante"""
    return tg if tg < T['D'] else min(16.6, T['D'] + (tg - T['D']) * 0.28)

def bg_clip(t_glob):
    return LR.soft(LR.clip(LR.L2, 'work/l2', bg_time(t_glob), ''))

def sA(t): return LR.sA(t)

def sB(t):
    return LR.sB(t)

def sC(t):
    im = bg_clip(T['C'] + t)
    R.headline(im, [("Con Propera", R.PURPLE)], 115, t + 1, 76)
    R.paste_phone(im, R.phone(L.scr_capture2(t), 0.95), W / 2, 230)
    return im

DLAB = [(0.0, [("5 movimientos preparados", R.PURPLE)]), (2.45, [("Lucía revisa…", R.WHITE)]),
        (4.95, [("¿Es un pago planificado?", R.PURPLE)]), (9.5, [("…y registra el resto.", R.WHITE)])]
def sD(t):
    im = bg_clip(T['D'] + t)
    a, lines = [x for x in DLAB if x[0] <= t][-1]
    R.headline(im, lines, 115, t - a + (1 if a == 0 else 0), 66)
    R.paste_phone(im, R.phone(BJ.scr_bandeja(t), 0.95), W / 2, 230)
    return im

def sE(t):
    im = bg_clip(T['E'] + t)
    R.headline(im, [("Con Propera", R.PURPLE)], 115, t + 1, 76)
    R.paste_phone(im, R.phone(L.scr_avail2(t), 0.95), W / 2, 230)
    return im

def sF(t):
    im = LR.darken_top(LR.clip(LR.L4, 'work/l4', t, ''))
    d = ImageDraw.Draw(im, 'RGBA')
    f = R.F(R.POP, 80); l1 = "640 € en el banco."
    p = ease((t - 0.1) / 0.3); w = d.textlength(l1, font=f)
    d.text(((W - w) / 2, 170 + (1 - p) * 40), l1, font=f, fill=(255, 255, 255, int(255 * p)))
    sp = ease((t - 0.35) / 0.35)
    if sp > 0:
        d.line(((W - w) / 2 - 10, 228, (W - w) / 2 - 10 + (w + 20) * sp, 228), fill=R.PURPLE, width=9)
    R.headline(im, [("99 € de verdad.", R.PURPLE)], 280, t, 88, start=0.45)
    q = ease((t - (START['s5b'] + 2.4 / K - T['F'])) / 0.4)
    if q > 0:
        d = ImageDraw.Draw(im, 'RGBA')
        d.rounded_rectangle((110, 1320 + (1 - q) * 30, 970, 1530 + (1 - q) * 30), 34, fill=(14, 9, 32, int(205 * q)))
        f1, f2 = R.F(R.POP, 68), R.F(R.POPM, 36)
        for s_, f_, y_, c_ in (("Así de fácil.", f1, 1345, (255, 255, 255)), ("Propera prepara. Tú revisas y confirmas.", f2, 1450, R.PURPLE)):
            d.text(((W - d.textlength(s_, font=f_)) / 2, y_ + (1 - q) * 30), s_, font=f_, fill=c_ + (int(255 * q),))
    return im

def sG(t): return EC.endcard(t, cta_at=START['s6'] + 0.78 / K - T['G'], link_at=START['s6'] + 2.6 / K - T['G'])

SC = [('A', sA), ('B', sB), ('C', sC), ('D', sD), ('E', sE), ('F', sF), ('G', sG)]
keys = list(T.keys())
R.SCENES[:] = [(T[k], (T[keys[i + 1]] if i + 1 < len(keys) else DUR), fn) for i, (k, fn) in enumerate(SC)]
LR.T.update(T)

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'out/propera_reel_lucia_v17.mp4'
    only = os.environ.get('ONLY')
    if only:
        os.makedirs('work/t16', exist_ok=True)
        for x in only.split(','):
            R.frame(float(x)).save(f'work/t16/{float(x):06.2f}.png')
        sys.exit()
    # subtitles
    cues = []
    for name, inp, a, b, parts in SEGS:
        st = START[name]
        for txt, r0, r1 in parts:
            cues.append((round(st + r0 / K, 2), round(st + r1 / K + 0.05, 2), txt))
    src = open('work/subs_lucia.py').read()
    i = src.index('CUES = ['); j = src.index(']\n', i) + 2
    open('work/subs_v16.py', 'w').write(src[:i] + 'CUES = ' + json.dumps(cues, ensure_ascii=False) + '\n' + src[j:])
    # sfx
    from sfx_pro import make, add, whoosh, soft_tap, detect_soft, success_soft, save
    o = make(DUR)
    for k in ('B', 'C', 'D', 'E', 'F', 'G'): add(o, whoosh(a=0.05), T[k] - 0.22)
    for tt in (L.CAP2['tap_reg'], L.CAP2['tap_plus'], L.CAP2['tap_img']): add(o, soft_tap(), T['C'] + tt)
    Bb = BJ.B
    for k in ('tap_edit', 'tap_cat', 'tap_reg', 'tap_net', 'tap_gym', 'tap_group'): add(o, soft_tap(), T['D'] + Bb[k])
    add(o, detect_soft(), T['D'] + Bb['hl_net']); add(o, detect_soft(), T['D'] + Bb['tap_gym'] - 1.2)
    add(o, success_soft(a=0.04), T['D'] + Bb['done'])
    add(o, success_soft(), T['E'] + L.AV['box'])
    save(o, 'work/sfx_v16.wav')
    # frames
    subprocess.run('rm -rf work/f16 work/f16s && mkdir -p work/f16', shell=True, check=True)
    for k in range(int(DUR * FPS)):
        R.frame(k / FPS).save(f'work/f16/{k:04d}.png')
    subprocess.run(['python3', 'work/subs_v16.py', 'work/f16', 'work/f16s'], check=True)
    fc, labels = [], []
    for n, (name, inp, a, b, _) in enumerate(SEGS):
        ms = int(START[name] * 1000)
        fc.append(f"[{inp}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,atempo={K},adelay={ms}|{ms}[v{n}]"); labels.append(f"[v{n}]")
    fc.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0,apad,atrim=0:{DUR},asplit[vo][sc]")
    fc.append(f"[3:a]aloop=loop=1:size=2147483647,apad,atrim=0:{DUR},volume=0.5,afade=t=out:st={DUR-1.7}:d=1.7[mu]")
    fc.append("[mu][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=350[duck]")
    fc.append("[4:a]aformat=channel_layouts=stereo,volume=0.9[fx]")
    fc.append("[vo][duck][fx]amix=inputs=3:normalize=0,alimiter=limit=0.95[aout]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '30', '-i', 'work/f16s/%04d.png', '-i', V, '-i', V2, '-i', M,
                    '-i', 'work/sfx_v16.wav', '-i', V4, '-i', 'work/voice/voz_lucia_facil.mp3', '-filter_complex', ";".join(fc), '-map', '0:v', '-map', '[aout]',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
                    '-t', str(DUR), '-movflags', '+faststart', out], check=True)
    print('done', out)

"""Reel Lucía v15: Bandeja real de Propera (capturas auténticas, EUR→€), revisión y confirmación por la usuaria."""
import json, os, subprocess, sys
sys.path.insert(0, '/home/claude/work')
os.chdir('/home/claude')
from PIL import Image, ImageDraw, ImageFilter
import render as R, lucia_screens as L, endcard as EC
import lucia_reel as LR   # clips, darken_top, soft, placeholder

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
    ('s4', 5, 0.00, 2.40, [("Propera saca todos los movimientos de golpe…", 0.0, 2.36)]),
    ('s5', 1, 23.00, 26.40, [("640 € en el banco…", 0.0, 1.92), ("…99 € de verdad.", 2.26, 3.37)]),
    ('s6', 1, 28.95, 32.68, []),
]
T = dict(A=0.0, B=3.56, C=7.32, D=12.3, E=20.5, F=24.3, G=26.9)
START = {'s1': 0.15, 's2': 3.61, 's3': 7.42, 's4': 12.95, 's5': 20.7, 's6': 27.1}
DUR = 31.3
D1, D2, D3, D4 = 0.0, 2.5, 4.4, 6.4     # sub-scenes inside D (local)
DLEN = T['E'] - T['D']

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
def bg_clip(t_glob):
    return LR.soft(LR.clip(LR.L2, 'work/l2', min(16.6, t_glob * 0.45 + 2), ''))

def sA(t): return LR.sA(t)

def sB(t):
    return LR.sB(t)

def sC(t):
    im = bg_clip(T['C'] + t)
    R.headline(im, [("Con Propera", R.PURPLE)], 115, t + 1, 76)
    R.paste_phone(im, R.phone(L.scr_capture2(t), 0.95), W / 2, 230)
    return im

def sD(t):
    im = bg_clip(T['D'] + t)
    if t < D2:   # Bandeja: preparados para revisar
        u = t - D1; y = 150 + 190 * ease((u - 0.8) / 1.5)
        c, _, _ = window(S1, y); panel(im, c)
        label(im, [("Una captura.", R.WHITE), ("Movimientos preparados", R.PURPLE)], u)
    elif t < D3:  # revisión individual del Café
        u = t - D2; y = 600 + 950 * ease(u / 1.3)
        c, y0, sc = window(S2, y); panel(im, c)
        label(im, [("Lucía revisa…", R.WHITE)], u)
        tap_at(im, PX0 + 320 * sc, PY0 + (2088 - y0) * sc, u, 1.45)
    elif t < D4:  # posible pago planificado: ella decide
        u = t - D3
        c = NET.resize((PW, PH), Image.LANCZOS); panel(im, c)
        label(im, [("…decide si es un", R.WHITE), ("pago planificado…", R.PURPLE)], u)
    else:        # registro en grupo de los 3 que eligió
        u = t - D4
        c, y0, sc = window(S1, 3730, x0=5, cw=600); panel(im, c)
        label(im, [("…y confirma.", R.WHITE)], u)
        tap_at(im, PX0 + (320 - 5) * sc, PY0 + (4124 - y0) * sc, u, 1.0)
    return im

def sE(t):
    im = bg_clip(T['E'] + t)
    R.headline(im, [("Con Propera", R.PURPLE)], 115, t + 1, 76)
    R.paste_phone(im, R.phone(L.scr_avail2(t), 0.95), W / 2, 230)
    return im

def sF(t):
    im = LR.sE(t)
    d = ImageDraw.Draw(im, 'RGBA')
    p = ease((t - 0.5) / 0.4)
    if p > 0:
        f = R.F(R.POP, 46)
        for i, (s, col) in enumerate([("Propera prepara tus movimientos.", (255, 255, 255)), ("Tú los revisas y confirmas.", R.PURPLE)]):
            w = d.textlength(s, font=f); x = (W - w) / 2; y = 1330 + i * 64
            if i == 0: d.rounded_rectangle((90, 1310, 990, 1460), 30, fill=(14, 9, 32, int(200 * p)))
            d.text((x, y), s, font=f, fill=col + (int(255 * p),))
    return im

def sG(t): return EC.endcard(t, cta_at=START['s6'] + 0.78 / K - T['G'], link_at=START['s6'] + 2.6 / K - T['G'])

SC = [('A', sA), ('B', sB), ('C', sC), ('D', sD), ('E', sE), ('F', sF), ('G', sG)]
keys = list(T.keys())
R.SCENES[:] = [(T[k], (T[keys[i + 1]] if i + 1 < len(keys) else DUR), fn) for i, (k, fn) in enumerate(SC)]
LR.T.update(T)

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'out/propera_reel_lucia_v15.mp4'
    only = os.environ.get('ONLY')
    if only:
        os.makedirs('work/t15', exist_ok=True)
        for x in only.split(','):
            R.frame(float(x)).save(f'work/t15/{float(x):06.2f}.png')
        sys.exit()
    # subtitles
    cues = []
    for name, inp, a, b, parts in SEGS:
        st = START[name]
        for txt, r0, r1 in parts:
            cues.append((round(st + r0 / K, 2), round(st + r1 / K + 0.05, 2), txt))
    src = open('work/subs_lucia.py').read()
    i = src.index('CUES = ['); j = src.index(']\n', i) + 2
    open('work/subs_v15.py', 'w').write(src[:i] + 'CUES = ' + json.dumps(cues, ensure_ascii=False) + '\n' + src[j:])
    # sfx
    from sfx_pro import make, add, whoosh, soft_tap, detect_soft, success_soft, save
    o = make(DUR)
    for k in ('B', 'C', 'D', 'E', 'F', 'G'): add(o, whoosh(a=0.05), T[k] - 0.22)
    for tt in (L.CAP2['tap_reg'], L.CAP2['tap_plus'], L.CAP2['tap_img']): add(o, soft_tap(), T['C'] + tt)
    add(o, soft_tap(), T['D'] + D2 + 1.45); add(o, detect_soft(), T['D'] + D3 + 0.2); add(o, soft_tap(), T['D'] + D4 + 1.0)
    add(o, success_soft(), T['E'] + L.AV['box'])
    save(o, 'work/sfx_v15.wav')
    # frames
    subprocess.run('rm -rf work/f15 work/f15s && mkdir -p work/f15', shell=True, check=True)
    for k in range(int(DUR * FPS)):
        R.frame(k / FPS).save(f'work/f15/{k:04d}.png')
    subprocess.run(['python3', 'work/subs_v15.py', 'work/f15', 'work/f15s'], check=True)
    fc, labels = [], []
    for n, (name, inp, a, b, _) in enumerate(SEGS):
        ms = int(START[name] * 1000)
        fc.append(f"[{inp}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,atempo={K},adelay={ms}|{ms}[v{n}]"); labels.append(f"[v{n}]")
    fc.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0,apad,atrim=0:{DUR},asplit[vo][sc]")
    fc.append(f"[3:a]aloop=loop=1:size=2147483647,apad,atrim=0:{DUR},volume=0.5,afade=t=out:st={DUR-1.7}:d=1.7[mu]")
    fc.append("[mu][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=350[duck]")
    fc.append("[4:a]aformat=channel_layouts=stereo,volume=0.9[fx]")
    fc.append("[vo][duck][fx]amix=inputs=3:normalize=0,alimiter=limit=0.95[aout]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '30', '-i', 'work/f15s/%04d.png', '-i', V, '-i', V2, '-i', M,
                    '-i', 'work/sfx_v15.wav', '-i', V4, '-filter_complex', ";".join(fc), '-map', '0:v', '-map', '[aout]',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
                    '-t', str(DUR), '-movflags', '+faststart', out], check=True)
    print('done', out)

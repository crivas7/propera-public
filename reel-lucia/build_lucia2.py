"""Construye el reel de Lucía con una línea de tiempo calculada a partir de la voz (más compacta)."""
import json, os, subprocess, sys
sys.path.insert(0, '/home/claude/work')

K = 1.07          # velocidad de la voz
GAP = 0.3
V, V2, V4 = 'work/voice/voz_lucia.mp3', 'work/voice/voz_lucia_s2.mp3', 'work/voice/voz_lucia_s4b.mp3'
M = 'propera-public/685446693-60628f34-2042-4e8a-bd58-d5e154bd5059.mp4'
# (nombre, entrada ffmpeg, inicio, fin, [(texto, ini_rel, fin_rel) en tiempo de origen] )
SEGS = [
    ('s1', 1, 0.00, 3.33, []),
    ('s2', 2, 0.00, 6.58, [("Día veinte.", 0.0, 0.81), ("El banco dice 640 €…", 1.28, 3.66),
                           ("…y tiene un montón de movimientos sin revisar.", 4.09, 6.55)]),
    ('s3', 1, 10.70, 16.36, [("¿Apuntarlos uno a uno?", 0.0, 1.29), ("Ni de broma.", 1.6, 2.4),
                             ("Hace una sola captura del banco y se la pasa a Propera.", 2.4, 5.66)]),
    ('s4', 5, 0.00, 7.70, [("Propera saca todos los movimientos de golpe…", 0.0, 2.36),
                           ("…y reconoce el Netflix y el gimnasio…", 2.64, 5.0),
                           ("…como pagos planificados…", 5.0, 6.2), ("…para no contarlos dos veces.", 6.2, 7.65)]),
    ('s5a', 1, 23.00, 26.40, [("640 € en el banco…", 0.0, 1.92), ("…99 € de verdad.", 2.26, 3.37)]),
    ('s5b', 1, 26.73, 28.59, [("Y lo ha resuelto en diez segundos.", 0.0, 1.86)]),
    ('s6', 1, 28.95, 32.68, []),
]
GAPS = {'s2': 0.35, 's3': 0.35, 's4': 0.2, 's5a': 0.2, 's5b': 0.3, 's6': 0.35}

pos = {}; cur = 0.15
for name, inp, a, b, _ in SEGS:
    cur += GAPS.get(name, 0)
    d = (b - a) / K
    pos[name] = (cur, cur + d); cur += d

T = dict(A=0.0, B=round(pos['s2'][0] - 0.05, 2), C=round(pos['s3'][0] - 0.1, 2),
         E=round(pos['s5b'][0] - 0.6, 2), F=round(pos['s6'][0] - 0.15, 2))
DUR = round(pos['s6'][1] + 0.7, 2)
C = T['C']
lst = pos['s4'][0] - C
hl = pos['s4'][0] + 2.64 / K - C
pend = pos['s5a'][0] - C - 0.15
box = pos['s5a'][0] + 2.26 / K - (C + pend)
CAP2 = dict(tap_reg=1.0, sheet=1.3, tap_plus=2.0, opts=2.3, tap_img=3.0, read=3.4, lst=lst, hl=hl, conf=pend - 1.1, pend=pend)
AV = dict(box=box)
TL = dict(T=T, DUR=DUR, CAP2=CAP2, AV=AV)
print(json.dumps(TL, indent=1))

# subtítulos
cues = []
for name, inp, a, b, parts in SEGS:
    st = pos[name][0]
    for txt, r0, r1 in parts:
        cues.append((round(st + r0 / K, 2), round(st + r1 / K + 0.05, 2), txt))
src = open('work/subs_lucia.py').read()
i = src.index('CUES = ['); j = src.index(']\n', i) + 2
src = src[:i] + 'CUES = ' + json.dumps(cues, ensure_ascii=False) + '\n' + src[j:]
open('work/subs_lucia2.py', 'w').write(src)

# efectos
from sfx_pro import make, add, whoosh, soft_tap, detect_soft, success_soft, save
o = make(DUR)
for t in (T['B'], T['C'], T['E'], T['F']): add(o, whoosh(a=0.05), t - 0.22)
for t in (CAP2['tap_reg'], CAP2['tap_plus'], CAP2['tap_img']): add(o, soft_tap(), C + t)
add(o, detect_soft(), C + hl)
add(o, success_soft(), C + pend + box)
save(o, 'work/sfx_lucia2.wav')

# render
env = dict(os.environ, LTL=json.dumps(TL))
subprocess.run('rm -rf work/lf work/lfs', shell=True, check=True)
subprocess.run(['python3', 'work/lucia_reel.py', 'work/lf'], env=env, check=True)
subprocess.run(['python3', 'work/subs_lucia2.py', 'work/lf', 'work/lfs'], check=True)
fc = []
labels = []
for n, (name, inp, a, b, _) in enumerate(SEGS):
    ms = int(pos[name][0] * 1000)
    fc.append(f"[{inp}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,atempo={K},adelay={ms}|{ms}[v{n}]")
    labels.append(f"[v{n}]")
fc.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0,apad,atrim=0:{DUR},asplit[vo][sc]")
fc.append(f"[3:a]aloop=loop=1:size=2147483647,apad,atrim=0:{DUR},volume=0.5,afade=t=out:st={DUR-1.7}:d=1.7[mu]")
fc.append("[mu][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=350[duck]")
fc.append("[4:a]aformat=channel_layouts=stereo,volume=0.9[fx]")
fc.append("[vo][duck][fx]amix=inputs=3:normalize=0,alimiter=limit=0.95[aout]")
out = sys.argv[1] if len(sys.argv) > 1 else 'out/propera_reel_lucia_v14.mp4'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '30', '-i', 'work/lfs/%04d.png', '-i', V, '-i', V2, '-i', M,
                '-i', 'work/sfx_lucia2.wav', '-i', V4, '-filter_complex', ";".join(fc), '-map', '0:v', '-map', '[aout]',
                '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
                '-t', str(DUR), '-movflags', '+faststart', out], check=True)
print('done', out, DUR)

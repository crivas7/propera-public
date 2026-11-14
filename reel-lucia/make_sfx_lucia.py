# SFX de Lucía con paleta suave: toques suaves, marimba al detectar, contador suave + arpegio final
import sys; sys.path.insert(0, '/home/claude/work')
from sfx_pro import *
DUR = float(sys.argv[1]) if len(sys.argv) > 1 else 33.1
SHIFT = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0   # retraso extra tras la frase 4
C = 10.9
o = make(DUR)
for t in (4.0, 10.9): add(o, whoosh(a=0.05), t - 0.22)
for t in (25.4, 29.1): add(o, whoosh(a=0.05), t + SHIFT - 0.22)
for t in (1.2, 2.5, 3.9): add(o, soft_tap(), C + t)
add(o, detect_soft(), 20.3)
counter_soft(o, 22.75 + SHIFT, 24.75 + SHIFT)
add(o, success_soft(), 24.9 + SHIFT)
save(o, '/home/claude/work/sfx_lucia.wav')

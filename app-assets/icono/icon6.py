"""Icono v6 sobre la base del usuario: contorno algo menos redondo, fondo más lila, pupila del logo original."""
import numpy as np, scipy.ndimage as nd
from PIL import Image, ImageDraw, ImageFont, ImageFilter
N = 1024
base = np.array(Image.open('/mnt/user-data/uploads/b9163170-image.png').convert('RGB')).astype(float)
A = np.clip((base.min(2) - 150) / 95, 0, 1); white = A > 0.5
S_base = nd.binary_fill_holes(white)
# --- silueta oficial alineada
src = Image.open('/mnt/user-data/uploads/67c1b44e-image.png').convert('RGBA')
sa = np.array(src)[..., 3] > 128; l, n = nd.label(sa); sa = l == (1 + np.argmax(nd.sum(sa, l, range(1, n + 1))))
oy, ox = np.where(sa); OFF = Image.fromarray((sa[oy.min():oy.max() + 1, ox.min():ox.max() + 1] * 255).astype(np.uint8))
ry, rx = np.where(S_base); bw, bh = rx.max() - rx.min() + 1, ry.max() - ry.min() + 1
def place(sx, sy, tx, ty, k=1.0):
    c = Image.new('L', (round(N * k), round(N * k)), 0)
    c.paste(OFF.resize((max(1, round(bw * sx * k)), max(1, round(bh * sy * k))), Image.LANCZOS), (round((rx.min() + tx) * k), round((ry.min() + ty) * k)))
    return np.array(c)
k = 0.25; Sr = np.array(Image.fromarray((S_base * 255).astype(np.uint8)).resize((256, 256))) > 127; best = (0, None)
for sx in np.arange(0.95, 1.06, 0.01):
    for sy in np.arange(0.95, 1.06, 0.01):
        for tx in range(-16, 17, 4):
            for ty in range(-16, 17, 4):
                o = place(sx, sy, tx, ty, k) > 127; iou = (o & Sr).sum() / (o | Sr).sum()
                if iou > best[0]: best = (iou, (sx, sy, tx, ty))
S_off = place(*best[1]) > 127
# --- mezcla de contornos con distancias con signo: un poco hacia el oficial
def sdf(m): return nd.distance_transform_edt(m) - nd.distance_transform_edt(~m)
W = 0.75
S_close = nd.binary_fill_holes(nd.binary_closing(np.pad(S_base, 60), iterations=45))[60:-60, 60:-60]
concave = nd.binary_dilation(S_close & ~S_base, iterations=10)          # canales y entrantes: aquí no se toca nada
import cv2
cs, _ = cv2.findContours(S_base.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
hull = np.zeros((N, N), np.uint8); cv2.fillPoly(hull, [cv2.convexHull(np.vstack([c for c in cs if cv2.contourArea(c) > 2000]))], 1); hull = hull > 0
band = np.abs(sdf(hull)) < 14                                             # solo las esquinas exteriores (sobre la envolvente)
allow = nd.gaussian_filter((band & ~nd.binary_dilation(concave, iterations=12)).astype(float), 4)
SD = sdf(S_base) + W * allow * (sdf(S_off) - sdf(S_base))
sil = np.clip(SD / 1.2 + 0.5, 0, 1)                                     # borde antialiasado
base_soft = np.clip(sdf(S_base) / 1.2 + 0.5, 0, 1)
add = np.clip(sil - base_soft, 0, 1) * allow; rem = 0
mark = A * (1 - allow) + np.maximum(A, np.where(S_base | (base_soft > 0), sil, sil)) * allow
# --- pupila del logo original
a = np.array(src).astype(float); r, g, b = a[..., 0], a[..., 1], a[..., 2]; h, w = r.shape; Y, X = np.mgrid[0:h, 0:w]
cyan = (a[..., 3] > 128) & (b > 200) & (g > 150) & (r < 150)
cl, cn = nd.label(nd.binary_opening(cyan, iterations=2)); csz = nd.sum(cyan, cl, range(1, cn + 1))
icy, icx = nd.center_of_mass(cl == (1 + np.argmax(csz)))
near = np.hypot(Y - icy, X - icx) < 90
pup = nd.binary_opening(near & (a[..., 3] > 128) & (r > 150) & (g < 140) & (b > 150), iterations=2)
pl, pn = nd.label(pup); psz = nd.sum(pup, pl, range(1, pn + 1)); pup = pl == (1 + np.argmax(psz))
py, px = nd.center_of_mass(pup); pr = (pup.sum() / np.pi) ** 0.5
print('pupila original', round(py), round(px), round(pr, 1))
wl, wn = nd.label(white); comps = []
for i in range(1, wn + 1):
    m = wl == i; s = m.sum()
    if 300 < s < 20000:
        cy, cx = nd.center_of_mass(m); rr = (s / np.pi) ** 0.5
        circ = s / (np.pi * max(np.ptp(np.where(m)[0]), np.ptp(np.where(m)[1])) ** 2 / 4)
        comps.append((circ, i, cy, cx, rr))
_, pid, cy, cx, rr = max(comps)
print('ajuste', round(best[0], 3), 'pupila base', round(cy), round(cx), round(rr, 1))
R = pr * 0.97; crop = src.convert('RGB').crop((round(px - R), round(py - R), round(px + R), round(py + R)))
D = round(rr * 2 * 1.10); crop = crop.resize((D, D), Image.LANCZOS)
PUP = Image.new('RGB', (N, N)); PUP.paste(crop, (round(cx - D / 2), round(cy - D / 2)))
YY, XX = np.mgrid[0:N, 0:N]; pm = np.clip(D / 2 - 0.5 - np.hypot(YY - cy, XX - cx), 0, 1)

def bg(size):
    y, x = np.mgrid[0:size, 0:size] / size
    deep, mid, top, glow = np.array((86, 18, 220)), np.array((140, 52, 240)), np.array((182, 96, 254)), np.array((200, 116, 254))
    t = (1 - y)[..., None]
    c = np.where(t < 0.55, deep + (mid - deep) * (t / 0.55), mid + (top - mid) * ((t - 0.55) / 0.45))
    gl = (np.clip(1 - np.hypot(x - 0.95, y - 0.0) / 0.6, 0, 1) ** 2.2)[..., None] * 0.45
    return np.clip(c * (1 - gl) + glow * gl, 0, 255)

out = bg(N) * (1 - mark[..., None]) + 255 * mark[..., None]
out = out * (1 - pm[..., None]) + np.array(PUP).astype(float) * pm[..., None]
ICON = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)); ICON.save('/home/claude/out/icono_propera_v6_1024.png')

F = lambda s: ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Medium.otf', s)
def mask(s):
    m = Image.new('L', (s * 4, s * 4), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, s * 4 - 1, s * 4 - 1), s * 4 * 0.225, fill=255); return m.resize((s, s), Image.LANCZOS)
sh = Image.new('RGB', (1180, 800), (236, 234, 242)); d = ImageDraw.Draw(sh)
for i, (im, lab) in enumerate([(Image.open('/mnt/user-data/uploads/b9163170-image.png').convert('RGB'), 'Base'), (ICON, 'Ahora')]):
    x = 70 + i * 560; sh.paste(im.resize((480, 480), Image.LANCZOS), (x, 50), mask(480)); d.text((x + 240, 550), lab, font=F(28), fill=(50, 45, 75), anchor='ma')
    for j, s in enumerate((120, 76, 56)): sh.paste(im.resize((s, s), Image.LANCZOS), (x + 80 + j * 130, 630 + (120 - s) // 2), mask(s))
sh.save('/home/claude/out/icono_propera_v6_preview.png')
ICON.crop((380, 380, 720, 640)).resize((680, 520), Image.LANCZOS).save('/tmp/eye6.png')

"""Reconstruye el logo con bordes limpios: sin halo claro y con contorno suavizado a 4x."""
from PIL import Image, ImageFilter
import numpy as np, scipy.ndimage as nd
im = Image.open('/mnt/user-data/uploads/ac65a8dc-image.png').convert('RGB')
c = np.array(im.crop((652, 566, 900, 886))).astype(float)
bg = np.array([250., 248., 254.])
dist = np.sqrt(((c - bg) ** 2).sum(2)); fg = dist > 28
lab, _ = nd.label(~fg)
border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
solid = ~np.isin(lab, list(border))
core = nd.binary_erosion(solid, iterations=2)            # píxeles sin mezcla con el fondo
idx = nd.distance_transform_edt(~core, return_distances=False, return_indices=True)
col = c[idx[0], idx[1]]                                   # extiende el color interior hacia el borde
K = 4
big = Image.fromarray(col.astype(np.uint8)).resize((c.shape[1] * K, c.shape[0] * K), Image.BICUBIC)
big = big.filter(ImageFilter.UnsharpMask(radius=3, percent=60, threshold=2))
m = Image.fromarray((nd.binary_erosion(solid, iterations=1) * 255).astype(np.uint8)).resize(big.size, Image.BICUBIC)
m = np.array(m.filter(ImageFilter.GaussianBlur(3.2))).astype(float) / 255
a = np.clip((m - 0.5) * 5 + 0.5, 0, 1)                    # contorno nítido y antialiasado
out = Image.fromarray(np.dstack([np.array(big), (a * 255).astype(np.uint8)]), 'RGBA')
out = out.crop(out.getbbox()); out.save('logo_hq.png'); print(out.size)

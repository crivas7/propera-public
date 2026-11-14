"""Icono y splash de Propera para iOS (SwiftUI) y Android (Kotlin) a partir del logo oficial."""
import os, numpy as np
from PIL import Image, ImageDraw, ImageFilter
SRC = Image.open('/mnt/user-data/uploads/67c1b44e-image.png').convert('RGBA')
LOGO = SRC.crop(SRC.getbbox())
LIGHT = (245, 241, 255); DARK = (18, 12, 42)
OUT = '/home/claude/out/propera_app_assets'
def mk(p): os.makedirs(os.path.dirname(p), exist_ok=True); return p
def fit(h): return LOGO.resize((round(h * LOGO.width / LOGO.height), round(h)), Image.LANCZOS)
def centered(size, bg, logo_h, dx=0.012, circle=None):
    """lienzo cuadrado con el logo centrado (dx compensa el peso visual del pico)"""
    im = Image.new('RGBA', (size, size), bg if len(bg) == 4 else bg + (255,))
    if circle:
        r = size * circle / 2; ImageDraw.Draw(im).ellipse((size / 2 - r, size / 2 - r, size / 2 + r, size / 2 + r), fill=LIGHT + (255,))
    lg = fit(size * logo_h)
    im.alpha_composite(lg, (round((size - lg.width) / 2 + size * dx), round((size - lg.height) / 2)))
    return im

# ---------- iOS ----------
centered(1024, LIGHT, 0.62).convert('RGB').save(mk(f'{OUT}/ios/AppIcon.appiconset/AppIcon-1024.png'))
centered(1024, DARK, 0.62).convert('RGB').save(f'{OUT}/ios/AppIcon.appiconset/AppIcon-1024-dark.png')
g = centered(1024, (0, 0, 0), 0.62).convert('L').convert('RGB'); g.save(f'{OUT}/ios/AppIcon.appiconset/AppIcon-1024-tinted.png')
open(f'{OUT}/ios/AppIcon.appiconset/Contents.json', 'w').write('''{
  "images" : [
    { "filename" : "AppIcon-1024.png", "idiom" : "universal", "platform" : "ios", "size" : "1024x1024" },
    { "appearances" : [ { "appearance" : "luminosity", "value" : "dark" } ], "filename" : "AppIcon-1024-dark.png", "idiom" : "universal", "platform" : "ios", "size" : "1024x1024" },
    { "appearances" : [ { "appearance" : "luminosity", "value" : "tinted" } ], "filename" : "AppIcon-1024-tinted.png", "idiom" : "universal", "platform" : "ios", "size" : "1024x1024" }
  ],
  "info" : { "author" : "xcode", "version" : 1 }
}
''')
for name, circ in (('SplashLogo', None), ('SplashLogoDark', 1.0)):
    for sc in (1, 2, 3):
        s = 200 * sc
        im = centered(s, (0, 0, 0, 0), 0.60 if circ else 0.86, circle=circ)
        im.save(mk(f'{OUT}/ios/SplashLogo.imageset/{name}@{sc}x.png'))
open(f'{OUT}/ios/SplashLogo.imageset/Contents.json', 'w').write('''{
  "images" : [
    { "filename" : "SplashLogo@1x.png", "idiom" : "universal", "scale" : "1x" },
    { "filename" : "SplashLogo@2x.png", "idiom" : "universal", "scale" : "2x" },
    { "filename" : "SplashLogo@3x.png", "idiom" : "universal", "scale" : "3x" },
    { "appearances" : [ { "appearance" : "luminosity", "value" : "dark" } ], "filename" : "SplashLogoDark@1x.png", "idiom" : "universal", "scale" : "1x" },
    { "appearances" : [ { "appearance" : "luminosity", "value" : "dark" } ], "filename" : "SplashLogoDark@2x.png", "idiom" : "universal", "scale" : "2x" },
    { "appearances" : [ { "appearance" : "luminosity", "value" : "dark" } ], "filename" : "SplashLogoDark@3x.png", "idiom" : "universal", "scale" : "3x" }
  ],
  "info" : { "author" : "xcode", "version" : 1 }
}
''')
os.makedirs(f'{OUT}/ios/SplashBackground.colorset', exist_ok=True)
def comp(c): return ', '.join(f'"{k}" : "0x{v:02X}"' for k, v in zip(('red', 'green', 'blue'), c))
open(f'{OUT}/ios/SplashBackground.colorset/Contents.json', 'w').write('''{
  "colors" : [
    { "color" : { "color-space" : "srgb", "components" : { "alpha" : "1.000", %s } }, "idiom" : "universal" },
    { "appearances" : [ { "appearance" : "luminosity", "value" : "dark" } ], "color" : { "color-space" : "srgb", "components" : { "alpha" : "1.000", %s } }, "idiom" : "universal" }
  ],
  "info" : { "author" : "xcode", "version" : 1 }
}
''' % (comp(LIGHT), comp(DARK)))

# ---------- Android ----------
R = f'{OUT}/android/res'
# monocromo: silueta con ceja, ojo y brillo del pico calados
a = np.array(LOGO).astype(float); al = a[..., 3] / 255
lum = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
h = a.shape[0]; yy = np.arange(h)[:, None] / h
dark_line = (lum < 62) & (yy < 0.66)                       # ceja y contorno del ojo
bright = (a[..., 2] > 215) & (a[..., 0] < 150) & (lum > 150)   # iris y brillos cian
hole = Image.fromarray(((dark_line | bright) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
mono_a = np.clip(al * 255 - np.array(hole).astype(float), 0, 255).astype(np.uint8)
MONO = Image.merge('RGBA', [Image.new('L', LOGO.size, 255)] * 3 + [Image.fromarray(mono_a)])
def fg(size, logo, frac=0.50):
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0)); hh = size * frac
    lg = logo.resize((round(hh * logo.width / logo.height), round(hh)), Image.LANCZOS)
    im.alpha_composite(lg, (round((size - lg.width) / 2 + size * 0.008), round((size - lg.height) / 2))); return im
for d, px in (('mdpi', 108), ('hdpi', 162), ('xhdpi', 216), ('xxhdpi', 324), ('xxxhdpi', 432)):
    fg(px, LOGO).save(mk(f'{R}/mipmap-{d}/ic_launcher_foreground.png'))
    fg(px, MONO).save(f'{R}/mipmap-{d}/ic_launcher_monochrome.png')
    leg = px * 48 // 108                                      # icono clásico para Android < 8
    sq = centered(leg * 4, LIGHT, 0.62).resize((leg, leg), Image.LANCZOS)
    m = Image.new('L', (leg * 4, leg * 4), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, leg * 4 - 1, leg * 4 - 1), leg * 0.9, fill=255)
    sq.putalpha(m.resize((leg, leg), Image.LANCZOS)); sq.save(f'{R}/mipmap-{d}/ic_launcher.png')
    c = centered(leg * 4, LIGHT, 0.58).resize((leg, leg), Image.LANCZOS)
    m = Image.new('L', (leg * 4, leg * 4), 0); ImageDraw.Draw(m).ellipse((0, 0, leg * 4 - 1, leg * 4 - 1), fill=255)
    c.putalpha(m.resize((leg, leg), Image.LANCZOS)); c.save(f'{R}/mipmap-{d}/ic_launcher_round.png')
    sp = px * 288 // 108                                      # splash Android 12+: lienzo 288dp, contenido en círculo de 192dp
    fg(sp, LOGO, 0.40).save(mk(f'{R}/drawable-{d}/splash_icon.png'))
xml = '''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background" />
    <foreground android:drawable="@mipmap/ic_launcher_foreground" />
    <monochrome android:drawable="@mipmap/ic_launcher_monochrome" />
</adaptive-icon>
'''
for n in ('ic_launcher', 'ic_launcher_round'): open(mk(f'{R}/mipmap-anydpi-v26/{n}.xml'), 'w').write(xml)
hx = lambda c: '#%02X%02X%02X' % c
open(mk(f'{R}/values/propera_branding.xml'), 'w').write(f'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="ic_launcher_background">{hx(LIGHT)}</color>
    <color name="splash_background">{hx(LIGHT)}</color>
    <color name="splash_icon_background">{hx(LIGHT)}</color>

    <!-- Requiere: implementation("androidx.core:core-splashscreen:1.0.1") -->
    <style name="Theme.Propera.Splash" parent="Theme.SplashScreen">
        <item name="windowSplashScreenBackground">@color/splash_background</item>
        <item name="windowSplashScreenAnimatedIcon">@drawable/splash_icon</item>
        <item name="windowSplashScreenIconBackgroundColor">@color/splash_icon_background</item>
        <item name="postSplashScreenTheme">@style/Theme.Propera</item>
    </style>
</resources>
''')
open(mk(f'{R}/values-night/propera_branding.xml'), 'w').write(f'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="splash_background">{hx(DARK)}</color>
</resources>
''')
centered(512, LIGHT, 0.62).convert('RGB').save(mk(f'{OUT}/android/play_store_icon_512.png'))
LOGO.save(mk(f'{OUT}/master/logo_propera_transparente.png')); MONO.save(f'{OUT}/master/logo_propera_monocromo.png')
print('ok', LOGO.size)

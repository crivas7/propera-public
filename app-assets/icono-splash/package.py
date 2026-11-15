"""Paquete final Propera: icono (cian) + splash (lila #7C2CDE, halcón, parpadeo, 'propera.') para iOS (SwiftUI) y Android (Kotlin)."""
import os, json, shutil, numpy as np, scipy.ndimage as nd, cv2
from PIL import Image, ImageDraw, ImageFont
OUT = '/home/claude/out/propera_icono_splash'
shutil.rmtree(OUT, ignore_errors=True)
def mk(p): os.makedirs(os.path.dirname(p), exist_ok=True); return p
ICON = Image.open('/home/claude/out/icono_propera_final_1024.png').convert('RGB')
ic = np.array(ICON).astype(float); N = 1024
# ---------- capas del halcón (blanco, anillo del ojo, pupila) a partir del icono maestro
bgrow = ic[:, 40:80].mean(1); g = ic[..., 1]; bgG = bgrow[:, 1][:, None]
A = np.clip((g - bgG) / (255 - bgG), 0, 1); A = A * nd.binary_dilation(A > 0.5, iterations=3)
cyan = (ic[..., 1] > 150) & (ic[..., 0] < 120) & (ic[..., 2] > 200)
ys, xs = np.where(cyan); pcy, pcx = ys.mean(), xs.mean(); r = max(np.ptp(ys), np.ptp(xs)) / 2 + 4
Y, X = np.mgrid[0:N, 0:N]; pz = np.hypot(Y - pcy, X - pcx) < r
pupA = np.clip((g - 52) / (196 - 52), 0, 1) * pz
whA = np.where(pz, 0, A)
l, n = nd.label(whA > 0.5); sz = nd.sum(whA > 0.5, l, range(1, n + 1))
ringid = 1 + [i for i in range(n) if 1500 < sz[i] < 12000][0]
ringM = nd.binary_dilation(l == ringid, iterations=2) & ~nd.binary_dilation((whA > 0.5) & (l != ringid), iterations=1)
ringA = whA * ringM; bodyA = whA * ~ringM
def layer(alpha, rgb): return Image.fromarray(np.dstack([np.broadcast_to(np.array(rgb, float), alpha.shape + (3,)), alpha * 255]).astype(np.uint8), 'RGBA')
L_body, L_ring, L_pup = layer(bodyA, (255, 255, 255)), layer(ringA, (255, 255, 255)), layer(pupA, (56, 196, 248))
bb = Image.fromarray(((bodyA + ringA + pupA) > 0.02).astype(np.uint8) * 255).getbbox()
crop = lambda im: im.crop(bb)
L_body, L_ring, L_pup = map(crop, (L_body, L_ring, L_pup)); MW, MH = L_body.size
# ---------- lienzo común del splash: 288x288 unidades, halcón de 144 de alto centrado (cabe en el círculo de 192 de Android 12)
CAN = 288; HH = 144; HW = HH * MW / MH; OX = (CAN - HW) / 2 + 2; OY = (CAN - HH) / 2
def canvas(layers, px):
    s = px / CAN; im = Image.new('RGBA', (px, px), (0, 0, 0, 0))
    for L in layers:
        im.alpha_composite(L.resize((round(HW * s), round(HH * s)), Image.LANCZOS), (round(OX * s), round(OY * s)))
    return im
# constantes normalizadas (0..1 del lienzo) para el código de la animación
ox0, oy0 = bb[0], bb[1]
PUP_X = (OX + (pcx - ox0) / MW * HW) / CAN; PUP_Y = (OY + (pcy - oy0) / MH * HH) / CAN
ey = np.where((ringA + pupA) > 0.3)[0]
EYE_TOP = (OY + (ey.min() - oy0) / MH * HH) / CAN; EYE_BOT = (OY + (ey.max() - oy0) / MH * HH) / CAN
LILA = (124, 44, 222); CYAN = (56, 196, 248)
# palabra "propera." como imagen (misma tipografía en las dos plataformas)
POPB = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
def wordmark(scale):
    f = ImageFont.truetype(POPB, 22 * scale); d0 = ImageDraw.Draw(Image.new('RGBA', (10, 10)))
    tw = d0.textlength('propera', font=f); dot = 6 * scale; W = int(tw + dot + 4 * scale); H = int(34 * scale)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((0, 0), 'propera', font=f, fill='white'); x = tw + 2 * scale; y = 17.6 * scale
    d.ellipse((x, y, x + dot, y + dot), fill=CYAN); return im
# ================= iOS =================
IO = f'{OUT}/ios/Assets.xcassets'
ICON.save(mk(f'{IO}/AppIcon.appiconset/AppIcon-1024.png'))
json.dump({"images": [{"filename": "AppIcon-1024.png", "idiom": "universal", "platform": "ios", "size": "1024x1024"}], "info": {"author": "xcode", "version": 1}},
          open(f'{IO}/AppIcon.appiconset/Contents.json', 'w'), indent=2)
def imageset(name, make):
    imgs = []
    for sc in (1, 2, 3):
        fn = f'{name}@{sc}x.png'; make(sc).save(mk(f'{IO}/{name}.imageset/{fn}')); imgs.append({"filename": fn, "idiom": "universal", "scale": f"{sc}x"})
    json.dump({"images": imgs, "info": {"author": "xcode", "version": 1}}, open(f'{IO}/{name}.imageset/Contents.json', 'w'), indent=2)
imageset('SplashLogo', lambda sc: canvas([L_body, L_ring], CAN * sc))        # pantalla de arranque del sistema
imageset('SplashHalcon', lambda sc: canvas([L_body], CAN * sc))              # capas de la animación
imageset('SplashAnillo', lambda sc: canvas([L_ring], CAN * sc))
imageset('SplashPupila', lambda sc: canvas([L_pup], CAN * sc))
imageset('SplashMarca', lambda sc: wordmark(sc))
os.makedirs(f'{IO}/SplashBackground.colorset', exist_ok=True)
json.dump({"colors": [{"color": {"color-space": "srgb", "components": {"alpha": "1.000", "red": "0x%02X" % LILA[0], "green": "0x%02X" % LILA[1], "blue": "0x%02X" % LILA[2]}}, "idiom": "universal"}],
           "info": {"author": "xcode", "version": 1}}, open(f'{IO}/SplashBackground.colorset/Contents.json', 'w'), indent=2)
json.dump({"info": {"author": "xcode", "version": 1}}, open(f'{IO}/Contents.json', 'w'), indent=2)
# ================= Android =================
R = f'{OUT}/android/res'
fgmask = ((bodyA + ringA + pupA) > 0.02).astype(np.uint8)
bgimg = cv2.inpaint(np.array(ICON)[..., ::-1], cv2.dilate(fgmask * 255, np.ones((9, 9), np.uint8)), 12, cv2.INPAINT_TELEA)[..., ::-1]
BGI = Image.fromarray(bgimg)
L_mono = layer(np.clip(bodyA + ringA, 0, 1), (255, 255, 255)).crop(bb)
def adaptive(layers, px, frac=0.485):
    im = Image.new('RGBA', (px, px), (0, 0, 0, 0)); h = px * frac; w = h * MW / MH
    for L in layers: im.alpha_composite(L.resize((round(w), round(h)), Image.LANCZOS), (round((px - w) / 2 + px * 0.006), round((px - h) / 2)))
    return im
def rmask(s, kind):
    m = Image.new('L', (s * 4, s * 4), 0); d = ImageDraw.Draw(m)
    if kind == 'round': d.ellipse((0, 0, s * 4 - 1, s * 4 - 1), fill=255)
    else: d.rounded_rectangle((0, 0, s * 4 - 1, s * 4 - 1), s * 4 * 0.18, fill=255)
    return m.resize((s, s), Image.LANCZOS)
for dn, k in (('mdpi', 1), ('hdpi', 1.5), ('xhdpi', 2), ('xxhdpi', 3), ('xxxhdpi', 4)):
    p108 = round(108 * k); p48 = round(48 * k)
    adaptive([L_body, L_ring, L_pup], p108).save(mk(f'{R}/mipmap-{dn}/ic_launcher_foreground.png'))
    BGI.resize((p108, p108), Image.LANCZOS).save(f'{R}/mipmap-{dn}/ic_launcher_background.png')
    adaptive([L_mono], p108).save(f'{R}/mipmap-{dn}/ic_launcher_monochrome.png')
    for kind, name in (('square', 'ic_launcher'), ('round', 'ic_launcher_round')):
        t = ICON.resize((p48, p48), Image.LANCZOS).convert('RGBA'); t.putalpha(rmask(p48, kind)); t.save(f'{R}/mipmap-{dn}/{name}.png')
    canvas([L_body, L_ring], round(288 * k)).save(mk(f'{R}/drawable-{dn}/splash_logo.png'))
for name, ls in (('splash_halcon', [L_body]), ('splash_anillo', [L_ring]), ('splash_pupila', [L_pup])):
    canvas(ls, 1152).save(mk(f'{R}/drawable-nodpi/{name}.png'))
wordmark(4).save(f'{R}/drawable-nodpi/splash_marca.png')
xml = '''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@mipmap/ic_launcher_background" />
    <foreground android:drawable="@mipmap/ic_launcher_foreground" />
    <monochrome android:drawable="@mipmap/ic_launcher_monochrome" />
</adaptive-icon>
'''
for nme in ('ic_launcher', 'ic_launcher_round'): open(mk(f'{R}/mipmap-anydpi-v26/{nme}.xml'), 'w').write(xml)
open(mk(f'{R}/values/propera_splash.xml'), 'w').write('''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="splash_background">#%02X%02X%02X</color>

    <!-- Dependencia: implementation("androidx.core:core-splashscreen:1.0.1") -->
    <style name="Theme.Propera.Splash" parent="Theme.SplashScreen">
        <item name="windowSplashScreenBackground">@color/splash_background</item>
        <item name="windowSplashScreenAnimatedIcon">@drawable/splash_logo</item>
        <!-- Cambia por el tema real de la app -->
        <item name="postSplashScreenTheme">@style/Theme.Propera</item>
    </style>
</resources>
''' % LILA)
ICON.resize((512, 512), Image.LANCZOS).save(mk(f'{OUT}/android/play_store_512.png'))
# ================= código =================
C = dict(px=round(PUP_X, 4), py=round(PUP_Y, 4), et=round(EYE_TOP, 4), eb=round(EYE_BOT, 4))
open(mk(f'{OUT}/ios/ProperaSplashView.swift'), 'w').write('''import SwiftUI

/// Animación de entrada de Propera. Empieza igual que la pantalla de arranque del sistema
/// (halcón con el ojo vacío) y después: se enciende la pupila, el halcón parpadea y entra "propera.".
/// Llama a `onFinished` al terminar (~1,4 s). Si la app ya está lista antes, puedes cortarla.
struct ProperaSplashView: View {
    var onFinished: () -> Void = {}

    @State private var pupil: CGFloat = 0      // 0 = sin pupila, 1 = pupila completa
    @State private var lid: CGFloat = 0        // 0 = ojo abierto, 1 = cerrado
    @State private var wordmark: Double = 0

    // Posiciones dentro del lienzo de 288 x 288 pt (fracciones 0...1)
    private let pupilAnchor = UnitPoint(x: %(px)s, y: %(py)s)
    private let eyeTop: CGFloat = %(et)s
    private let eyeBottom: CGFloat = %(eb)s

    var body: some View {
        ZStack {
            Color("SplashBackground").ignoresSafeArea()

            ZStack {
                Image("SplashHalcon").resizable()
                ZStack {
                    Image("SplashAnillo").resizable()
                    Image("SplashPupila").resizable()
                        .scaleEffect(pupil, anchor: pupilAnchor)
                }
                .mask(
                    // el párpado sube desde abajo: deja ver solo lo que queda por encima
                    GeometryReader { geo in
                        let visible = eyeBottom - (eyeBottom - eyeTop) * lid
                        VStack(spacing: 0) {
                            Rectangle().frame(height: geo.size.height * visible)
                            Spacer(minLength: 0)
                        }
                    }
                )
            }
            .frame(width: 288, height: 288)

            VStack {
                Spacer()
                Image("SplashMarca")
                    .opacity(wordmark)
                    .offset(y: wordmark == 1 ? 0 : 5)
                    .padding(.bottom, 100)
            }
        }
        .task { await run() }
    }

    private func run() async {
        try? await Task.sleep(for: .milliseconds(150))
        withAnimation(.spring(response: 0.35, dampingFraction: 0.55)) { pupil = 1 }
        try? await Task.sleep(for: .milliseconds(300))
        withAnimation(.easeOut(duration: 0.45)) { wordmark = 1 }
        try? await Task.sleep(for: .milliseconds(400))
        withAnimation(.easeIn(duration: 0.08)) { lid = 1 }          // parpadeo
        try? await Task.sleep(for: .milliseconds(110))
        withAnimation(.easeOut(duration: 0.13)) { lid = 0 }
        try? await Task.sleep(for: .milliseconds(350))
        onFinished()
    }
}

#Preview { ProperaSplashView() }
''' % C)
open(mk(f'{OUT}/android/ProperaSplash.kt'), 'w').write('''package com.propera.app.ui.splash   // cambia por tu paquete

import androidx.compose.animation.core.*
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.drawWithContent
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.TransformOrigin
import androidx.compose.ui.graphics.drawscope.clipRect
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import com.propera.app.R

private val SplashBackground = Color(0xFF%(col)s)
private const val PUPIL_X = %(px)sf
private const val PUPIL_Y = %(py)sf
private const val EYE_TOP = %(et)sf
private const val EYE_BOTTOM = %(eb)sf

/**
 * Animación de entrada de Propera. Empieza igual que el splash del sistema (halcón con el ojo vacío):
 * se enciende la pupila, el halcón parpadea y entra "propera.". Llama a onFinished al terminar (~1,4 s).
 */
@Composable
fun ProperaSplash(onFinished: () -> Unit = {}) {
    val pupil = remember { Animatable(0f) }
    val lid = remember { Animatable(0f) }
    val word = remember { Animatable(0f) }

    LaunchedEffect(Unit) {
        delay(150)
        launch { pupil.animateTo(1f, spring(dampingRatio = 0.45f, stiffness = 320f)) }
        delay(300)
        launch { word.animateTo(1f, tween(450, easing = LinearOutSlowInEasing)) }
        delay(400)
        lid.animateTo(1f, tween(80, easing = FastOutLinearInEasing))      // parpadeo
        delay(30)
        lid.animateTo(0f, tween(130, easing = LinearOutSlowInEasing))
        delay(350)
        onFinished()
    }

    Box(Modifier.fillMaxSize().background(SplashBackground), contentAlignment = Alignment.Center) {
        Box(Modifier.size(288.dp)) {
            Image(painterResource(R.drawable.splash_halcon), null, Modifier.fillMaxSize())
            Box(
                Modifier.fillMaxSize().drawWithContent {
                    val visible = EYE_BOTTOM - (EYE_BOTTOM - EYE_TOP) * lid.value
                    clipRect(bottom = size.height * visible) { this@drawWithContent.drawContent() }
                }
            ) {
                Image(painterResource(R.drawable.splash_anillo), null, Modifier.fillMaxSize())
                Image(
                    painterResource(R.drawable.splash_pupila), null,
                    Modifier.fillMaxSize().graphicsLayer {
                        scaleX = pupil.value; scaleY = pupil.value
                        transformOrigin = TransformOrigin(PUPIL_X, PUPIL_Y)
                    }
                )
            }
        }
        Image(
            painterResource(R.drawable.splash_marca), "Propera",
            Modifier.align(Alignment.BottomCenter).padding(bottom = 100.dp).height(34.dp)
                .graphicsLayer { alpha = word.value; translationY = (1f - word.value) * 5.dp.toPx() }
        )
    }
}
''' % dict(C, col='%02X%02X%02X' % LILA))
print(C, MW, MH)

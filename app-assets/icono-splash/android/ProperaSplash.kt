package com.propera.mobile.ui.splash   // ajusta al paquete real si es otro

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
import android.os.Build
import androidx.compose.ui.res.colorResource
import com.propera.mobile.R

private const val PUPIL_X = 0.52f
private const val PUPIL_Y = 0.4978f
private const val EYE_TOP = 0.4439f
private const val EYE_BOTTOM = 0.5402f

/**
 * Animación de entrada de Propera. Empieza igual que el splash del sistema (halcón con el ojo vacío):
 * se enciende la pupila y el halcón parpadea de abajo hacia arriba; "propera." está abajo. Llama a onFinished al terminar (~1,4 s).
 */
@Composable
fun ProperaSplash(onFinished: () -> Unit = {}) {
    val pupil = remember { Animatable(0f) }
    val lid = remember { Animatable(0f) }
    // En Android 12+ el splash del sistema ya muestra "propera." abajo (windowSplashScreenBrandingImage):
    // aquí empieza visible en el mismo sitio para que no salte. En Android 11 o anterior entra con un fundido.
    val brandingFromSystem = Build.VERSION.SDK_INT >= Build.VERSION_CODES.S
    val word = remember { Animatable(if (brandingFromSystem) 1f else 0f) }

    LaunchedEffect(Unit) {
        delay(150)
        launch { pupil.animateTo(1f, spring(dampingRatio = 0.45f, stiffness = 320f)) }
        delay(300)
        if (!brandingFromSystem) launch { word.animateTo(1f, tween(450, easing = LinearOutSlowInEasing)) }
        delay(400)
        lid.animateTo(1f, tween(80, easing = FastOutLinearInEasing))      // parpadeo
        delay(30)
        lid.animateTo(0f, tween(130, easing = LinearOutSlowInEasing))
        delay(350)
        onFinished()
    }

    // Fondo: #7C2CDE en modo claro y #140A24 en modo oscuro (values / values-night)
    Box(Modifier.fillMaxSize().background(colorResource(R.color.splash_background)), contentAlignment = Alignment.Center) {
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
            painterResource(R.drawable.propera_wordmark), "Propera",
            // 60 dp: margen inferior que usa Android para la imagen de marca del splash
            Modifier.align(Alignment.BottomCenter).padding(bottom = 60.dp).size(97.85.dp, 18.3.dp)
                .graphicsLayer { alpha = word.value; translationY = (1f - word.value) * 5.dp.toPx() }
        )
    }
}

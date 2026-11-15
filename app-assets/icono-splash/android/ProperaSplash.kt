package com.propera.app.ui.splash   // cambia por tu paquete

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

private val SplashBackground = Color(0xFF7C2CDE)
private const val PUPIL_X = 0.52f
private const val PUPIL_Y = 0.4978f
private const val EYE_TOP = 0.4439f
private const val EYE_BOTTOM = 0.5402f

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

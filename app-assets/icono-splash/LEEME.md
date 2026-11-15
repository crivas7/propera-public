# Propera · icono de la app y splash screen

- Icono: halcón blanco con el ojo cian sobre degradado violeta.
- Splash: fondo lila `#7C2CDE`, halcón en el centro y animación de entrada (se enciende la pupila cian, el halcón parpadea de abajo hacia arriba y entra "propera." con el punto cian).

Cómo funciona el splash en las dos plataformas:
1. El sistema muestra una pantalla de arranque **estática**: fondo lila y halcón con el ojo vacío (sin pupila).
2. La primera pantalla de la app es la **animación** (`ProperaSplashView` / `ProperaSplash`). Empieza exactamente igual que la pantalla del sistema, así que el paso de una a otra no se nota.
3. Al terminar (~1,4 s) llama a `onFinished` y la app pasa a su pantalla de inicio. Si la app ya está lista antes, se puede cortar.

---

## iOS (SwiftUI)

1. Copia el contenido de `ios/Assets.xcassets` dentro del `Assets.xcassets` del proyecto (sustituye `AppIcon`).
2. Pantalla de arranque del sistema: en `Info.plist`

```xml
<key>UILaunchScreen</key>
<dict>
    <key>UIColorName</key>
    <string>SplashBackground</string>
    <key>UIImageName</key>
    <string>SplashLogo</string>
    <key>UIImageRespectsSafeAreaInsets</key>
    <false/>
</dict>
```

3. Añade `ios/ProperaSplashView.swift` y úsala como primera vista:

```swift
@main
struct ProperaApp: App {
    @State private var showSplash = true
    var body: some Scene {
        WindowGroup {
            ZStack {
                ContentView()
                if showSplash {
                    ProperaSplashView { withAnimation(.easeOut(duration: 0.3)) { showSplash = false } }
                        .transition(.opacity)
                }
            }
        }
    }
}
```

`SplashLogo` mide 288 x 288 pt, igual que el lienzo de la animación, para que el halcón salga en el mismo sitio y al mismo tamaño.

---

## Android (Kotlin)

1. Copia `android/res` dentro de `app/src/main/res` (mezcla las carpetas).
2. `AndroidManifest.xml`:
   - `android:icon="@mipmap/ic_launcher"` y `android:roundIcon="@mipmap/ic_launcher_round"`
   - En la actividad de inicio: `android:theme="@style/Theme.Propera.Splash"`
3. `build.gradle`: `implementation("androidx.core:core-splashscreen:1.0.1")`
4. En `values/propera_splash.xml` cambia `@style/Theme.Propera` por el nombre real del tema de la app.
5. Añade `android/ProperaSplash.kt` (cambia el `package` y el import de `R`). En `MainActivity`:

```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    installSplashScreen()                // antes de super.onCreate
    super.onCreate(savedInstanceState)
    setContent {
        var showSplash by remember { mutableStateOf(true) }
        Box {
            AppContent()
            AnimatedVisibility(showSplash, exit = fadeOut(tween(300))) {
                ProperaSplash(onFinished = { showSplash = false })
            }
        }
    }
}
```

Icono:
- Adaptativo: `ic_launcher_foreground` (halcón), `ic_launcher_background` (degradado) y `ic_launcher_monochrome` (iconos temáticos de Android 13+).
- Clásico (`ic_launcher`, `ic_launcher_round`) para Android 7 o anterior.
- `play_store_512.png`: icono para la ficha de Google Play.

---

## Archivos

| Archivo | Uso |
|---|---|
| `AppIcon-1024.png` | Icono iOS (Xcode genera el resto de tamaños) |
| `SplashLogo` / `splash_logo` | Pantalla de arranque del sistema (halcón sin pupila) |
| `SplashHalcon`, `SplashAnillo`, `SplashPupila` | Capas de la animación (mismo lienzo de 288 x 288) |
| `SplashMarca` / `splash_marca` | "propera." con el punto cian |
| `SplashBackground` / `splash_background` | Lila `#7C2CDE` |

Pendiente: redibujar en vector las dos puntas inferiores del pico. Cuando esté, se sustituyen estos archivos con los mismos nombres.

# Propera · icono y splash (iOS SwiftUI + Android Kotlin)

Colores: fondo claro `#F5F1FF`, fondo oscuro `#120C2A`.

## iOS (Xcode, SwiftUI)
1. Copia `ios/AppIcon.appiconset` dentro de `Assets.xcassets` (sustituye al AppIcon actual). Incluye el icono claro, el oscuro y el tintado (iOS 18+).
2. Copia `ios/SplashLogo.imageset` y `ios/SplashBackground.colorset` dentro de `Assets.xcassets`. Los dos cambian solos entre modo claro y oscuro.
3. En `Info.plist` añade la pantalla de arranque:

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

## Android (Kotlin)
1. Copia el contenido de `android/res` dentro de `app/src/main/res` (mezcla las carpetas).
2. En `AndroidManifest.xml`: `android:icon="@mipmap/ic_launcher"` y `android:roundIcon="@mipmap/ic_launcher_round"`.
3. Splash (Android 12+ y anteriores con la librería de compatibilidad):
   - `build.gradle`: `implementation("androidx.core:core-splashscreen:1.0.1")`
   - En el manifest, pon `android:theme="@style/Theme.Propera.Splash"` en la actividad de inicio.
   - En `values/propera_branding.xml`, cambia `@style/Theme.Propera` por el nombre real del tema de la app.
   - En `MainActivity.onCreate`, antes de `super.onCreate(...)`: `installSplashScreen()`.
4. `android/play_store_icon_512.png` es el icono para la ficha de Google Play.

## master/
Logo con transparencia y versión monocroma, por si hacen falta otros tamaños.

# Splash en modo claro y oscuro

El splash continúa el icono de la app en cada modo:

| Modo | Fondo | Centro | Abajo |
|---|---|---|---|
| Claro | `#7C2CDE` (lila de marca, como el icono) | Halcón blanco, pupila cian | "propera." blanco, punto cian `#38C4F8` |
| Oscuro | `#140A24` (lila casi negro, como el icono oscuro) | Halcón blanco, pupila cian | "propera." blanco, punto cian `#38C4F8` |

Solo cambia el color de fondo. El halcón, la animación (pupila que se ilumina y parpadeo de abajo hacia arriba) y el logotipo son iguales en los dos modos.

## Archivos

| Archivo | Uso |
|---|---|
| `ejemplos/` | Cómo debe verse: iOS y Android, en claro y en oscuro (`splash_propuesta_4.png` los reúne). |
| `ios/SplashBackground.colorset/` | Fondo con dos versiones: `#7C2CDE` (Any) y `#140A24` (Dark). |
| `android/res/values/propera_splash_colors.xml` | `splash_background` = `#7C2CDE`. |
| `android/res/values-night/propera_splash_colors.xml` | `splash_background` = `#140A24`. |

El halcón del splash está en `app-assets/icono-splash/` y el logotipo "propera." en vector, en `app-assets/marca/`.

## Medidas

- **Halcón:** lienzo de 288 × 288 pt/dp con el halcón de 144 de alto, centrado. En Android 12+ cabe en el círculo de 192 dp que recorta el sistema.
- **"propera.":** 97,85 × 18,3 pt/dp (el tamaño del logotipo del splash), centrado abajo, a unos 56–60 pt/dp del borde inferior.

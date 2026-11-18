# Logotipo "propera." (vector)

Mismo dibujo que el splash: **Poppins Bold** con el **punto cian `#38C4F8`**. Está convertido a trazos, así que no hace falta instalar la fuente en la app y se ve idéntico en iOS, Android y el splash.

| Archivo | Uso |
|---|---|
| `ios/ProperaMarca.imageset/` | Imagen vectorial (SVG) para el catálogo de recursos de Xcode. Texto blanco, punto cian. |
| `ios/ProperaCian.colorset/` | Cian de interfaz con dos tonos: `#0A8FC7` en modo claro y `#38C4F8` en modo oscuro (indicador de carga, acentos). |
| `android/res/drawable/propera_wordmark.xml` | VectorDrawable. Texto blanco, punto cian. |
| `android/res/values/propera_marca.xml` y `values-night/` | `propera_cian`: `#0A8FC7` en claro y `#38C4F8` en oscuro; `propera_lila` `#7C2CDE`. |
| `svg/` | Versiones SVG en blanco (para fondos oscuros) y en lila (para fondos claros). |

**Proporción:** 97,85 × 18,3 (ancho × alto). Escalar siempre manteniendo la proporción.

**Tamaño en la cabecera:** un 15–20 % más grande que el texto "propera." actual (objetivo +18 %). Como referencia, unos 24 pt / 24 dp de alto (≈ 128 de ancho), y comprobar a ojo que queda proporcionado con los botones redondos de la derecha.

**Modo claro:** si la app tiene modo claro, usar la versión lila (`svg/propera_wordmark_lila.svg`) sobre fondo claro.

**Cian según el modo:** el cian de marca `#38C4F8` apenas contrasta sobre blanco (≈2:1), así que en modo claro los elementos de interfaz (indicador de carga, acentos) usan `#0A8FC7` (≈3,6:1). El punto del logotipo sigue siendo `#38C4F8` en los dos modos, porque forma parte de la marca.

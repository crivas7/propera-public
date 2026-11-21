# Reel «Día 30» (Marcos)

Reel vertical de Instagram para Propera (1080×1920, 30 fps, 31 s), pensado para el lunes 30 de noviembre (fin de mes). Marcos es un **personaje**: no lo presentes como cliente real ni le atribuyas testimonios.

Serie «tipos de personas»: Marcos registra **por voz**. Para no repetir «Luego lo apunto» (Sara), el giro es que **el día 1 Propera reserva los pagos fijos** y lo que queda es el disponible real.

## Archivos

- `reel_marcos_v2_sin_voz.mp4`: versión actual, con música y sin voz. Todos los planos son del mismo actor.
- `reel_marcos_v1_sin_voz.mp4`: primera versión (solo la mano con el móvil y pantallas simuladas).
- `marcos.py`: escenas, tarjetas (banco genérico, Propera) y pantallas simuladas.
- `timeline.json`: inicio de cada escena y subtítulos (`CAPS`), que solo se dibujan con voz.
- `build.sh`: regenera el vídeo. `./build.sh` sin voz; `VOZ=voz.wav ./build.sh` con voz, ducking de la música y subtítulos en Poppins Bold. `SOLO_TRAMOS=1 ./build.sh` solo prepara los fotogramas de los clips.
- Clips en `../media/marcos/`, música de `../685446693-….mp4` y cierre de `../reel-javi/assets/end.png`.

## Clips (Pexels, Mikhail Nilov, misma sesión y mismo actor)

| Clip | Uso |
|---|---|
| [6898111](https://www.pexels.com/video/6898111/) | Día 30: mira el móvil junto a la ventana |
| [6898113](https://www.pexels.com/video/6898113/) | Rebobinado: desembala un pedido |
| [6898022](https://www.pexels.com/video/6898022/) | Rebobinado: paga online con la tarjeta |
| [6898100](https://www.pexels.com/video/6898100/) | Rebobinado: pide comida en el móvil |
| [6898101](https://www.pexels.com/video/6898101/) | Rebobinado: recoge otro pedido de noche |
| [6898026](https://www.pexels.com/video/6898026/) | Fondo del día 1: sus manos con el móvil |
| [6898016](https://www.pexels.com/video/6898016/) | Le dicta el gasto al móvil y se queda tranquilo |
| [6898010](https://www.pexels.com/video/6898010/) | Día 30: mira el móvil y sonríe |

Crédito para el post: «Vídeos: Mikhail Nilov (Pexels)».

## Línea de tiempo

| Tramo | Escena |
|---|---|
| 0–4,5 s | «POV: es día 30»; notificación del banco: el saldo cae a 12,40 € |
| 4,5–10,5 s | Rebobinado de sus gastos (planos al revés): pedido 18,90 €, compra online 59,90 €, cena 24,50 €, otro pedido 32 € |
| 10,5–13 s | «Mes siguiente. Día 1.» |
| 13–19,5 s | Propera día 1: nómina 1.400 €, reserva alquiler, luz, internet, gimnasio y móvil → 615 € disponibles |
| 19,5–24 s | «Y cada gasto, se lo digo»: dicta «Café, dos cincuenta» → registrado |
| 24–27,5 s | «Día 30: sin sustos»: sonríe; Propera muestra 85 € y «Cierras el mes en positivo» |
| 27,5–31 s | Cierre de marca |

## Voz en off (pendiente)

- ElevenLabs, modelo `eleven_v4`, voz **Álvaro** (`ozbKZapo4Cy6jU7KTHtp`).
- Cada bloque empieza en su tramo; después de generarla, ajusta los tiempos de `CAPS` a la voz real.

```
[0,4–4,2 s] Día treinta. Abro el banco… doce euros.
[4,6–10,3 s] ¿En qué se me ha ido el sueldo? Un pedido, una compra online, otra cena… ni me acuerdo.
[10,6–12,8 s] Así que el mes siguiente cambié una cosa.
[13,1–19,3 s] El día uno, Propera reserva primero lo fijo: alquiler, luz, internet… Lo que queda es lo que tengo de verdad.
[19,6–23,7 s] Y cada gasto se lo digo: café, dos cincuenta. Listo.
[24,1–27,2 s] Día treinta, y sin sustos.
[27,6–30,6 s] Propera. Prosperar comienza con orden.
```

## Reglas

- No prometas registro automático: Marcos dice cada gasto y queda registrado.
- La app de banco es genérica, sin logo ni nombre de banco real; los gastos no nombran marcas de reparto.
- Al publicar: portada obligatoria y créditos del vídeo (Pexels) y de la música en el texto del post.

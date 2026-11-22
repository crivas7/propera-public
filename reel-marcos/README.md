# Reel «Día 30» (Marcos)

Reel vertical de Instagram para Propera (1080×1920, 30 fps, 31 s), pensado para el lunes 30 de noviembre (fin de mes). Marcos es un **personaje**: no lo presentes como cliente real ni le atribuyas testimonios.

Serie «tipos de personas»: Marcos registra **por voz**. Para no repetir «Luego lo apunto» (Sara), el giro es que **el día 1 Propera reserva los pagos fijos** y lo que queda es el disponible real.

## Archivos

- `reel_marcos_v10.mp4`: **versión actual** (32,2 s). Día 1 con «Primero, lo que ya tienes comprometido. / Después, lo que realmente puedes gastar.» y «comprometido» dentro de la app; subtítulos en una línea a altura fija (centro y=1545, fuera de la zona que tapa Instagram) con tarjetas y móviles por encima (≤1460); día 30 con avance temporal (12 → 30 dic, 402,30 → 85 €, +23 gastos registrados). Pendiente: cambiar en la voz «Propera reserva primero lo fijo».
- `reel_marcos_v9.mp4`: versión anterior (32,2 s). La escena del efectivo tiene un solo corte: él dictando con el móvil en la boca («Te escucho…») → zoom dentro de su móvil → pantalla de Propera que transcribe «Décimo de lotería, veinte euros» y lo registra con «Listo».
- `reel_marcos_v8.mp4`: versión anterior (32,2 s), con dos cortes en la escena del efectivo. Igual que la v7, pero la escena del efectivo ya no tiene el plano en que coge el móvil ni el gesto de la boca al bajarlo: pantalla de Propera (pulsa el micro) → él dictando el gasto (tramo limpio de 6898016, 23,0–24,8 s) → pantalla con «Lotería de Navidad −20 € · Registrado».
- `reel_marcos_v7.mp4`: versión anterior (32,2 s). Voz de Eric completa (`voz_v3.wav`), música A (lo-fi) solo desde «Mes siguiente / Día 1» (`musica/musica_a_desde_dia1.wav`), y la escena del efectivo a velocidad normal: coge el móvil de la mesa (6898019) y corte a él dictando el gasto (6898016).
- `reel_marcos_v6_musica_a.mp4`, `_b`, `_c`: versión actual (32,2 s) con la voz de Eric completa (`voz_v3.wav`) y tres opciones de música original: **a** lo-fi cálido, **b** pop acústico, **c** piano emotivo.
- `musica/synth.py`: compone las tres pistas aquí mismo, sin samples ni licencias (`python3 musica/synth.py a|b|c salida.wav 32.2`). Estructura: contenida hasta los 11 s, se abre en «Mes siguiente», golpe final a los 29 s. Las `.wav` están niveladas a −29 LUFS. `SIN_INTRO=1` (solo en la opción a) deja la música en silencio hasta los 11 s; `musica_a_desde_dia1.wav` está igualada a la opción A desde ese punto.
- `voz_v3.wav`: locución actual = `voz_v1.mp3` (Eric) con la frase de la lotería también de Eric.
- `reel_marcos_v5_con_voz.mp4`: versión actual (31,6 s). Toque de temporada: Black Friday en los recuerdos, gasto en efectivo (décimo de lotería) y final el 30 de diciembre. Música provisional (la de siempre).
- `voz_v2.wav`: locución actual = `voz_v1.mp3` con la frase del café sustituida por la de la lotería (ElevenLabs, flow `VGNZVZAYuAXeTccR7k7W`); se coloca con 0,3 s de desfase (`VOZ_DESFASE_MS`).
- `reel_marcos_v4_con_voz.mp4` / `voz_v1.mp3`: versión anterior, con «café, dos cincuenta».
- `reel_marcos_v3_sin_voz.mp4`: recuerdos como montón de fotos con contador, sin voz.
- `reel_marcos_v2_sin_voz.mp4`: recuerdos como rebobinado de planos al revés.
- `reel_marcos_v1_sin_voz.mp4`: primera versión (solo la mano con el móvil y pantallas simuladas).
- `marcos.py`: escenas, tarjetas (banco genérico, Propera) y pantallas simuladas.
- `timeline.json`: inicio de cada escena y subtítulos (`CAPS`), que solo se dibujan con voz.
- `build.sh`: regenera el vídeo. `./build.sh` sin voz; `VOZ=voz_v3.wav MUSICA=musica/musica_a_desde_dia1.wav ./build.sh` con voz, ducking de la música, subtítulos en Poppins Bold y normalización a −14 LUFS; `SOLO_MEZCLA=1` rehace solo el audio. `SOLO_TRAMOS=1 ./build.sh` solo prepara los fotogramas de los clips.
- Clips en `../media/marcos/`, música de `../685446693-….mp4` y cierre de `../reel-javi/assets/end.png`.

## Clips (Pexels, Mikhail Nilov, misma sesión y mismo actor)

| Clip | Uso |
|---|---|
| [6898111](https://www.pexels.com/video/6898111/) | Día 30: mira el móvil junto a la ventana |
| [6898113](https://www.pexels.com/video/6898113/) | Recuerdo: desembala un pedido |
| [6898022](https://www.pexels.com/video/6898022/) | Recuerdo: paga online con la tarjeta |
| [6898100](https://www.pexels.com/video/6898100/) | Recuerdo: pide comida en el móvil |
| [6898101](https://www.pexels.com/video/6898101/) | Recuerdo: recoge otro pedido de noche |
| [6898026](https://www.pexels.com/video/6898026/) | Fondo del día 1: sus manos con el móvil |
| [6898016](https://www.pexels.com/video/6898016/) | Le dicta el gasto al móvil (solo 23,0–24,75 s: después se acerca el móvil a la mejilla y al bajarlo hace un gesto con la boca que confunde) |
| [6898010](https://www.pexels.com/video/6898010/) | Día 30: mira el móvil y sonríe |

Crédito para el post: «Vídeos: Mikhail Nilov (Pexels)».

## Línea de tiempo (ajustada a la voz)

| Tramo | Escena | Voz |
|---|---|---|
| 0–4,1 s | «POV: es día 30»; el saldo del banco cae a 12,40 € | Día treinta. Abro el banco… doce euros. |
| 4,1–11 s | Recuerdos: cada gasto cae como una foto y el contador suma; remate «+ alquiler, facturas, el Black Friday y 36 gastos más» → 1.387,60 € | ¿En qué se me ha ido el sueldo? Un pedido, una compra online, otra cena… y así todo el mes. |
| 11–13,6 s | «Mes siguiente. Día 1.» | Así que el mes siguiente cambié una cosa. |
| 13,6–21 s | Propera día 1: las reservas entran con «alquiler, luz, internet» → 615 € disponibles | El día uno, Propera reserva primero lo fijo… Lo que queda es lo que tengo de verdad. |
| 21–26,85 s | «Lo que pago en efectivo, se lo digo»: dicta el gasto al móvil (tramo a 0,625×) → «Lotería de Navidad · Efectivo · −20 €», «Registrado» con «Listo» | Y lo que pago en efectivo, se lo digo: décimo de lotería, veinte euros. Listo. |
| 26,85–29,1 s | «30 de diciembre: sin sustos»; sonríe; 85 € disponibles | Día treinta, y sin sustos. |
| 29,1–32,2 s | Cierre de marca | Propera. Prosperar comienza con orden. |

## Guion de la voz

- ElevenLabs, modelo `eleven_v4`, voz **Álvaro** (`ozbKZapo4Cy6jU7KTHtp`).
- Generada en una sola toma (flow de ElevenLabs `VGNZVZAYuAXeTccR7k7W`); cada bloque se coloca en su tramo y los tiempos de `CAPS` se ajustan a la voz real.

```
[0,4–4,2 s] Día treinta. Abro el banco… doce euros.
[4,6–10,3 s] ¿En qué se me ha ido el sueldo? Un pedido, una compra online, otra cena… y así todo el mes.
[10,6–12,8 s] Así que el mes siguiente cambié una cosa.
[13,1–19,3 s] El día uno, Propera reserva primero lo fijo: alquiler, luz, internet… Lo que queda es lo que tengo de verdad.
[21,3–26,1 s] Y lo que pago en efectivo, se lo digo: décimo de lotería, veinte euros. Listo.
[24,1–27,2 s] Día treinta, y sin sustos.
[27,6–30,6 s] Propera. Prosperar comienza con orden.
```

## Reglas

- No decir que Propera «reserva» o «aparta» dinero: suena a que mueve dinero o se conecta al banco (y el cierre dice «sin conectar tu banco»). Hablar de lo «comprometido» y de lo que «realmente puedes gastar».
- Subtítulos siempre en una línea y a la misma altura; nada del montaje por debajo de y≈1460.

- No prometas registro automático: Marcos dice el gasto y queda registrado. La voz se vende para lo que ningún automatismo capta (efectivo, contexto); la lectura de notificaciones tendrá su propio reel.
- La app de banco es genérica, sin logo ni nombre de banco real; los gastos no nombran marcas de reparto.
- Al publicar: portada obligatoria y créditos del vídeo (Pexels) en el texto del post. Con las pistas de `musica/` no hay que acreditar música (son originales); con la pista antigua, sí.

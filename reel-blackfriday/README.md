# Reel «La ganga» (Black Friday)

Reel vertical (1080×1920, 30 fps, 41,8 s) para el lunes 23 de noviembre de 2026, semana del Black Friday (viernes 27). Lo cuenta ella con su voz (ElevenLabs) y los textos en pantalla, con música original. La protagonista es un **personaje** (no presentarla como clienta real).

La historia tiene dos momentos: **el Black Friday pasado** cayó en la trampa y **este año**, antes de comprar, mira lo que realmente puede gastar.

## Guion de la voz

ElevenLabs, modelo `eleven_v4`, voz **Gala** (`Wi5NZQRxyOb3Jx4r0hrI`, joven, España). Toma elegida: `voz.mp3` (40,7 s), entra a los 0,3 s del vídeo:

> [excited] El Black Friday pasado ahorré 120 €. Chaqueta: 60 € de descuento. Zapatillas: 30. Auriculares: 20. Y la freidora: 10 más. [happy] Me sentía la reina de las gangas. [pause] Hasta que miré el banco. [sighs] Supuestamente ahorré 120 €… pero en realidad gasté casi 255 € que no tenía planeado gastar. [warmly] Este año, antes de comprar, miro en Propera lo que realmente puedo gastar hasta cobrar. De mi lista… solo cabe la chaqueta. [happy] Así que me compro la chaqueta, y llego a fin de mes. Si la ganga no cabe en lo que realmente puedes gastar… no es una ganga. Pruébalo gratis en propera.life.

## Historia

Tiempos de `timeline.json`, ajustados a la toma de voz: cada escena entra justo antes de su frase y `beats` mueve lo que pasa dentro (entrada de cada compra, vuelo del «+X €», frases del giro, tarjeta y lista de Propera, remate).

| Escena | Qué pasa |
|---|---|
| hook | Abre paquetes encantada: «El Black Friday pasado ahorré 120 €.» |
| montage | Cuatro compras con su etiqueta. El descuento («+60 €», «+30 €»…) salta de la etiqueta al contador **«Ahorro total»**, que va sumando 60 → 90 → 110 → 120: chaqueta de punto 69,99 (antes 129,99), zapatillas 69,99 (99,99), auriculares 59,99 (79,99), freidora de aire 54,99 (64,99) |
| haul | Corte en la acción: de la caja a sacar la chaqueta y abrazarla. El contador se queda quieto. «Me sentía la reina de las gangas.» |
| twist | Corte seco y frenazo en la música. Ventana: «Hasta que miré el banco.» → «Supuestamente ahorré 120 €… pero en realidad gasté **254,96 €** que no tenía planeado gastar.» (el contador pasa a «Gastado», en rojo) |
| fix | «Este año, antes de comprar, miro lo que realmente puedo gastar.» Propera: disponible real hasta cobrar 180 €; su lista: solo cabe la chaqueta → «Me quedan 110,01 € hasta cobrar» |
| happy | «Solo la chaqueta. Y llego a fin de mes.» |
| punch | «Si la ganga no cabe en lo que realmente puedes gastar, no es una ganga.» |
| end | Cierre de marca |

## Archivos

- **`reel_bf_v4.mp4`: versión final, con la voz de ella** (`VOZ=voz.mp3 ./build.sh`; la música va más baja en el pop de compras, hasta el giro, y la voz la baja aún más mientras habla). `reel_bf_v3.mp4`: textos nuevos, contador «Ahorro total» y corte en la acción, sin voz. `reel_bf_v2.mp4`: primera con «ganga». `reel_bf_v1.mp4`: con «chollo». `portada.png` (+ `portada.py`).
- `bf.py` (escenas), `timeline.json`, `build.sh` (`./build.sh` → `out/reel_bf.mp4`; `VOZ=voz.wav ./build.sh` mezcla la voz y baja la música mientras habla).
- `musica/musica_bf.wav`: música original; `build.sh` la regenera con los tiempos de `timeline.json` (`BF_T=giro,solución,feliz,cierre python3 ../reel-marcos/musica/synth.py bf …`): pop de compras, frenazo en el giro, tensión y piano tranquilo que resuelve en el cierre.
- Clips en `../media/blackfriday/` (Pexels, Mikhail Nilov, misma sesión que Marcos): 6898098, 6898105, 6898106, 6898109, 6898110, 6898112.

## Reglas

- Usar «ganga» en vez de «chollo» (muy de España; «ganga» se entiende también en Latinoamérica).
- El «ahorro» es la suma de descuentos de cosas que no pensaba comprar: dejar claro que es «supuesto» y que lo real es lo que gastó.
- Propera no tiene «carrito» ni decide por ella: muestra el disponible real; la lista es suya.
- No decir que Propera «reserva» dinero; hablar de lo comprometido y de lo que realmente puedes gastar.
- Al publicar: portada y créditos «Vídeos: Mikhail Nilov (Pexels) · Música original».

# Reel «La ganga» (Black Friday)

Reel vertical (1080×1920, 30 fps, 32,6 s) para el lunes 23 de noviembre de 2026, semana del Black Friday (viernes 27). **Sin voz**: la historia se cuenta con textos en pantalla y música original. La protagonista es un **personaje** (no presentarla como clienta real).

## Historia

| Tramo | Escena |
|---|---|
| 0–3,5 s | Abre paquetes encantada: «Este Black Friday ahorré 120 €.» |
| 3,5–10,1 s | Montaje de compras con etiqueta y contador «Ahorrado» (verde): chaqueta de punto 69,99 (antes 129,99), zapatillas 69,99 (99,99), auriculares 59,99 (79,99), freidora de aire 54,99 (64,99) |
| 10,1–13 s | Se prueba la chaqueta: «Me sentía la reina de las gangas.» (120 € ahorrados) |
| 13–17,2 s | Giro (corte seco y frenazo en la música): junto a la ventana, «Hasta que miré el banco.» → «No ahorré 120 €. Gasté 254,96 €.» |
| 17,2–23,8 s | «Este año, antes de comprar, miro lo que realmente puedo gastar.» Propera: disponible real hasta cobrar 180 €; su lista: solo cabe la chaqueta → «Me quedan 110,01 € hasta cobrar» |
| 23,8–26,4 s | «Solo la chaqueta. Y llego a fin de mes.» |
| 26,4–29,2 s | «Si la ganga no cabe en tu disponible real, no es una ganga.» |
| 29,2–32,6 s | Cierre de marca |

## Archivos

- `reel_bf_v2.mp4`: versión actual («ganga», que se entiende en España y Latinoamérica). `reel_bf_v1.mp4`: con «chollo». `portada.png` (+ `portada.py`).
- `bf.py` (escenas), `timeline.json`, `build.sh` (`./build.sh` → `out/reel_bf.mp4`).
- `musica/musica_bf.wav`: música original (`python3 ../reel-marcos/musica/synth.py bf musica/musica_bf.wav 32.6`): pop de compras hasta los 13 s, frenazo, tensión y piano tranquilo que resuelve en el cierre.
- Clips en `../media/blackfriday/` (Pexels, Mikhail Nilov, misma sesión que Marcos): 6898098, 6898105, 6898106, 6898109, 6898110, 6898112.

## Reglas

- Usar «ganga» en vez de «chollo» (muy de España; «ganga» se entiende también en Latinoamérica).

- Propera no tiene «carrito» ni decide por ella: muestra el disponible real; la lista es suya.
- No decir que Propera «reserva» dinero; hablar de lo comprometido y de lo que realmente puedes gastar.
- Al publicar: portada y créditos «Vídeos: Mikhail Nilov (Pexels) · Música original».

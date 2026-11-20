# Reel «Día 30» (Marcos)

Reel vertical de Instagram para Propera (1080×1920, 30 fps, 31 s), pensado para el lunes 30 de noviembre (fin de mes). Marcos es un **personaje**: no lo presentes como cliente real ni le atribuyas testimonios.

Serie «tipos de personas»: Marcos registra **por voz**. Para no repetir «Luego lo apunto» (Sara), el giro es que **el día 1 Propera reserva los pagos fijos** y lo que queda es el disponible real.

## Archivos

- `reel_marcos_v1_sin_voz.mp4`: primera versión, con música y sin voz.
- `marcos.py`: pantallas simuladas (banco genérico sin marca, Propera día 1, registro por voz, Propera día 30) y escenas.
- `timeline.json`: inicio de cada escena y subtítulos (`CAPS`), que solo se dibujan con voz.
- `build.sh`: regenera el vídeo. `./build.sh` sin voz; `VOZ=voz.wav ./build.sh` con voz, ducking de la música y subtítulos en Poppins Bold.
- Reutiliza `../media/pexels_movil_8165696.mp4`, la música de `../685446693-….mp4` y el cierre de `../reel-javi/assets/end.png`.

## Línea de tiempo

| Tramo | Escena |
|---|---|
| 0–4,5 s | Mano con móvil + app de banco: «POV: es día 30», saldo cae a 12,40 € |
| 4,5–10,5 s | Rebobinado: cañas, Glovo, Bizum, suscripción, ropa, cena |
| 10,5–13 s | «Mes siguiente. Día 1.» |
| 13–19,5 s | Propera día 1: nómina 1.400 €, reserva alquiler, luz, internet, gimnasio y móvil → 615 € disponibles |
| 19,5–24 s | «Y cada gasto, se lo digo»: «Café, dos cincuenta» → Confirmar |
| 24–27,5 s | Propera día 30: 85 € disponibles, «Cierras el mes en positivo» |
| 27,5–31 s | Cierre de marca |

## Voz en off (pendiente)

- ElevenLabs, modelo `eleven_v4`, voz **Álvaro** (`ozbKZapo4Cy6jU7KTHtp`).
- Cada bloque empieza en su tramo; después de generarla, ajusta los tiempos de `CAPS` a la voz real.

```
[0,4–4,2 s] Día treinta. Abro el banco… doce euros.
[4,6–10,3 s] ¿En qué se me ha ido el sueldo? Unas cañas, un Glovo, un Bizum… y una suscripción que ni uso.
[10,6–12,8 s] Así que el mes siguiente cambio una cosa.
[13,1–19,3 s] El día uno, Propera reserva primero lo fijo: alquiler, luz, internet… Lo que queda es lo que tengo de verdad.
[19,6–23,7 s] Y cada gasto se lo digo: café, dos cincuenta. Confirmo y listo.
[24,1–26,9 s] Día treinta, y sin sustos.
[27,6–30,6 s] Propera. Prosperar comienza con orden.
```

## Reglas

- No prometas registro automático: Marcos dice cada gasto y lo confirma.
- La app de banco es genérica, sin logo ni nombre de banco real.
- Al publicar: portada obligatoria y créditos del clip de Pexels y de la música en el texto del post.

# Reel "¿Me las puedo comprar?" (Javi)

Reel vertical de Instagram para Propera (1080×1920, 30 fps, 31 s). Javi es un **personaje**: no lo presentes como cliente real ni le atribuyas testimonios. Los clips de Pexels se usan conforme a su licencia.

## Archivos

- `reel_javi_v3_sin_voz.mp4`: versión aprobada, con música y sin voz.
- `portada.png`: portada del reel. Súbela siempre como portada al programarlo.
- `render.py`: pantallas simuladas (chat de IA genérico, pantalla de Propera), textos y cierre.
- `render2.py`: escenas con los clips y la línea de tiempo.
- `build.sh`: regenera el vídeo sin voz a partir de los clips en `../media/`.
- `assets/`: logo pequeño y fotograma del cierre de marca.

## Línea de tiempo

| Tramo | Escena |
|---|---|
| 0–3,5 s | Clip zapatillas: "POV: quieres estas zapatillas" |
| 3,5–8,5 s | Etiqueta 89,99 €, "El banco dice 640 €…", "¿me las puedo permitir?" |
| 8,5–21,5 s | Clip mano con móvil + chat: pregunta, "Consultando Propera", respuesta |
| 21,5–27 s | Pantalla Propera: ~~640 € en el banco~~ → 210 € de verdad |
| 27–31 s | Cierre: logo, "Prosperar comienza con orden", propera.life |

## Voz en off (pendiente)

- Proveedor: ElevenLabs, modelo `eleven_v4`.
- Voz: **Álvaro – Cool and Energetic**, `voice_id` `ozbKZapo4Cy6jU7KTHtp` (español de España, joven, cercana).
- Encaje en el vídeo: cada bloque empieza en su tramo. La música baja (ducking) mientras habla la voz. Subtítulos grandes en la parte baja, en Poppins Bold.

Guion (un bloque por escena):

```
[0–3 s] Mira qué zapatillas. Me encantan.
[3,5–8 s] Noventa euros. El banco dice que tengo seiscientos cuarenta… ¿pero me las puedo permitir?
[8,5–13 s] Así que se lo pregunto a mi IA, que tiene Propera conectado.
[15–21 s] Y me lo dice claro: de esos seiscientos cuarenta, cuatrocientos treinta ya están comprometidos. Alquiler, luz, gimnasio…
[21,5–26,5 s] Lo que tengo de verdad son doscientos diez euros. Hoy no. Mejor el mes que viene, sin agobios.
[27–31 s] Propera. Sabe lo que tienes de verdad antes de gastar.
```

## Reglas

- No prometas registro automático: hoy el disponible real depende de registrar movimientos (voz, texto o captura).
- El chat es un "Asistente IA" genérico, sin logo ni interfaz de ChatGPT.

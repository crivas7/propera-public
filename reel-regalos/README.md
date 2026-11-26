# Reel «Los regalos» (Black Friday + Navidad)

Reel vertical (1080×1920, 30 fps, 29,4 s) para el **viernes 27 de noviembre de 2026**, el día del Black Friday. Cierra la semana: el lunes fue «La ganga» (no era una ganga), hoy toca «regalos sí, pero con cabeza» y el lunes 30, Marcos con el día 30.

La protagonista es un **personaje nuevo** (no es la chica de «La ganga», que solo tiene clips de un día y con la misma ropa) y no es una clienta real.

## Guion de la voz

ElevenLabs, modelo `eleven_v4`, voz **Silvia Expresiva** (`DNtbMnLZ43q8pReedyYw`, joven, España; distinta de Gala):

> [excited] Hoy es Black Friday: día de adelantar los regalos de Navidad. Mamá, papá, mi hermana, el amigo invisible… y un caprichito para mí. [pause] [sighs] El año pasado hice lo mismo… y llegué a enero sin un euro. [warmly] Este año, antes de pagar, miro en Propera lo que realmente puedo gastar hasta cobrar. Los regalos caben. El capricho… [laughs softly] que espere a las rebajas. [happy] Los mismos regalos, sin cuesta de enero. Pruébalo gratis en propera.life.

## Historia

| Escena | Qué pasa |
|---|---|
| hook | Sentada en la cama con el portátil y los regalos (6173679): «Hoy es Black Friday: día de adelantar los regalos de Navidad.» |
| list | Plano más cerrado (6173683, con zoom); va comprando: Mamá 45 €, Papá 39 €, Mi hermana 60 €, Amigo invisible 20 € y «Un capricho para mí» 129 €. El contador «Total» sube a 293 € |
| lastyear | Corte seco, color apagado. «El año pasado hice lo mismo… y llegué a enero sin un euro.» (tirada en el suelo entre regalos → agotada) |
| fix | «Este año, antes de pagar, miro lo que realmente puedo gastar.» Propera: disponible real hasta cobrar 210 €. Los 4 regalos ✓, el capricho ✕ «→ rebajas de enero». «Regalos: 164 € · me quedan 46 €» |
| happy | Feliz con sus regalos: «Los mismos regalos. Sin cuesta de enero.» |
| end | Cierre de marca |

## Archivos

- **`reel_regalos_v3.mp4`: con la voz de Silvia (`voz.mp3`) y música de ElevenLabs**; sin los planos en los que sale tumbada boca abajo con el portátil. `reel_regalos_v2.mp4`: empieza sentada en la cama, sin voz. `reel_regalos_v1.mp4`: primera versión.
- `regalos.py` (escenas), `timeline.json` (tiempos y `beats`), `build.sh` (`./build.sh`; `VOZ=voz.mp3 ./build.sh` mezcla la voz).
- Música: `musica/eleven_navidad.mp3` (ElevenLabs Music, pop navideño, 35 s) adaptada a las escenas con `mix_musica.py`: se apaga en «el año pasado», vuelve contenida con Propera y a tope en el final. Si falta, `build.sh` usa la sintetizada (`synth.py xmas`, `xmas_lofi` o `xmas_swing` con `MUSICA_OPCION`).
- Clips en `../media/regalos/` (Pexels, verticales 1080×1920): 6173679, 6173683, 6173854, 6174040, 6173681, 6173883 (y otros de la misma sesión). No usar 6173793/6173794/6173795: sale tumbada boca abajo con el portátil.

## Reglas

- Portada: `portada.png` (`portada.py`): «Regalos de Navidad en el Black Friday…» + «¿y en enero?».
- Créditos al publicar: Vídeos: **Leeloo The First** (Pexels; misma sesión que sus fotos 6173332–6173354) · Música: ElevenLabs · «Historia ficticia, interpretada por actores».
- No decir que Propera «reserva» dinero; hablar de lo que realmente puedes gastar.

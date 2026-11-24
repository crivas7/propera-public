# Reel «Los regalos» (Black Friday + Navidad)

Reel vertical (1080×1920, 30 fps) para el **viernes 27 de noviembre de 2026**, el día del Black Friday. Cierra la semana: el lunes fue «La ganga» (no era una ganga), hoy toca «regalos sí, pero con cabeza» y el lunes 30, Marcos con el día 30.

La protagonista es un **personaje nuevo** (no es la chica de «La ganga», que solo tiene clips de un día y con la misma ropa) y no es una clienta real.

## Guion de la voz

ElevenLabs, modelo `eleven_v4`, voz **Silvia Expresiva** (`DNtbMnLZ43q8pReedyYw`, joven, España; distinta de Gala):

> [excited] Hoy es Black Friday: día de adelantar los regalos de Navidad. Mamá, papá, mi hermana, el amigo invisible… y un caprichito para mí. [pause] [sighs] El año pasado hice lo mismo… y llegué a enero sin un euro. [warmly] Este año, antes de pagar, miro en Propera lo que realmente puedo gastar hasta cobrar. Los regalos caben. El capricho… [laughs softly] que espere a las rebajas. [happy] Los mismos regalos, sin cuesta de enero. Pruébalo gratis en propera.life.

## Historia

| Escena | Qué pasa |
|---|---|
| hook | En la cama con el portátil y los regalos: «Hoy es Black Friday: día de adelantar los regalos de Navidad.» |
| list | Va comprando: Mamá 45 €, Papá 39 €, Mi hermana 60 €, Amigo invisible 20 € y «Un capricho para mí» 129 €. El contador «Total» sube a 293 € |
| lastyear | Corte seco, color apagado. «El año pasado hice lo mismo… y llegué a enero sin un euro.» (tirada en el suelo entre regalos → agotada) |
| fix | «Este año, antes de pagar, miro lo que realmente puedo gastar.» Propera: disponible real hasta cobrar 210 €. Los 4 regalos ✓, el capricho ✕ «→ rebajas de enero». «Regalos: 164 € · me quedan 46 €» |
| happy | Feliz con sus regalos: «Los mismos regalos. Sin cuesta de enero.» |
| end | Cierre de marca |

## Archivos

- `reel_regalos_v1.mp4`: primera versión, sin voz (tiempos estimados).
- `regalos.py` (escenas), `timeline.json` (tiempos y `beats`), `build.sh` (`./build.sh`; `VOZ=voz.mp3 ./build.sh` mezcla la voz).
- Música original: `../reel-marcos/musica/synth.py xmas` (pop navideño con cascabeles; se apaga en «el año pasado» y vuelve con Propera). `build.sh` la regenera con los tiempos del timeline.
- Clips en `../media/regalos/` (Pexels, verticales 1080×1920): 6173794, 6173793, 6173795, 6173854, 6174040, 6173681, 6173883 (y otros de la misma sesión).

## Reglas

- Créditos al publicar: autor de los vídeos (por confirmar en Pexels; las fotos de la misma sesión son de **Leeloo The First**) · Música original · «Historia ficticia, interpretada por actores».
- No decir que Propera «reserva» dinero; hablar de lo que realmente puedes gastar.

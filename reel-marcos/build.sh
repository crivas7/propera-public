#!/usr/bin/env bash
# Reel «Día 30» (Marcos) v2. Todos los planos son del mismo actor (sesión de Mikhail Nilov en Pexels).
#   ./build.sh              -> out/reel_marcos_sin_voz.mp4 (música, sin voz)
#   VOZ=voz.wav ./build.sh  -> out/reel_marcos_con_voz.mp4 (voz + ducking + subtítulos)
set -e
cd "$(dirname "$0")"
M=../media/marcos; MUS=../685446693-60628f34-2042-4e8a-bd58-d5e154bd5059.mp4
V="scale=1080:1920:flags=lanczos,setsar=1"                 # clips verticales
C() { echo "crop=608:1080:$(( $1 - 304 )):0,scale=1080:1920:flags=lanczos,setsar=1"; }  # recorte vertical de clips 16:9
[ -n "$SOLO_MEZCLA" ] || { rm -rf work && mkdir -p work/frames out; }
seg() {  # seg NOMBRE CLIP INICIO DURACION FILTRO
  mkdir -p work/$1
  ffmpeg -v error -y -ss $3 -t $4 -i $M/pexels_nilov_$2.mp4 -vf "$5,fps=30" -q:v 2 work/$1/%04d.jpg
}
if [ -z "$SOLO_MEZCLA" ]; then
seg hook  6898111 0.6  4.7 "$V"            # día 30: mira el móvil junto a la ventana
seg r1    6898113 6.0  2.7 "$V"            # recuerdo: desembala un pedido
seg r2    6898022 4.0  1.7 "$(C 780)"      # recuerdo: paga online con la tarjeta
seg r3    6898100 4.0  1.7 "$V"            # recuerdo: pide comida en el móvil
seg r4    6898101 5.0  1.7 "$V"            # recuerdo: recoge otro pedido de noche
seg d1bg  6898026 0.3  7.6 "$(C 1150)"     # sus manos con el móvil (fondo del día 1)
seg voice_a 6898016 22.85 2.45 "$(C 760),setpts=1.4*PTS"  # le dicta el gasto al móvil (a 0,7x, dura 3,43 s)
seg voice_b 6898016 25.3 1.6 "$(C 760)"    # baja el móvil y se queda tranquilo
seg d30   6898010 12.2 2.6 "$(C 700)"      # día 30: mira el móvil y sonríe
fi
[ -n "$SOLO_TRAMOS" ] && { echo "Tramos listos en work/"; exit 0; }
# SOLO_MEZCLA=1 reutiliza work/frames y solo rehace el audio
if [ -n "$VOZ" ]; then
  [ -n "$SOLO_MEZCLA" ] || SUBS=1 python3 marcos.py work work/frames
  ffmpeg -v error -y -framerate 30 -i work/frames/%04d.png -i $MUS -i "$VOZ" \
    -filter_complex "[1:a]apad,volume=0.9[m];[2:a]adelay=${VOZ_DESFASE_MS:-300},apad,volume=1.6,asplit=2[v][sc];[m][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[md];[md][v]amix=inputs=2:duration=first:normalize=0,afade=t=out:st=29:d=2,loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
    -map 0:v -map "[a]" -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -c:a aac -b:a 160k -t 31 -movflags +faststart out/reel_marcos_con_voz.mp4
  echo "OK -> out/reel_marcos_con_voz.mp4"
else
  python3 marcos.py work work/frames
  ffmpeg -v error -y -framerate 30 -i work/frames/%04d.png -i $MUS -map 0:v -map 1:a \
    -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p \
    -af "apad,afade=t=out:st=29:d=2" -c:a aac -b:a 160k -t 31 -movflags +faststart out/reel_marcos_sin_voz.mp4
  echo "OK -> out/reel_marcos_sin_voz.mp4"
fi

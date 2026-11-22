#!/usr/bin/env bash
# Reel «El chollo» (Black Friday). Sin voz: textos en pantalla + música original (musica/musica_bf.wav).
#   ./build.sh                 -> out/reel_bf.mp4
#   SOLO_TRAMOS=1 ./build.sh   -> solo prepara los fotogramas de los clips
# La música se regenera con: python3 ../reel-marcos/musica/synth.py bf musica/musica_bf.wav 32.6
set -e
cd "$(dirname "$0")"
DUR=$(python3 -c "import json;print(json.load(open('timeline.json'))['DUR'])")
M=../media/blackfriday
V="scale=1080:1920:flags=lanczos,setsar=1"
rm -rf work && mkdir -p work/frames out
seg() { mkdir -p work/$1; ffmpeg -v error -y -ss $3 -t $4 -i $M/pexels_nilov_$2.mp4 -vf "$V,fps=30" -q:v 2 work/$1/%04d.jpg; }
seg hook  6898098 13.5 3.7   # abre los paquetes, encantada
seg m1    6898106 2.0  1.8   # compra en el portátil (chaqueta)
seg m2    6898110 5.5  1.8   # compra en la cocina (zapatillas)
seg m3    6898109 2.2  1.8   # compra con el móvil (auriculares)
seg m4    6898098 5.4  1.8   # abre otra caja (freidora)
seg haul  6898105 12.5 3.0   # se prueba la chaqueta
seg twist 6898112 1.0  4.3   # junto a la ventana, mirando el banco
seg fixbg 6898106 8.0  6.7   # fondo de la escena de Propera
seg happy 6898105 18.7 2.7   # con la chaqueta, contenta
[ -n "$SOLO_TRAMOS" ] && { echo "Tramos listos en work/"; exit 0; }
python3 bf.py work work/frames
ffmpeg -v error -y -framerate 30 -i work/frames/%04d.png -i musica/musica_bf.wav -map 0:v -map 1:a \
  -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p \
  -af "apad,loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.84:level=false" -c:a aac -ar 48000 -b:a 160k -t $DUR -movflags +faststart out/reel_bf.mp4
echo "OK -> out/reel_bf.mp4"

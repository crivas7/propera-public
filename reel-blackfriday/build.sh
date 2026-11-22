#!/usr/bin/env bash
# Reel «La ganga» (Black Friday). Voz de la protagonista + textos en pantalla + música original.
#   ./build.sh                    -> out/reel_bf.mp4 (sin voz)
#   VOZ=voz.wav ./build.sh        -> con voz; la música baja mientras habla (VOZ_DESFASE_MS, por defecto 300)
#   SOLO_TRAMOS=1 ./build.sh      -> solo prepara los fotogramas de los clips
# La música (musica/musica_bf.wav) se regenera sola con los tiempos de timeline.json.
set -e
cd "$(dirname "$0")"
DUR=$(python3 -c "import json;print(json.load(open('timeline.json'))['DUR'])")
M=../media/blackfriday
V="scale=1080:1920:flags=lanczos,setsar=1"
rm -rf work && mkdir -p work/frames out
seg() { mkdir -p work/$1; ffmpeg -v error -y -ss $3 -t $4 -i $M/pexels_nilov_$2.mp4 -vf "$V,fps=30" -q:v 2 work/$1/%04d.jpg; }
seg hook  6898098 13.5 4.0   # abre los paquetes, encantada
seg m1    6898106 2.0  2.6   # compra en el portátil (chaqueta)
seg m2    6898110 5.5  2.6   # compra en la cocina (zapatillas)
seg m3    6898109 2.2  2.6   # compra con el móvil (auriculares)
seg m4    6898098 5.4  2.6   # abre otra caja (freidora)
seg haul  6898105 9.6  3.8   # saca la chaqueta y la abraza (corte en la acción desde la caja)
seg twist 6898112 1.0  11.5  # junto a la ventana, mirando el banco
seg fixbg 6898106 8.0  9.0   # fondo de la escena de Propera
seg happy 6898105 18.7 3.6   # con la chaqueta, contenta
[ -n "$SOLO_TRAMOS" ] && { echo "Tramos listos en work/"; exit 0; }
BF_T=$(python3 -c "import json;t=json.load(open('timeline.json'));print(','.join(str(t[k]) for k in ('twist','fix','happy','end')))")
BF_T=$BF_T python3 ../reel-marcos/musica/synth.py bf musica/musica_bf.wav $DUR
python3 bf.py work work/frames
NORM="loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.84:level=false"
if [ -n "$VOZ" ]; then
  D=${VOZ_DESFASE_MS:-300}
  TW=$(python3 -c "import json;print(json.load(open('timeline.json'))['twist'])")
  # música por debajo de la voz: el pop de compras (hasta el giro) viene más fuerte, se baja más
  ffmpeg -v error -y -framerate 30 -i work/frames/%04d.png -i musica/musica_bf.wav -i "$VOZ" \
    -filter_complex "[1:a]volume='if(lt(t,$TW),0.3,0.55)':eval=frame,apad[m];[2:a]adelay=$D|$D,apad,volume=1.6,asplit=2[v][sc];[m][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[md];[md][v]amix=inputs=2:duration=first:normalize=0,$NORM[a]" \
    -map 0:v -map "[a]" -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -c:a aac -ar 48000 -b:a 160k -t $DUR -movflags +faststart out/reel_bf.mp4
else
  ffmpeg -v error -y -framerate 30 -i work/frames/%04d.png -i musica/musica_bf.wav -map 0:v -map 1:a \
    -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p \
    -af "apad,$NORM" -c:a aac -ar 48000 -b:a 160k -t $DUR -movflags +faststart out/reel_bf.mp4
fi
echo "OK -> out/reel_bf.mp4"

#!/usr/bin/env bash
# Reel «Los regalos» (Black Friday + Navidad). Voz de la protagonista + textos en pantalla + música original.
#   ./build.sh                    -> out/reel_regalos.mp4 (sin voz)
#   VOZ=voz.mp3 ./build.sh        -> con voz; la música baja mientras habla (VOZ_DESFASE_MS, por defecto 300)
#   SOLO_TRAMOS=1 ./build.sh      -> solo prepara los fotogramas de los clips
# La música (musica/musica_regalos.wav) se regenera sola con los tiempos de timeline.json.
set -e
cd "$(dirname "$0")"
DUR=$(python3 -c "import json;print(json.load(open('timeline.json'))['DUR'])")
M=../media/regalos
V="scale=1080:1920:flags=lanczos,setsar=1"
rm -rf work && mkdir -p work/frames out musica
seg() { mkdir -p work/$1; ffmpeg -v error -y -ss $3 -t $4 -i $M/pexels_xmas_$2.mp4 -vf "$V,fps=30" -q:v 2 work/$1/%04d.jpg; }
seg hook  6173794 0.3 7.4    # tumbada en la cama con el portátil y los regalos
seg list1 6173793 0.2 6.5    # compra en el portátil (cerca)
seg list2 6173795 0.3 8.4    # sigue comprando, rodeada de regalos
seg ly1   6173854 0.5 9.5    # el año pasado: tirada en el suelo entre regalos
seg ly2   6174040 0.2 5.0    # y en enero: agotada
seg fixbg 6173681 0.0 12.3   # revisa los regalos (fondo de Propera)
seg happy 6173883 0.0 4.6    # feliz con sus regalos
[ -n "$SOLO_TRAMOS" ] && { echo "Tramos listos en work/"; exit 0; }
XM_T=$(python3 -c "import json;t=json.load(open('timeline.json'));print(','.join(str(t[k]) for k in ('lastyear','fix','happy','end')))")
XM_T=$XM_T python3 ../reel-marcos/musica/synth.py xmas musica/musica_regalos.wav $DUR
python3 regalos.py work work/frames
NORM="loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.84:level=false"
if [ -n "$VOZ" ]; then
  D=${VOZ_DESFASE_MS:-300}
  ffmpeg -v error -y -framerate 30 -i work/frames/%04d.png -i musica/musica_regalos.wav -i "$VOZ" \
    -filter_complex "[1:a]volume=0.4,apad[m];[2:a]adelay=$D|$D,apad,volume=1.6,asplit=2[v][sc];[m][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[md];[md][v]amix=inputs=2:duration=first:normalize=0,$NORM[a]" \
    -map 0:v -map "[a]" -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -c:a aac -ar 48000 -b:a 160k -t $DUR -movflags +faststart out/reel_regalos.mp4
else
  ffmpeg -v error -y -framerate 30 -i work/frames/%04d.png -i musica/musica_regalos.wav -map 0:v -map 1:a \
    -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p \
    -af "apad,$NORM" -c:a aac -ar 48000 -b:a 160k -t $DUR -movflags +faststart out/reel_regalos.mp4
fi
echo "OK -> out/reel_regalos.mp4"

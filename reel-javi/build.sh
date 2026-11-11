#!/usr/bin/env bash
# Reconstruye el reel de Javi (sin voz). Ejecutar desde reel-javi/
set -e
cd "$(dirname "$0")"
Z=../media/pexels_zapatillas_7680115.mp4; M=../media/pexels_movil_8165696.mp4
rm -rf work && mkdir -p work/c1 work/c2 work/frames out
ffmpeg -v error -y -ss 1.0 -t 8.6 -i $Z -vf "fps=30,scale=-2:1920,crop=1080:1920" -q:v 3 work/c1/%04d.jpg
ffmpeg -v error -y -i $M -vf "setpts=PTS*1.12,fps=30,scale=1080:-2,crop=1080:1920:0:64" -q:v 3 work/c2/%04d.jpg
cp render.py render2.py work/
python3 work/render2.py work/frames
ffmpeg -v error -y -framerate 30 -i work/frames/%04d.png -i ../685446693-60628f34-2042-4e8a-bd58-d5e154bd5059.mp4 \
  -map 0:v -map 1:a -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p \
  -af "apad,afade=t=out:st=28.5:d=2" -c:a aac -b:a 160k -t 31 -movflags +faststart out/reel_javi_sin_voz.mp4
echo "OK -> out/reel_javi_sin_voz.mp4"

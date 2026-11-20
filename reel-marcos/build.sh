#!/usr/bin/env bash
# Reel «Día 30» (Marcos). Ejecutar desde cualquier sitio.
#   ./build.sh            -> out/reel_marcos_sin_voz.mp4 (música, sin voz)
#   VOZ=voz.wav ./build.sh -> out/reel_marcos_con_voz.mp4 (voz + ducking + subtítulos)
set -e
cd "$(dirname "$0")"
M=../media/pexels_movil_8165696.mp4; MUS=../685446693-60628f34-2042-4e8a-bd58-d5e154bd5059.mp4
rm -rf work && mkdir -p work/c_movil work/frames out
ffmpeg -v error -y -i $M -vf "setpts=PTS*1.12,fps=30,scale=1080:-2,crop=1080:1920:0:64" -q:v 3 work/c_movil/%04d.jpg
if [ -n "$VOZ" ]; then
  SUBS=1 python3 marcos.py work work/frames
  ffmpeg -v error -y -framerate 30 -i work/frames/%04d.png -i $MUS -i "$VOZ" \
    -filter_complex "[1:a]apad,volume=0.9[m];[2:a]apad,volume=1.6,asplit=2[v][sc];[m][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[md];[md][v]amix=inputs=2:duration=first:normalize=0,afade=t=out:st=29:d=2[a]" \
    -map 0:v -map "[a]" -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -c:a aac -b:a 160k -t 31 -movflags +faststart out/reel_marcos_con_voz.mp4
  echo "OK -> out/reel_marcos_con_voz.mp4"
else
  python3 marcos.py work work/frames
  ffmpeg -v error -y -framerate 30 -i work/frames/%04d.png -i $MUS -map 0:v -map 1:a \
    -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p \
    -af "apad,afade=t=out:st=29:d=2" -c:a aac -b:a 160k -t 31 -movflags +faststart out/reel_marcos_sin_voz.mp4
  echo "OK -> out/reel_marcos_sin_voz.mp4"
fi

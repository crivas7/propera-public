#!/usr/bin/env bash
set -e
cd /home/claude
OUTNAME=${1:-propera_reel_lucia_borrador}
rm -rf work/lf work/lfs
python3 work/lucia_reel.py work/lf
python3 work/subs_lucia.py work/lf work/lfs
V=work/voice/voz_lucia.mp3; V2=work/voice/voz_lucia_s2.mp3; M=propera-public/685446693-60628f34-2042-4e8a-bd58-d5e154bd5059.mp4
ffmpeg -v error -y -framerate 30 -i work/lfs/%04d.png -i $V -i $V2 -i $M -i work/sfx_lucia.wav -filter_complex "\
[1:a]atrim=0:3.33,asetpts=PTS-STARTPTS,adelay=200|200[a];\
[2:a]atrim=0:6.58,asetpts=PTS-STARTPTS,adelay=4200|4200[b];\
[1:a]atrim=10.70:16.36,asetpts=PTS-STARTPTS,adelay=11000|11000[c];\
[1:a]atrim=16.95:22.47,asetpts=PTS-STARTPTS,adelay=17000|17000[d];\
[1:a]atrim=23.00:28.59,asetpts=PTS-STARTPTS,adelay=22600|22600[e];\
[1:a]atrim=28.95:32.68,asetpts=PTS-STARTPTS,adelay=28700|28700[f];\
[a][b][c][d][e][f]amix=inputs=6:normalize=0,apad,atrim=0:32.5,asplit[vo][sc];\
[3:a]aloop=loop=1:size=2147483647,apad,atrim=0:32.5,volume=0.5,afade=t=out:st=30.8:d=1.7[mu];\
[mu][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=350[duck];\
[4:a]aformat=channel_layouts=stereo,volume=0.9[fx];\
[vo][duck][fx]amix=inputs=3:normalize=0,alimiter=limit=0.95[aout]" \
-map 0:v -map "[aout]" -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k -t 32.5 -movflags +faststart out/$OUTNAME.mp4
echo done out/$OUTNAME.mp4

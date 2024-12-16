ffmpeg -i %1 -vcodec h264 -profile:v main -vf "vflip" "%1_vflip.mp4"
pause
ffmpeg -i %1 -vcodec h264 -profile:v main -to 0:0:5 "%1_short.mp4"
pause
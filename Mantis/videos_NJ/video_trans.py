
import cv2
import sys
from tqdm import tqdm

video_file = sys.argv[1]
# NOTE: single file (xxx.avi), in the same directory
output_video = video_file.replace(".avi", "_c.avi")
cap = cv2.VideoCapture(video_file)

fourcc = "MJPG"
total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
vw = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*fourcc), fps, size)
real_frame = 0
for i in tqdm(range(total_frame)):
    ret, img = cap.read()
    if not ret:
        break
    img1 = 255 - img

    # img1[:, :, 0] = 0  #B
    # img1[:, :, 1] = 0  #G
    img1[:, :, 2] = 0  #R

    vw.write(img1)
    real_frame += 1
print("\n finish\ntotal: %d, real: %d" % (total_frame, real_frame))
vw.release()

import os
import matplotlib.pyplot as plt
import numpy as np
import cv2

out_path = r"G:\simple_stim"
v = 100
r = 15

bg_color = (255, 255, 255)
dot_color = (0, 0, 0)

fps = 60  # frame/s
video_w = 300  # pixel
video_h = 200  # pixel

run_range = video_w
duration = 2 * run_range / v
repeat_n = int(30/duration)
image_n = int(fps * duration)
dot_to_r_x = np.linspace(r, video_w - r, int(image_n / 2))
dot_to_l_x = np.linspace(video_w - r, r, int(image_n / 2))
dot_x = np.concatenate((dot_to_r_x, dot_to_l_x))
# dot_y = np.full((dot_n, 1), video_h/2)

output_video_name = "dot_%spixel_%sv_%ss" % (r, v, duration)
output_video_path = os.path.join(out_path, output_video_name + ".avi")
output_video = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*"MJPG"), fps, (video_w, video_h))

for repeat in range(repeat_n):
    for i in range(image_n):
        img = np.ones((video_h, video_w, 3), dtype="uint8")
        img[:] = bg_color
        center = (round(dot_x[i]), round(video_h/2))
        cv2.circle(img, center, r, dot_color, -1)
        # cv2.imshow("1", img)
        # cv2.waitKey(1)
        # output_video.write(cv2.cvtColor(img, cv2.COLOR_GRAY2BGR))
        output_video.write(img)
# output_video.release()

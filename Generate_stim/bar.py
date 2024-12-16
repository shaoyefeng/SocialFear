import os
import matplotlib.pyplot as plt
import numpy as np
import cv2

out_path = r"G:\simple_stim"
v = 100
bar_width = 15

bg_color = (255, 255, 255)
bar_color = (0, 0, 0)

fps = 60  # frame/s
video_w = 300  # pixel
video_h = 200  # pixel

run_range = video_w
duration = 2 * run_range / v
repeat_n = int(30/duration)
image_n = int(fps * duration)
bar_to_r_x = np.linspace(0, video_w - bar_width, int(image_n / 2))
bar_to_l_x = np.linspace(video_w - bar_width, 0, int(image_n / 2))
bar_x = np.concatenate((bar_to_r_x, bar_to_l_x))

output_video_name = "bar_%spixel_%sv_%ss" % (bar_width, v, duration)
output_video_path = os.path.join(out_path, output_video_name + ".avi")
output_video = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*"MJPG"), fps, (video_w, video_h))

for repeat in range(repeat_n):
    for i in range(image_n):
        img = np.ones((video_h, video_w, 3), dtype="uint8")
        img[:] = bg_color
        center = (round(bar_x[i]), round(video_h/2))
        cv2.rectangle(img, (round(bar_x[i]), 0), (round(bar_x[i]+bar_width), video_h), bar_color, -1)
        # cv2.imshow("1", img)
        # cv2.waitKey(1)
        # output_video.write(cv2.cvtColor(img, cv2.COLOR_GRAY2BGR))
        output_video.write(img)
# output_video.release()

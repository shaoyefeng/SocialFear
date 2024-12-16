import os
import matplotlib.pyplot as plt
import numpy as np
import cv2

out_path = r"G:\simple_stim"
v = 60
stripe_width = 15
bg_color = (255, 255, 255)
stripe_color = (0, 0, 0)

fps = 60  # frame/s
video_w = 300  # pixel
video_h = 200  # pixel

run_range = video_w
duration = 2*run_range / v
stripe_n = round(video_w/(stripe_width*2))
image_n = int(fps * duration)
repeat_n = int(30/duration)

loop_width = int(stripe_n * 2 * stripe_width)
grating_x = []
for n in range(stripe_n):
    stripe_to_r_x = np.linspace(0, video_w, int(image_n / 2)) + n * stripe_width * 2
    stripe_to_l_x = np.linspace(video_w, 0, int(image_n / 2)) + n * stripe_width * 2
    stripe_x = np.concatenate((stripe_to_r_x, stripe_to_l_x))
    stripe_x = stripe_x % loop_width
    stripe_x[stripe_x > loop_width - stripe_width] = stripe_x[stripe_x > loop_width - stripe_width] - loop_width
    grating_x.append([x for x in stripe_x])

output_video_name = "grating_%sv_%ss" % (v, duration)
output_video_path = os.path.join(out_path, output_video_name + ".avi")
output_video = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*"MJPG"), fps, (video_w, video_h))

for repeat in range(repeat_n):
    for i in range(image_n):
        img = np.ones((video_h, video_w, 3), dtype="uint8")
        img[:] = bg_color
        for j in range(stripe_n):
            cv2.rectangle(img, (int(grating_x[j][i]), 0), (int(grating_x[j][i] + stripe_width), video_h), stripe_color, -1)
        # cv2.imshow("1", img)
        # cv2.waitKey(1)
        # output_video.write(cv2.cvtColor(img, cv2.COLOR_GRAY2BGR))
        output_video.write(img)
# output_video.release()

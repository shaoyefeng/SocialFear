import os

import matplotlib.pyplot as plt
import numpy as np
import cv2

out_path = r"F:\FoB\visual_stimulation"
scr_pix_per_deg = 256/270
fps = 50
duration = 2
persist = 0.7
total_duration = 5.4
repeat = int(total_duration/(duration + persist))
r = 8  # cm
v = 160  # cm/s (r/v=50ms)
video_w = 256  # pix
video_h = 64  # pix
bg_color = np.array([0, 0, 255])
circle_color = (0, 0, 0)

t = np.arange(-duration, 0, 1/fps)
ang = 2*np.rad2deg(np.arctan(r/(-v*t)))
# plt.plot(t, ang)
# v = 20
# ang = 2*np.rad2deg(np.arctan(r/(-v*t)))

mi, ma = np.min(ang), np.max(ang)
wid = np.concatenate([(ang-mi)/(ma-mi) * video_h, np.full((int(persist*fps),), video_h)])
plt.plot(wid)
# plt.show()
name = "looming_%sv%ss%ss%ss" % (v, duration, persist, total_duration)
fig_path = os.path.join(out_path, name + ".png")
video_path = os.path.join(out_path, name + ".avi")
plt.savefig(fig_path)

output_video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*"MJPG"), fps, (video_w, video_h))
center = (int(video_w/2), int(video_h/2))
bg_color[0], bg_color[2] = bg_color[2], bg_color[0]
for i in range(repeat):
    for ww in wid:
        # img = np.full((video_h, video_w), 255, dtype=np.uint8)
        img = np.ones((video_h, video_w, 3), dtype="uint8")

        img[:] = bg_color
        cv2.circle(img, center, int(ww/2), circle_color, -1)
        # cv2.imshow("1", img)
        # cv2.waitKey(1)
        # output_video.write(cv2.cvtColor(img, cv2.COLOR_GRAY2BGR))
        output_video.write(img)
# output_video.release()

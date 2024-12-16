import random
import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt

input_video = r"F:\Code\SocialFear\Mantis\videos\c.avi"
output_video = r"F:\Code\SocialFear\Mantis\videos\c_total_random.avi"
image = r"F:\Code\SocialFear\Mantis\videos\gray_value.jpg"

cap = cv2.VideoCapture(input_video)
total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
video_w, video_h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# output_video = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*"MJPG"), fps, (video_w, video_h))

mean_gray_value = []
for seq in range(0, total_frame):
    ret, img = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img = img[:, :, 0]
    f = gray.flatten()
    mean_gray_value.append(f.mean())
    random.seed(8)
    random.shuffle(f)
    s = np.reshape(f, gray.shape)
    gray = s
    img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    # cv2.imshow("", img)
    # cv2.waitKey(1)
    # output_video.write(img)
    print(seq)
plt.plot(mean_gray_value)
plt.show()
cap.release()

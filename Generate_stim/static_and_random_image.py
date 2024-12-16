import random
import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt

input_video = r"G:\simple_stim\grating_60v_10.0s.avi"

cap = cv2.VideoCapture(input_video)
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
video_w, video_h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

ret, img = cap.read()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
f = gray.flatten()
random.seed(8)
random.shuffle(f)
s = np.reshape(f, gray.shape)
img = cv2.cvtColor(s, cv2.COLOR_GRAY2BGR)
cv2.imwrite(r"G:\simple_stim\grating_random.jpg", img)

cap.release()

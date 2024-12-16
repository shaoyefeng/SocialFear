import random
import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import cm

input_video = r"F:\Code\SocialFear\Mantis\videos\c.avi"
output_video = r"F:\Code\SocialFear\Mantis\videos\c_total_random.avi"

cap = cv2.VideoCapture(input_video)
total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

mean_gray_value = []
for seq in range(0, total_frame):
    ret, img = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    f = gray.flatten()
    mean_gray_value.append(f.mean())
    print(seq)

fig, ax = plt.subplots(figsize=(20, 8))
plt.subplots_adjust(left=0.05, right=0.99, wspace=0.03)
plt.plot(mean_gray_value)
stim_resp_df = pd.read_pickle(r"G:\ambushes\stim_resp.pickle")
cmap = cm.get_cmap('rainbow', len(stim_resp_df))
colors = np.linspace(1, 0, len(stim_resp_df))
for i in range(len(stim_resp_df)):
    plt.axvline(stim_resp_df.iloc[i]['start_frame'], linewidth=0.5, color=cmap(colors[i]))
    plt.axvline(stim_resp_df.iloc[i]['end_frame'], linewidth=0.5, color=cmap(colors[i]))
plt.savefig(r"G:\ambushes\gray_value.png")
cap.release()

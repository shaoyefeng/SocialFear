import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
import seaborn as sns
import numpy as np
from glob import glob

logpath = r"G:\20220614\log"
bins = 500

trial_interval = []
for log in glob(logpath+'/*.log'):
    PC_start = []
    for line in open(log, 'r'):
        if line.startswith('START'):
            start = float(line.split(' ')[1])
            PC_start.append(start)
    PC_start = np.array(PC_start)
    interval = np.diff(PC_start).tolist()
    trial_interval.extend(interval)
fig, ax = plt.subplots(figsize=(20, 8))
ax.hist(x=trial_interval, bins=bins)
# plt.show()
plt.savefig(logpath)
#
# trial_interval = np.array([])
# PC_start = np.array([])
# for line in open(r"D:\2022\analysis\20220412\20220412_1\20220412_162241.log", 'r'):
#     if line.startswith('START'):
#         start = float(line.split(' ')[1])
#         PC_start = np.append(PC_start, start)
# PC_start = np.array(PC_start)
# interval = np.diff(PC_start)
# trial_interval = np.append(trial_interval, interval)
# trial_interval.flatten()
# fig, ax = plt.subplots(figsize=(20, 8))
# ax.hist(x=trial_interval, bins=500)
# plt.show()

#
# video_start = []
# video_end = []
# for log in glob(path+'/*.log'):
#     for line in open(log, 'r'):
#         if line.startswith('video_start'):
#             start = float(line.split(' ')[1])
#             video_start.append(start)
#         elif line.startswith('video_end'):
#             end = float(line.split(' ')[1])
#             video_end.append(end)
# active_interval = np.array(video_end) - np.array(video_start)
#
# static_start = []
# static_end = []
# for log in glob(path+'/*.log'):
#     for line in open(log, 'r'):
#         if line.startswith('static_start'):
#             start = float(line.split(' ')[1])
#             static_start.append(start)
#         elif line.startswith('static_end'):
#             end = float(line.split(' ')[1])
#             static_end.append(end)
# static_interval = np.array(static_end) - np.array(static_start)

# random_start = []
# random_end = []
# for log in glob(path+'/*.log'):
#     for line in open(log, 'r'):
#         if line.startswith('random_start'):
#             start = float(line.split(' ')[1])
#             random_start.append(start)
#         elif line.startswith('random_end'):
#             end = float(line.split(' ')[1])
#             random_end.append(end)
# random_interval = np.array(random_end) - np.array(random_start)


# fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(20, 5))
# ax0 = axes[0]
# ax0.hist(x=active_interval, bins=50)
# ax1 = axes[1]
# ax1.hist(x=static_interval, bins=50)
# ax2 = axes[2]
# ax2.hist(x=trial_interval, bins=500)

# video_len = []
# for a in glob(r"D:\2022\analysis\single/*"):
#     for b in glob(a+'/*'):
#         for c in glob(b+'/*'):
#             df = pd.read_csv(c)
#             video_len.append(len(df))
#             print(c)
# fig, ax = plt.subplots(figsize=(20, 8))
# ax.hist(x=video_len, bins=500)
# plt.show()
# 108000 + (-9) = 107991




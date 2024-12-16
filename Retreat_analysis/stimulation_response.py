import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import cv2
import seaborn as sns
import numpy as np
from matplotlib import cm
from glob import glob

from Function_analysis import ava_filter

stim_path = r"G:\ambushes"
video_path = r"F:\Code\SocialFear\Mantis\videos\c.avi"


ambush_frame_list = []
for img_path in os.listdir(stim_path):
    if 'ambush' in img_path:
        pair = (img_path.split(' ')[-1]).split('.')[0]
        ambush = int(pair.split('_')[0])
        frame = int(pair.split('_')[-1])
        ambush_frame_list.append([ambush, frame])
ambush_frame_list = np.reshape(ambush_frame_list, (-1, 2, 2))

#  stimulation
annot_path = glob(stim_path + '/*.json')[0]
annot_dict = json.load(open(annot_path))["annotations"]
frame_keypoint_dict = {}
for annot in annot_dict:
    keypoint = np.reshape(annot["keypoints"], (-1, 3))
    frame_keypoint_dict[annot["id"]] = keypoint[:, :2]

start_frame = []
end_frame = []
ambush_list = []
dist_list = []
for ambush_frame in ambush_frame_list:
    ambush = ambush_frame[0, 0]
    frame_start = ambush_frame[0, 1]
    frame_end = ambush_frame[1, 1]
    keypoint_start = frame_keypoint_dict[frame_start]
    keypoint_end = frame_keypoint_dict[frame_end]
    dist = 0
    for i in range(15):
        keypoint_dist = np.sqrt(np.sum(np.square(keypoint_start[i] - keypoint_end[i])))
        dist += keypoint_dist
    ambush_list.append(ambush)
    start_frame.append(frame_start)
    end_frame.append(frame_end)
    dist_list.append(dist)

cap = cv2.VideoCapture(video_path)
gray_value = []
for ambush_frame in ambush_frame_list:
    ambush = ambush_frame[0, 0]
    frame_start = ambush_frame[0, 1]
    frame_end = ambush_frame[1, 1]
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_start)
    ret, img = cap.read()
    gray_value_start = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_end)
    ret, img = cap.read()
    gray_value_end = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_value_diff = gray_value_end - gray_value_start
    gray_value_diff_mean = np.mean(np.absolute(gray_value_diff.flatten()))
    # img = img[:, :, 0]
    gray_value.append(gray_value_diff_mean)

stim_resp = pd.DataFrame([])
stim_resp['ambush'] = ambush_list
stim_resp['stim_dist'] = dist_list
stim_resp['gray_value'] = gray_value
stim_resp['start_frame'] = start_frame
stim_resp['end_frame'] = end_frame
stim_resp = stim_resp.sort_values('ambush')
stim_resp.index = stim_resp['ambush']

#  response
data_path = r"D:\2022\datamerged\50fps\repeat\CS_M_4-5d"
fps = 50
blocks_n = 6

# merged_df = pd.DataFrame([])
# for block in np.arange(blocks_n):
#     for repeat_folder in os.listdir(data_path):
#         repeat_folder_path = os.path.join(data_path, repeat_folder)
#         if os.path.isdir(repeat_folder_path):
#             for fly in os.listdir(repeat_folder_path):
#                 fly_path = os.path.join(repeat_folder_path, fly)
#                 block_folders = os.listdir(fly_path)
#                 block_folders.sort(key=lambda x: int(x.split('_')[1]))
#                 block_folder_path = os.path.join(fly_path, block_folders[block])
#                 for repeat_df_path in glob(block_folder_path+'/*'):
#                     repeat_df = pd.read_csv(repeat_df_path)
#                     repeat_df['frame'] = repeat_df.index.tolist()
#                     merged_df = pd.concat([merged_df, repeat_df], ignore_index=True)
#                     print(repeat_df_path)
# meandf = merged_df.groupby('frame', as_index=False).agg('mean')
# meandf.to_pickle(r"G:\ambushes\response.pickle")

meandf = pd.read_pickle(r"G:\ambushes\response.pickle")
slope = []
area = []
fig, ax = plt.subplots(figsize=(5, 10))
cmap = cm.get_cmap('rainbow', len(stim_resp))
colors = np.linspace(1, 0, len(stim_resp))
for j in range(len(stim_resp)):
    ambush_strat = (stim_resp.iloc[j]['start_frame'])/60*fps + 0.5*60*fps
    ambush_df = meandf.iloc[int(ambush_strat): int(ambush_strat+fps*2)]
    ambush_df = ambush_df.reset_index(drop=True)
    ambush_df['frame'] = ambush_df.index
    baseline = ambush_df['posy'][0]
    ambush_df['posy'] = ambush_df['posy'] - baseline
    integral = np.trapz(ambush_df['posy'])
    area.append(integral)
    # sns.lineplot(data=ambush_df, x='frame', y='posy', ci=None, linewidth=1, err_kws={'lw': 0}, ax=ax, color=cmap(colors[j]))
    filter_df = ava_filter(ambush_df['posy'], 3)
    slope.append(filter_df[1])
    sns.lineplot(data=filter_df, ci=None, linewidth=1, err_kws={'lw': 0}, ax=ax, color=cmap(colors[j]))
# plt.savefig(r"G:\ambushes\response.png", dpi=1000)
plt.savefig(r"G:\ambushes\response_filter.png", dpi=1000)
stim_resp['slope'] = slope
stim_resp['area'] = area
stim_resp.to_pickle(r"G:\ambushes\stim_resp.pickle")








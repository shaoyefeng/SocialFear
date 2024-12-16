import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import seaborn as sns
import numpy as np
from glob import glob

def all_log(datapath):
    logpath = glob(datapath+'/*.log')[0]
    PC_start = []
    static_start = []
    static_end = []
    video_start = []
    video_end = []
    random_start = []
    random_end = []
    for line in open(logpath, 'r'):
        if line.startswith('START'):
            START = float(line.split(' ')[1])
            PC_start.append(START)
        elif line.startswith('static_start'):
            single_static_start = float(line.split(' ')[1])
            static_start.append(single_static_start)
        elif line.startswith('static_end'):
            single_static_end = float(line.split(' ')[1])
            static_end.append(single_static_end)
        elif line.startswith('video_start'):
            single_video_start = float(line.split(' ')[1])
            video_start.append(single_video_start)
        elif line.startswith('video_end'):
            single_video_end = float(line.split(' ')[1])
            video_end.append(single_video_end)
        elif line.startswith('random_start'):
            single_random_start = float(line.split(' ')[1])
            random_start.append(single_random_start)
        elif line.startswith('random_end'):
            single_random_end = float(line.split(' ')[1])
            random_end.append(single_random_end)
        elif line.startswith('END'):
            end = float(line.split(' ')[1])
    screen_start = []
    # for i, t in enumerate(video_start):
    #     if i % 5 == 0:
    #         screen_start.append(t)
    # screen_start = (np.array(PC_start) + np.array(screen_start)).tolist()
    for i, t in enumerate(static_start):
        if i % 6 == 0:
            screen_start.append(t)
    screen_start = (np.array(PC_start) + np.array(screen_start)).tolist()

    log_dict = {"PC_start": PC_start, 'screen_start': screen_start, "static_start": static_start, "static_end": static_end, "video_start": video_start, "video_end": video_end, "random_start": random_start, "random_end": random_end, 'END': end}
    return log_dict


def cd_datapath(analysis_path):
    data_path_list = []
    for exp in os.listdir(analysis_path):
        exp_path = os.path.join(analysis_path, exp)
        for data in os.listdir(exp_path):
            data_path = os.path.join(exp_path, data)
            if os.path.isdir(data_path):
                data_path_list.append(data_path)
    return data_path_list


def ava_filter(x, filt_length):
    N = len(x)
    res = []
    for i in range(N):
        if i <= filt_length // 2 or i >= N - (filt_length // 2):
            temp = x[i]
        else:
            sum = 0
            for j in range(filt_length):
                sum += x[i - filt_length // 2 + j]
            temp = sum * 1.0 / filt_length
        res.append(temp)
    return res
# v-t
# distance = [0]
# for i in range(0, len(df)-1):
#     a = df[['1:pos:x', '1:pos:y']].iloc[i]
#     b = df[['1:pos:x', '1:pos:y']].iloc[i+1]
#     dist = np.linalg.norm(a-b)
#     distance.append(dist)
# df['distance'] = distance
# df['distance(mm)'] = df['distance']/13.69
# df['velocity'] = df['distance']/frame_rate




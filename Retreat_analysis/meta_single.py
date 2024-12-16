import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import seaborn as sns
import numpy as np
from glob import glob
from Function_analysis import *

# 同一板果蝇
analysis_path = r"G:\analysis"
fps = 50   # frame rate
video_duration = 30000  # frame

# meta文件
# 'frame'（已排序）, 果蝇实际坐标'posx'和'posy'，身体朝向'body_dir'

for datapath in cd_datapath(analysis_path):
    log_dict = all_log(datapath)
    static_start = log_dict['static_start']
    PC_start = log_dict['PC_start']
    screen_start = log_dict['screen_start']
    for a in os.listdir(datapath):
        b = os.path.join(datapath, a)
        if os.path.isdir(b) and 'meta' not in a:
            date = os.path.basename(datapath).split('_')[0]
            arena = os.path.basename(datapath).split('_')[1]
            LR = a.split('_')[1]
            video_folder = os.listdir(b)
            video_folder.sort(key=lambda x: int(x.split('_')[0]))
            for i, c in enumerate(video_folder):
                d = os.path.join(b, c)
                logpath = glob(d+'/*.log')[0]
                for line in open(logpath, 'r'):
                    if 'ts:' in line:
                        camera_start = line.split(':')[4]
                camera_start = int(camera_start)/pow(10, (len(camera_start)-1-10))
                removal_frames = round((screen_start[i] - camera_start)*fps)
                for fly in os.listdir(d):
                    if fly.isdigit():
                        fly_path = os.path.join(d, fly)
                        for g in os.listdir(fly_path):
                            if g.endswith('feat.csv'):
                                df_path = os.path.join(fly_path, g)
                                meta_txt_path = df_path.replace('feat.csv', 'meta.txt')
                                meta_txt = json.load(open(meta_txt_path, 'r'))
                                scale = meta_txt['FEAT_SCALE']

                                metadata_folder_name = '%s_%s_%s_metadata' % (date, arena, LR)
                                metadata_folder_path = os.path.join(datapath, metadata_folder_name)
                                metadata_fly_path = os.path.join(metadata_folder_path, fly)
                                metadata_name = g.replace('feat', 'meta')
                                metadata_path = os.path.join(metadata_fly_path, metadata_name)
                                if not os.path.exists(metadata_folder_path):
                                    os.mkdir(metadata_folder_path)
                                if not os.path.exists(metadata_fly_path):
                                    os.mkdir(metadata_fly_path)

                                df = pd.read_csv(df_path)
                                df = df.sort_values('frame')
                                df.index = range(len(df))
                                df = df[removal_frames:len(df)]
                                df.index = range(len(df))
                                df['frame'] = df.index.values
                                df = df.iloc[:video_duration, ]

                                body_dir = []
                                for j in range(0, len(df)):
                                    xpoint = df['1:point:xs'].iloc[j]
                                    ypoint = df['1:point:ys'].iloc[j]
                                    headx = xpoint.split(' ')[0]
                                    heady = ypoint.split(' ')[0]
                                    tailx = xpoint.split(' ')[2]
                                    taily = ypoint.split(' ')[2]
                                    if int(fly) <= 3:
                                        head = (20-float(headx)/scale, float(heady)/scale)
                                        tail = (20-float(tailx)/scale, float(taily)/scale)
                                    else:
                                        head = (float(headx)/scale, 20-float(heady)/scale)
                                        tail = (float(tailx)/scale, 20-float(taily)/scale)
                                    body_dir_vector = (head[0] - tail[0], head[1] - tail[1])
                                    body_direction = np.rad2deg(np.arctan2(body_dir_vector[1], body_dir_vector[0]))
                                    body_dir.append(round(body_direction, 2))

                                if int(fly) <= 3:
                                    df['posx'] = round(20 - df['1:pos:x'] / scale, 2)
                                    df['posy'] = round(df['1:pos:y'] / scale, 2)
                                    df['body_dir'] = body_dir
                                else:
                                    df['posx'] = round(df['1:pos:x'] / scale, 2)
                                    df['posy'] = round(20 - df['1:pos:y'] / scale, 2)
                                    df['body_dir'] = body_dir
                                    # df['body_dir'] = (-np.array(body_dir)).tolist()

                                metadata = df[['frame', 'posx', 'posy', 'body_dir']]
                                metadata.to_csv(metadata_path, index=False)
                                print(metadata_path)













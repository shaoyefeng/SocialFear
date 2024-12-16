import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import json
import os
from glob import glob

from Function_analysis import *

analysis_path = r"G:\analysis"
fps = 50

for datapath in cd_datapath(analysis_path):
    log_dict = all_log(datapath)
    PC_start = np.array(log_dict['PC_start']).repeat(5)
    screen_start = np.array(log_dict['screen_start']).repeat(5)
    static_start = np.array(log_dict['static_start']).reshape(3, 6)
    repeat_start = np.delete(static_start, 5, axis=1).flatten() + PC_start - screen_start
    static_end = np.array(log_dict['static_end']).reshape(3, 6)
    repeat_end = np.delete(static_end, 0, axis=1).flatten() + PC_start - screen_start
    repeat_list = np.array([repeat_start, repeat_end]).T.reshape(-1, 5, 2)

    for metadata_folder in os.listdir(datapath):
        if 'metadata' in metadata_folder:
            metadata_folder_path = os.path.join(datapath, metadata_folder)
            repeat_folder = metadata_folder.replace('metadata', 'repeat')
            repeat_folder_path = os.path.join(datapath, repeat_folder)
            if not os.path.exists(repeat_folder_path):
                os.mkdir(repeat_folder_path)
            for fly in os.listdir(metadata_folder_path):
                repeat_fly_path = os.path.join(repeat_folder_path, fly)
                if not os.path.exists(repeat_fly_path):
                    os.mkdir(repeat_fly_path)
                fly_path = os.path.join(metadata_folder_path, fly)
                metadata = os.listdir(fly_path)
                metadata.sort(key=lambda x: int(x.split('_')[1]))
                for block_n, block in enumerate(repeat_list):
                    metadf_path = os.path.join(fly_path, metadata[block_n])
                    meta_df = pd.read_csv(metadf_path)
                    repeat_block_folder = metadata[block_n].replace('_meta.csv', '')
                    repeat_block_path = os.path.join(repeat_fly_path, repeat_block_folder)
                    if not os.path.exists(repeat_block_path):
                        os.mkdir(repeat_block_path)
                    for repeat_n, repeat in enumerate(block):
                        repeat_repeat_start = int(repeat[0] * fps)
                        repeat_repeat_end = int(repeat[1] * fps)
                        repeat_df = meta_df.iloc[repeat_repeat_start: repeat_repeat_end + 1]
                        repeat_df_name = metadata[block_n].replace('meta', 'repeat_' + str(repeat_n))
                        repeat_df_path = os.path.join(repeat_block_path, repeat_df_name)
                        repeat_df.to_csv(repeat_df_path, index=None)
                        print(repeat_df_path)
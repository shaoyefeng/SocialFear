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
    video_start = np.array(log_dict['video_start']) + PC_start
    video_end = np.array(log_dict['video_end']) + PC_start
    sti_start = video_start - screen_start
    sti_end = video_end - screen_start
    sti = np.array([sti_start, sti_end]).T.reshape(-1, 5, 2)

    for metadata_folder in os.listdir(datapath):
        if 'metadata' in metadata_folder:
            metadata_folder_path = os.path.join(datapath, metadata_folder)
            sti_folder = metadata_folder.replace('metadata', 'stimuli')
            sti_folder_path = os.path.join(datapath, sti_folder)
            if not os.path.exists(sti_folder_path):
                os.mkdir(sti_folder_path)
            for fly in os.listdir(metadata_folder_path):
                sti_fly_path = os.path.join(sti_folder_path, fly)
                if not os.path.exists(sti_fly_path):
                    os.mkdir(sti_fly_path)
                fly_path = os.path.join(metadata_folder_path, fly)
                metadata = os.listdir(fly_path)
                metadata.sort(key=lambda x: int(x.split('_')[1]))
                for repeat, repeat_sti in enumerate(sti):
                    metadf_path = os.path.join(fly_path, metadata[repeat])
                    meta_df = pd.read_csv(metadf_path)
                    for bout, bout_sti in enumerate(repeat_sti):
                        bout_sti_start = int(bout_sti[0]*fps)
                        bout_sti_end = int(bout_sti[1]*fps)
                        sti_df = meta_df.iloc[bout_sti_start: bout_sti_end+1]
                        sti_df_name = metadata[repeat].replace('meta', 'stimuli_'+str(bout))
                        sti_df_path = os.path.join(sti_fly_path, sti_df_name)
                        sti_df.to_csv(sti_df_path, index=None)
                        print(sti_df_path)









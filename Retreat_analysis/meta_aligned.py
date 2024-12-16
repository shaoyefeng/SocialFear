import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import seaborn as sns
import numpy as np
from Function_analysis import *

# 同一板果蝇
analysis_path = r"G:\analysis"
fps = 50

for datapath in cd_datapath(analysis_path):
    log_dict = all_log(datapath)
    screen_start = log_dict['screen_start']
    start0 = screen_start[0]
    interval = (np.array(screen_start)-start0).tolist()
    for metadata_folder in os.listdir(datapath):
        if 'metadata' in metadata_folder:
            metadata_folder_path = os.path.join(datapath, metadata_folder)
            aligned_folder = metadata_folder.replace('metadata', 'aligned')
            aligned_folder_path = os.path.join(datapath, aligned_folder)
            if not os.path.exists(aligned_folder_path):
                os.mkdir(aligned_folder_path)
            for fly in os.listdir(metadata_folder_path):
                aligned_fly_path = os.path.join(aligned_folder_path, fly)
                if not os.path.exists(aligned_fly_path):
                    os.mkdir(aligned_fly_path)

                metadata_fly_path = os.path.join(metadata_folder_path, fly)
                meta_df = os.listdir(metadata_fly_path)
                meta_df.sort(key=lambda x: int(x.split('_')[1]))
                for i, metadata in enumerate(meta_df):
                    metadf_path = os.path.join(metadata_fly_path, metadata)
                    df = pd.read_csv(metadf_path)
                    aligned_df_name = metadata.replace('meta', 'aligned')
                    aligned_df_path = os.path.join(aligned_fly_path, aligned_df_name)
                    df['frame'] = (df['frame'] + fps * interval[i]).astype(int)
                    df.to_csv(aligned_df_path, index=None)
                    print(aligned_df_path)







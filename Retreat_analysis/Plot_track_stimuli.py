import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import json
import os
from glob import glob

from Function_plot import *
from Function_analysis import *

plotpath = r"G:\20220614\CS_F\stimuli"
fps = 50

for stimuli_folder in os.listdir(plotpath):
    stimuli_folder_path = os.path.join(plotpath, stimuli_folder)
    if os.path.isdir(stimuli_folder_path):
        for fly in os.listdir(stimuli_folder_path):
            fly_path = os.path.join(stimuli_folder_path, fly)
            stimuli_df = os.listdir(fly_path)
            stimuli_df.sort(key=lambda x: int(x.split('_')[1]))

            fig, axes = plt.subplots(nrows=3, ncols=5, figsize=(15, 9))
            plt.tight_layout(rect=[0, 0, 1, 1])
            plt.subplots_adjust(left=0.04, right=0.99, bottom=0.04, top=0.96)
            axes = axes.flatten()
            for i, data in enumerate(stimuli_df):
                block = i // 5
                repeat = i % 5
                stimuli_df_path = os.path.join(fly_path, stimuli_df[i])
                stim_df = pd.read_csv(stimuli_df_path)
                ax = axes[i]
                ax.set_xlim(0, 20)
                ax.set_ylim(0, 20)
                ax.tick_params(labelsize=10)
                ax.set_aspect(1)
                ax.set_title('fly%s-block%s-repeat%s' % (int(fly)+1, block+1, repeat+1), fontsize=10)
                if i == 29:
                    need_colorbar = True
                else:
                    need_colorbar = False
                plot_overlap_time2(ax=ax, xs=stim_df['posx'], ys=stim_df['posy'], dirs=stim_df['body_dir'], fly=1, inter=25, cmap="viridis", need_colorbar=need_colorbar)
            # plt.show()
            fig_name = stimuli_df[0].replace('_0.csv', '.png')
            fig_path = os.path.join(plotpath, fig_name)
            print(fig_path)
            plt.savefig(fig_path, dpi=1000)
            plt.close()










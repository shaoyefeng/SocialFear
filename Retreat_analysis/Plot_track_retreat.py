import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import json
import os
from glob import glob

from Function_plot import *

datapath = r"D:\2022\Retreat\20220222_E\20220222_1_E_metadata"
annotation_path = r"D:\2022\Retreat\retreat\retreat_20220222_new.csv"

annot_df = pd.read_csv(annotation_path)
for i, data in annot_df.iterrows():
    fly, retreat, start, stop = data[['fly', 'retreat', 'start', 'stop']]
    fly_path = os.path.join(datapath, str(fly))
    df_path = glob(fly_path + '/*.csv')[0]
    df = pd.read_csv(df_path)
    retreat_df = df.iloc[start: stop+1]
    fig_path = os.path.join(os.path.dirname(annotation_path), str(i//15)+'_retreat.png')
    if i % 15 == 0:
        if not i == 0:
            plt.savefig(fig_path, dpi=1000)
        fig, axes = plt.subplots(nrows=3, ncols=5, figsize=(20, 8))
        plt.subplots_adjust(left=0.02, right=0.98, bottom=0.02, top=0.96)
        axes = axes.flatten()
    ax = axes[i % 15]
    ax.set_xlim(-8, 30)
    ax.set_ylim(-8, 30)
    ax.tick_params(labelsize=5)
    ax.set_aspect(1)
    ax.set_title('fly%s-retreat%s' % (fly, retreat))
    plot_overlap_time2(ax, xs=retreat_df['posx'], ys=retreat_df['posy'], dirs=retreat_df['body_dir'], fly=1, inter=10, cmap="viridis", need_colorbar=True)
# plt. savefig(fig_path, dpi=1000)
plt.show()



# df = pd.read_csv(r"D:\2022\20220222_1\20220222_E\20220222_1_E_metadata\3\20220222_184411_E_3_meta.csv")
# retreat_df = df.loc[4676:4750]
# fig, ax = plt.subplots(figsize=(20, 8))
# ax.set_xlim(min(retreat_df['posx'])-1, max(retreat_df['posx'])+1)
# ax.set_ylim(min(retreat_df['posy'])-1, max(retreat_df['posy'])+1)
# ax.set_aspect(1)
# # plot_overlap_time(ax, xs=retreat_df['posx'], ys=retreat_df['posy'], dirs=retreat_df['body_dir'], fly=1, inter=2)
# plot_overlap_time2(ax, xs=retreat_df['posx'], ys=retreat_df['posy'], dirs=retreat_df['body_dir'], fly=1, inter=10, cmap="viridis", need_colorbar=True)
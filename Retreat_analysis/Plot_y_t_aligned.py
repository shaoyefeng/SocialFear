import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import seaborn as sns
import numpy as np
from glob import glob

plotpath = r"G:\20220614\aligned"
fps = 50               # frame/second
blocks_n = 3                # total block number
block_duration = 615.58    # second
color = ['dodgerblue','magenta','black','green','red',]
# cache_exist = False
cache_exist = True

# fps = 60             # frame/second
# blocks_n = 16                # total block number
# block_duration = 1815.43     #second

fig, ax = plt.subplots(figsize=(20, 10))
plt.subplots_adjust(left=0.05, right=0.99)

first_static = np.array([0, 1, 2, 3, 4, 5]) * 60 * fps
static_x = []
for i in np.arange(0, blocks_n):
    static_x = np.append(static_x, first_static + i * block_duration * fps)
for j in static_x:
    rect = plt.Rectangle((j, 0), 30*fps, 20, color='lightgreen', alpha=0.2)
    ax.add_patch(rect)

first_active = np.array([0.5, 1.5, 2.5, 3.5, 4.5]) * 60 * fps
active_x = []
for i in np.arange(0, blocks_n):
    active_x = np.append(active_x, first_active + i * block_duration * fps)
for j in active_x:
    rect = plt.Rectangle((j, 0), 30*fps, 20, color='salmon', alpha=0.2)
    ax.add_patch(rect)

# first_active = np.array([0, 1, 2, 3, 4]) * 60 * fps
# active_x = []
# for i in np.arange(0, blocks_n):
#     active_x = np.append(active_x, first_active + i * block_duration * fps)
# for j in active_x:
#     rect = plt.Rectangle((j, 0), 30*fps, 20, color='salmon', alpha=0.2)
#     ax.add_patch(rect)
#
# first_static = np.array([0.5, 1.5, 2.5, 3.5, 4.5]) * 60 * fps
# static_x = []
# for i in np.arange(0, blocks_n):
#     static_x = np.append(static_x, first_static + i * block_duration * fps)
# for j in static_x:
#     rect = plt.Rectangle((j, 0), 30*fps, 20, color='lightgreen', alpha=0.2)
#     ax.add_patch(rect)

for i, genotype in enumerate(os.listdir(plotpath)):
    genotype_path = os.path.join(plotpath, genotype)
    for n in np.arange(0, blocks_n):
        if not cache_exist:
            block_df = pd.DataFrame([])
            for aligned_folder in os.listdir(genotype_path):
                aligned_folder_path = os.path.join(genotype_path, aligned_folder)
                if os.path.isdir(aligned_folder_path):
                    for fly in os.listdir(aligned_folder_path):
                        fly_path = os.path.join(aligned_folder_path, fly)
                        aligned_df = os.listdir(fly_path)
                        aligned_df.sort(key=lambda x: int(x.split('_')[1]))
                        aligned_df_path = os.path.join(fly_path, aligned_df[n])
                        df = pd.read_csv(aligned_df_path)
                        block_df = pd.concat([block_df, df], ignore_index=True)
                cache = '%s_block%s_aligned.pickle' % (aligned_folder.split('_')[0], n + 1)
                cache_path = os.path.join(genotype_path, cache)
                block_df.to_pickle(cache_path)
        else:
            cache_path = glob(genotype_path + '/*.pickle')[n]
            block_df = pd.read_pickle(cache_path)
        print(cache_path)
        if n == 0:
            label = genotype
        else:
            label = None
        # sns.lineplot(data=block_df, x='frame', y='posy', ci='sd', color=color[i], linewidth=1, err_kws={'lw': 0}, label=label)
        sns.lineplot(data=block_df, x='frame', y='posy', ci=None, color=color[i], linewidth=1, err_kws={'lw': 0}, label=label)
ax.set_xlabel('time (min)')
ax.set_ylabel('Distance from screen (mm)')

ax.set_ylim(0, 20)
ax.set_xlim(0, 31*60*fps)
xticks = np.arange(0, 40, 10)

# ax.set_ylim(0, 20)
# ax.set_xlim(0, 65*60*fps)
# xticks = np.arange(0, 70, 10.5)

# ax.set_ylim(0, 20)
# ax.set_xlim(0, 62*60*fps)
# xticks = np.arange(0, 70, 10)

# ax.set_ylim(0, 20)
# ax.set_xlim(0, 1480*60*fps)
# xticks = np.arange(0, 1494.5, 60)

#np.linspace(0, 70, 15)

ax.set_xticks(xticks*60*fps)
ax.set_xticklabels(xticks)
plt.legend()
# plt.show()
figpath = os.path.join(plotpath, 'all_aligned.png')
plt.savefig(figpath, dpi=1000)
plt.close()






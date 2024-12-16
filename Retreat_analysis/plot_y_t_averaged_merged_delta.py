import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import seaborn as sns
import numpy as np
from matplotlib import cm
from glob import glob

plotpath = r"G:\datamerged\colorful mantis\Male"
fps = 50
blocks_n = 3
color = ['black','blue','cyan','green','purple','red','silver','gray','orange']
# color = ['dodgerblue','black','magenta','green','red',]

fig, ax = plt.subplots(figsize=(5, 10))
# plt.tight_layout()
# plt.subplots_adjust(left=0.05, right=0.99, wspace=0.03)

# static_x = np.array([0, 1, 2, 3, 4, 5]) * 60 * fps
# for j in static_x:
#     rect = plt.Rectangle((j, 0), 30 * fps, 20, color='lightgreen', alpha=0.05)
# ax.add_patch(rect)
# active_x = np.array([0.5, 1.5, 2.5, 3.5, 4.5]) * 60 * fps
# for j in active_x:
#     rect = plt.Rectangle((j, 0), 30 * fps, 20, color='salmon', alpha=0.1)
#     ax.add_patch(rect)

static_x = np.array([0, 1]) * 60 * fps
for j in static_x:
    rect = plt.Rectangle((j, -10), 30 * fps, 20, color='lightgreen', alpha=0)
    ax.add_patch(rect)
active_x = np.array([0.5]) * 60 * fps
for j in active_x:
    rect = plt.Rectangle((j, -10), 30 * fps, 20, color='salmon', alpha=0.2)
    ax.add_patch(rect)

ambush = np.array([0, 12, 14, 27, 28, 42, 44, 58, 71, 73, 89, 102, 116, 117, 147, 162])/6 * fps + 0.5*60*fps
for i in ambush:
    plt.axvline(i, linewidth=0.5, color='black')

# headbowing1 = 68/6 * fps + 0.5*60*fps
# plt.axvline(headbowing1, linewidth=0.5, color='blue')
# headbowing2 = 69/6 * fps + 0.5*60*fps
# plt.axvline(headbowing2, linewidth=0.5, color='blue')
# forelimbmoving = 70/6 * fps + 0.5*60*fps
# plt.axvline(forelimbmoving, linewidth=0.5, color='red')
# forelimbmoving = 134/6 * fps + 0.5*60*fps
# plt.axvline(forelimbmoving, linewidth=0.5, color='red')

for i, genotype in enumerate(os.listdir(plotpath)):
    genotype_path = os.path.join(plotpath, genotype)
    merged_df = pd.DataFrame([])
    # os.listdir(genotype_path)
    for block in np.arange(blocks_n):
        for repeat_folder in os.listdir(genotype_path):
            repeat_folder_path = os.path.join(genotype_path, repeat_folder)
            if os.path.isdir(repeat_folder_path):
                for fly in os.listdir(repeat_folder_path):
                    fly_path = os.path.join(repeat_folder_path, fly)
                    block_folders = os.listdir(fly_path)

                    block_folders.sort(key=lambda x: int(x.split('_')[1]))
                    block_folder_path = os.path.join(fly_path, block_folders[block])
                    for repeat_df_path in glob(block_folder_path+'/*'):
                        repeat_df = pd.read_csv(repeat_df_path)
                        repeat_df['frame'] = repeat_df.index.tolist()
                        repeat_df['posy'] = repeat_df['posy'] - repeat_df['posy'][1500]
                        merged_df = pd.concat([merged_df, repeat_df], ignore_index=True)
                        print(repeat_df_path)
    # alpha = np.linspace(0, 1, 6)
    # alpha = alpha[repeat + 1],  color='deepskyblue'
# sns.lineplot(data=merged_df, x='frame', y='posy', ci='sd', linewidth=1, err_kws={'lw': 0}, ax=ax, color='b')
#     if i == 0:
#        label = genotype
#     else:
#        label = genotype
    sns.lineplot(data=merged_df, x='frame', y='posy', ci=None, linewidth=1, err_kws={'lw': 0}, ax=ax, color=color[i], label=genotype)

ax.set_xlabel('time (s)')
ax.set_ylabel('Distance from screen (mm)')
ax.set_ylim(-10, 10)
ax.set_xlim(0, 90 * fps)
xticks = np.array([0, 30, 60, 90])
ax.set_xticks(xticks * fps)
ax.set_xticklabels(xticks)

# plt.legend()
# plt.show()
figpath = os.path.join(plotpath, 'averaged_merged_delta.png')
plt.savefig(figpath, dpi=1000)
plt.close()






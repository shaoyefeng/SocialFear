import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import seaborn as sns
import numpy as np
from matplotlib import cm
from glob import glob

plotpath = r"D:\2022\datamerged\50fps\repeat"
fps = 50
blocks_n = 6
ambush = np.array([0, 12, 14, 27, 28, 42, 44, 58, 71, 73, 89, 102, 116, 117, 147, 162])/6 * fps + 0.5*60*fps
cmap = cm.get_cmap('rainbow', len(ambush))
colors = np.linspace(1, 0, len(ambush))

fig, ax = plt.subplots(figsize=(5, 10))
# plt.tight_layout()
# plt.subplots_adjust(left=0.05, right=0.99, wspace=0.03)

merged_df = pd.DataFrame([])
for geno in os.listdir(plotpath):
    geno_path = os.path.join(plotpath, geno)
    for block in np.arange(blocks_n):
        for repeat_folder in os.listdir(geno_path):
            repeat_folder_path = os.path.join(geno_path, repeat_folder)
            if os.path.isdir(repeat_folder_path):
                for fly in os.listdir(repeat_folder_path):
                    fly_path = os.path.join(repeat_folder_path, fly)
                    block_folders = os.listdir(fly_path)
                    block_folders.sort(key=lambda x: int(x.split('_')[1]))
                    block_folder_path = os.path.join(fly_path, block_folders[block])
                    for repeat_df_path in glob(block_folder_path+'/*'):
                        repeat_df = pd.read_csv(repeat_df_path)
                        repeat_df['frame'] = repeat_df.index.tolist()
                        merged_df = pd.concat([merged_df, repeat_df], ignore_index=True)
                        print(repeat_df_path)

meandf = merged_df.groupby('frame', as_index=False).agg('mean')
for i, timepoint in enumerate(ambush):
    ambush_df = meandf.iloc[int(timepoint): int(timepoint+fps*2)]
    ambush_df = ambush_df.reset_index(drop=True)
    ambush_df['frame'] = ambush_df.index
    baseline = ambush_df['posy'][0]
    ambush_df['posy'] = ambush_df['posy'] - baseline
    sns.lineplot(data=ambush_df, x='frame', y='posy', ci=None, linewidth=1, err_kws={'lw': 0}, ax=ax, color=cmap(colors[i]))

# ax.set_xlabel('time (s)')
ax.set_ylabel('Distance from screen (mm)')
# ax.set_ylim(0, 20)
# ax.set_xlim(0, 90 * fps)
# xticks = np.array([0, 30, 60, 90])
# ax.set_xticks(xticks * fps)
# ax.set_xticklabels(xticks)

# plt.legend()
# plt.show()
figpath = os.path.join(plotpath, 'ambush_reponse.png')
plt.savefig(figpath, dpi=1000)







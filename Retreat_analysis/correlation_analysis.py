import itertools

import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import cv2
import seaborn as sns
import numpy as np
from matplotlib import cm
from glob import glob
import scipy.stats as ss


stim_resp_df = pd.read_pickle(r"G:\ambushes\stim_resp.pickle")

# fig, ax = plt.subplots(figsize=(5, 10))
# plt.tight_layout()
# plt.subplots_adjust(left=0.05, right=0.99, wspace=0.03)
# stim_resp_df = stim_resp_df[1:16]
stim_dist = stim_resp_df['stim_dist']
gray_value = stim_resp_df['gray_value']
area = stim_resp_df['area']
slope = stim_resp_df['slope']
time_sequence = stim_resp_df.index.values

cor_list = ['stim_dist', 'gray_value', 'area', 'slope', 'time_sequence']

combinations = list(itertools.combinations(cor_list, 2))

for i in combinations:
    fig_name = i[0] + '-' + i[1] + '1.png'
    eval(i[0])
    plt.figure()
    corr_index, p_value = ss.pearsonr(eval(i[0]), eval(i[1]))
    plt.scatter(eval(i[0]), eval(i[1]))
    plt.xlabel(i[0])
    plt.ylabel(i[1])
    plt.text(0.8, 0.2, round(corr_index, 5), transform=plt.gca().transAxes)
    plt.text(0.8, 0.1, round(p_value, 5), transform=plt.gca().transAxes)
    plt.savefig(os.path.join(r"G:\ambushes", fig_name))
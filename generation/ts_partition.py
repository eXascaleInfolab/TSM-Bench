import pandas as pd
import numpy as np
from tqdm import tqdm
import argparse
import warnings

warnings.filterwarnings('ignore')

parser = argparse.ArgumentParser(description="A script that takes two integer values as input and calls a function with them.")
parser.add_argument("--seed", type=str, default='conductivity', help="Link to original dataset")
args = parser.parse_args()
data = pd.read_csv("data/" + args.seed + "/original.txt", header=None, sep= ';')

# data.head(3072 * 2)

# res_shift_1 = pd.DataFrame()
res_shift_50 = pd.DataFrame()
# res_shift_1800 = pd.DataFrame()

# for i in tqdm(range(1024)):
for i in tqdm(range(3072)):
    # res_shift_1[i] = np.array(list(data[2])[i:i + 3072])
    res_shift_50[i] = np.array(list(data[0])[50 * i:(50 * i) + 3072])
    # res_shift_50[i] = np.array(list(data[0])[50 * i:(50 * i) + 1536])
    # res_shift_1800[i] = np.array(list(data[2])[1800 * i:(1800 * i) + 3072])

res_shift_50 = res_shift_50.T
# res_shift_1.to_csv('res_shift_1.txt', sep=',', encoding='utf-8', header=None, index=None)
res_shift_50.to_csv("data/" + args.seed + "/segments_orig.txt", sep=',', encoding='utf-8', header=None, index=None)
# res_shift_50.to_csv('res_shift_1024_1536.txt', sep=',', encoding='utf-8', header=None, index=None)
# res_shift_1800.to_csv('res_shift_1800.txt', sep=',', encoding='utf-8', header=None, index=None)



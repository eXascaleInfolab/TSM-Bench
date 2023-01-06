import matrixprofile as mp
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
# ignore matplotlib warnings

import warnings
warnings.filterwarnings("ignore")

# Load Data
input_file = '../../datasets/AEM_data.txt'
f = open(input_file, 'r')
rows = f.readlines()
dataset = []
for row in rows:
    dataset.append(float(row))
dataset = np.array(dataset)


# dates = pd.date_range(start = '19970223', end='19970406', freq = 'h').strftime("%Y-%m-%d %H:%M:%S").to_list()
# # dates = pd.date_range(start = '19970223', end='19970406', freq = 'h').strftime("%Y-%m-%d %H:%M:%S").to_list()
# plt.figure(figsize=(20,6))
# plt.plot(dates,dataset,'g')
# plt.title('Power Demand in Italy')
# plt.ylabel('Power Supply from HV Grid (MW)')
# plt.xlabel('Datetime')
# plt.xticks(rotation=90)
# plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(24))
# plt.show()


window_size = 19
k = 1


profile = mp.compute(dataset, window_size)
profile = mp.discover.discords(profile, k = k, exclusion_zone = window_size)
mp.visualize(profile)
plt.show()


mp_adjusted = np.append(profile['mp'], np.zeros(profile['w'] - 1) + np.nan)
fig, ax = plt.subplots(1, 1, sharex=True, figsize=(16,4))
ax.plot(np.arange(len(profile['data']['ts'])), profile['data']['ts'])
ax.set_title('Window Size {}'.format(str(window_size)))
ax.set_ylabel('Data')
flag = 1
for discord in profile['discords']:
    x = np.arange(discord, discord + profile['w'])
    y = profile['data']['ts'][discord:discord + profile['w']]
    if flag:
        ax.plot(x, y, c='r',label="Discord")
        flag = 0
    else:
        ax.plot(x, y, c='r')
plt.legend()
plt.show()



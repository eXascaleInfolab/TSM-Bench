import json
import numpy as np

from tsaug import TimeWarp, Crop, Quantize, Drift, Reverse
from tsaug.visualization import plot



with open("../parameters.json", "r") as f:
    para_dict = json.load(f)
    data_paths = para_dict["input_data_path"]  # dataset path



my_augmenter = (
    # TimeWarp() * 5  # random time warping 5 times in parallel
    # + Crop(size=300)  # random crop subsequences with length 300
    # +
    Quantize(n_levels=[10, 20, 30])  # random quantize to 10-, 20-, or 30- level sets
    #Drift(max_drift=(0.1, 0.5)) @ 0.8  # with 80% probability, random drift the signal up to 10% - 50%
    #Reverse() @ 0.5  # with 50% probability, reverse the sequence
)

X = X_aug = []

for data_path in data_paths:
    X.append(np.genfromtxt('../' + data_path, delimiter=',', dtype=np.float32).transpose())
    # Y = np.load("./Y.npy")
    # plot(X)

for i in range(len(X)):
    X_aug = my_augmenter.augment(X[i]).transpose()
    print('augmented.. ', i)


for i in range(len(X)):
    # print(X_aug)
    ori = X[i]
    gen = X_aug[i]
    # plot(ori[0], gen[0]);

    
    




import numpy as np
from tqdm import tqdm
data = np.loadtxt('/Users/abdel/PycharmProjects/tsgen/results/goldwind3072/fake0.csv', delimiter=',')

for i in tqdm(range(10)):
    np.savetxt('/Users/abdel/PycharmProjects/tsgen/results/goldwind3072/fake'+str(data.shape[0]) + '.csv', data, delimiter=',')
    data = np.concatenate((data, data[:3072]))

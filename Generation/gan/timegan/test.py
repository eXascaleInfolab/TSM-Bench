## Necessary packages
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import warnings
warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt


# 1. TimeGAN model
from timegan import timegan
# 2. Data loading
from data_loading import real_data_loading, sine_data_generation
# 3. Metrics
from metrics.metrics import discriminative_score_metrics
from metrics.metrics import visualization

## Data loading
data_name = 'google'
seq_len = 24

if data_name in ['stock', 'energy', 'google']:
    ori_data = real_data_loading(data_name, seq_len)
elif data_name == 'sine':
    # Set number of samples and its dimensions
    no, dim = 10000, 5
    ori_data = sine_data_generation(no, seq_len, dim)

print(data_name + ' dataset is ready.')


## Newtork parameters
parameters = dict()

parameters['module'] = 'gru'
parameters['hidden_dim'] = 24
parameters['num_layer'] = 3
parameters['iterations'] = 200
parameters['batch_size'] = 128


# Run TimeGAN
generated_data = timegan(ori_data, parameters)
print('Finish Synthetic Data Generation')


metric_iteration = 5

discriminative_score = list()
for _ in range(metric_iteration):
  temp_disc = discriminative_score_metrics(ori_data, generated_data)
  discriminative_score.append(temp_disc)

print('Discriminative score: ' + str(np.round(np.mean(discriminative_score), 4)))



visualization(ori_data, generated_data, 'pca')
visualization(ori_data, generated_data, 'tsne')


for i in range(len(generated_data[0])):
    plt.plot(generated_data[:,i])
    plt.plot(ori_data[i])

plt.show()
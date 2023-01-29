import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from os import path
sys.path.append(path.join(path.dirname(__file__), '..'))
# from baselines.agots.agots.multivariate_generators.multivariate_data_generator import MultivariateDataGenerator
from baselines.agots.agots.multivariate_generators.multivariate_data_generator import MultivariateDataGenerator


import baselines.agots.agots.multivariate_generators.multivariate_data_generator

STREAM_LENGTH = 2000
N = 1
K = 1

dg = MultivariateDataGenerator(STREAM_LENGTH, N, K)
df = dg.generate_baseline(initial_value_min=-4, initial_value_max=4)


for col in df.columns:
    plt.plot(df[col], label=col)
plt.legend()
plt.show()

df.corr()
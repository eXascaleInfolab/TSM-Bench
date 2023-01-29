import metrics as met
import pandas as pd
import numpy as np
import mat4py
import matplotlib.pyplot as plt

# original = np.genfromtxt('../datasets/ec21ts.csv', delimiter=',', dtype=np.float32)
# original = original[1:, 1:]
# normalize data
# original = (original - original.min()) / (original.max() - original.min())
# print (original)
# # print('data normalized')

dataset = "ec21ts"
# data_path = "../datasets/" + dataset + ".mat"
data_path = "../datasets/" + "ec21ts.csv"


# df =  mat4py.loadmat(data_path)
df = pd.read_csv(data_path, header=1)
# df_uni = df['X']
# df_uni = pd.DataFrame.from_records(df['X'])
df_uni = df.iloc[:,1]
# df_uni.plot()
# plt.show()
# df = pd.read_csv("TravelTime1ts.csv")
# df_uni = df.iloc[:, 1]
# df_uni = df.iloc[:, 1]
anos, ano_score = met.anomaly_detection(df_uni)
print("Anomaly score : %f" % ano_score)
met.anomaly_plot(df_uni, anos, dataset)

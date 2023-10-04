#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import multiprocessing
import hashing.lsh_main as lsh
# import graph.graph_main as graph
import time
from pathlib import Path
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import graph.random_walk_ori as random_walk
import pandas as pd
import lshashpy3 as lshash
import math 

def sigmoid(x):
    return 1 / (1 + math.exp(-x))


# In[3]:


data = pd.read_csv('data/pH_accuracy.csv')
data = data['pH'].tolist()
# data = data[:5000]
len(data)

#define moving average function
def moving_avg(x, n):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[n:] - cumsum[:-n]) / float(n)

#calculate moving average using previous 3 time periods

data = moving_avg(data, 200).tolist()


# In[4]:


plt.plot(data)
plt.show()
# plt.plot(generated)
# plt.show()


# In[26]:


print('Preparing segments...')
window = 1000
segments = []
for i in range(3):
    segments += [data[i:i + window] + np.random.normal(0,.008, window) for i in range(0, len(data) - window, int(0.1 * window))]


# In[8]:


df_segments = pd.DataFrame(segments)
df_segments = df_segments.T

df_segments.iloc[: , :50].plot(subplots=True, layout=(10,6), figsize=(10, 10), legend = True, color = 'b')
plt.show()


# ## Filter GAN generated data

# In[9]:


from scipy.signal import lfilter
print('Filtering GAN generated data...')

# df_segments = df_segments.T

n = 10  # the larger n is, the smoother curve will be
b = [1.0 / n] * n
a = 1

for col in tqdm(df_segments):
#     plt.plot(df_segments[col].tolist())
    yy = lfilter(b,a,df_segments[col].tolist())
    yy[:n] = yy[n:n+1]
    df_segments[col] = yy.tolist()
#     plt.plot(df_segments[col].tolist())
#     plt.show()
    
    
# df_segments = pd.DataFrame(segments)
# df_segments = df_segments.T

df_segments.iloc[: , :50].plot(subplots=True, layout=(10,6), figsize=(10, 10), legend = True, color = 'b')
plt.show()


# # LSH

# In[10]:


print('Launching LSH...')
lsh = lshash.LSHash(8, len(segments[0]), num_hashtables=8)

for i in segments:
    lsh.index(i)


# In[11]:


to_query = [data[i:i + window] for i in range(0, len(data) - window, window)]

# plt.plot(to_query[0])
# plt.show()

# plt.plot(random.choice( lsh.query(to_query[0], distance_func="euclidean", num_results=10))[0][0])
# plt.show()

# nn = lsh.query(to_query[0], distance_func="euclidean", num_results=10)
# for ((vec,extra_data),distance) in nn:
#     print( distance)
#     plt.plot(vec)
#     plt.show()
#     # len(segments)


# In[27]:


# lsh_res = []
# for i in range(3):
#     results = [lsh.query(to_query[i])[0][0][0] for i in range(len(to_query))]
#     print(len(results))
#     res_lsh = []
#     for l in results: 
#         res_lsh += l
#     lsh_res.append(res_lsh)

print('Querying LSH...')
lsh_res = []
n_top = 10
k = int(window * .03)
for i in tqdm(range(3)):
    temp = list(random.choice( lsh.query(to_query[0], distance_func="euclidean", num_results=n_top))[0][0])
    for i in range(1, len(to_query)): 
        s = list(random.choice( lsh.query(to_query[i], distance_func="euclidean", num_results=n_top))[0][0])
        temp_t = temp[-k:]
        s_h = s[:k]
        overlap = []
        for i in range(-k//2, k//2):
            overlap.append((1 - sigmoid(i))*temp_t[i + k//2] + sigmoid(i)*s_h[i + k//2])
#         for i in range(-1*k , 0):
#             temp[i]= (1 - sigmoid(i))*temp_t[i] + sigmoid(i)*s_h[i]
#         for i in range(0, k):
#             s[i]= (1 - sigmoid(i))*temp_t[i] + sigmoid(i)*s_h[i]
        temp[-k:] = overlap
        temp.extend(s[k:])
    lsh_res.append(temp)


# # Graph

# In[29]:


#Calculates the distance between two series. Given series A, B returns the Euclidean distance between A and B
def distance(a, b):
    return np.sqrt(np.sum((a - b)**2))
    
#The probability is converted according to the sorted distances, which adds up to 1
def distopro(a):
    a=len(a)
    if(a==3):
        b=[0.2,0.3,0.5]
    elif(a==4):
        b=[0.1,0.2,0.3,0.4]
    else:
        b=[0.04,0.12,0.2,0.28,0.36]
    return np.array(b)
        

#Input is the original data matrix, return is the relationship matrix relation_matrix, and probability matrix probability_matrix
#Data is the matrix of series, the first dimension is the number of series, and the second dimension is each series
#Window_size is the size of the window to calculate the distance, and k is the number of the nearest neighbors selected. Currently, 3,4,5 are supported
def transform(data, window_size, k):
    numOfSeq=data.shape[0]
    distance_matrix=np.ones([numOfSeq,numOfSeq],dtype = float)
    for i in range(numOfSeq):
        for j in range(numOfSeq):
            distance_matrix[i][j]=distance(data[i,data.shape[1]-window_size:],data[j,0:window_size])
    relation_matrix=np.ones([numOfSeq,k],dtype = int)
    subdistance_matrix=np.ones([numOfSeq,k],dtype = float)
    probability_matrix=np.ones([numOfSeq,k],dtype = float)
    for i in range(numOfSeq):
        relation_matrix[i]=distance_matrix[i].argsort()[::-1][data.shape[0]-k:]
        #print(relation_matrix[i])
#     print(relation_matrix[i])
    for i in range(numOfSeq):
        for j in range(k):
            subdistance_matrix[i][j]=distance_matrix[i][relation_matrix[i][j]]
    
    for i in range(numOfSeq):
        probability_matrix[i]=distopro(subdistance_matrix[i])
    
    
    return distance_matrix, subdistance_matrix ,relation_matrix, probability_matrix
            
      
#print(transform(np.array([[0,1,1,1],[1,0,1,1],[1,1,0,1],[1,1,1,0]]), 2, 3))


#Given the ID of the current series, the ID of the next series is generated randomly according to probability
def next_step(relation_array, probability_array):
    value=random.random()
#     print(value)
    threshold=[0]
    sum_value=0
    for i in range(len(probability_array)):
        sum_value=sum_value+probability_array[i]
        threshold.append(sum_value)
    for i in range(len(threshold)-1):
        if(value>threshold[i] and value<=threshold[i+1]):
            return relation_array[i]

#Given a relation matrix and a probability matrix, returns a series of length        
def random_walk(relation_matrix, probability_matrix, length):
    seq=[0]
    temp_id=0
    for i in range(length-1):
        temp_id=next_step(relation_matrix[temp_id],probability_matrix[temp_id])
        seq.append(temp_id)
        #print(temp_id)
    return np.array(seq)


# In[30]:


seq=[0]
print('Building Graph...')
a,b,c,d=transform(np.array(segments), 100, 5)


# In[31]:


print('Generating using Graph...')
graph_res = []
for i in range(3):
    path = random_walk( c, d, int(len(data)/window))
    print(path)
    temp=[]
    for s in path:
#         print(path[i], i)
        temp+=list(segments[s])
    graph_res.append(temp)
    print(len(graph_res))
    


# In[32]:


print(graph_res[0][-3:-1])
print(graph_res[1][-3:-1])
print(graph_res[2][-3:-1])


# In[19]:


# res_lsh = pd.read_csv('example_data.csv')
# res_lsh = res_lsh['LSH'].tolist()

# res_graph = pd.read_csv('example_data.csv')
# res_graph = res_graph['Graph'].tolist()


# In[45]:


xi = list(range(10000))
# plot the index for the x-values 

plt.figure(figsize=(60, 40))
plt.subplot(7, 1, 1)

# plt.figure(figsize=(60, 8))
plt.plot(data,color='blue',linewidth=4.0, label='Original')
plt.xlim(0,len(data))
plt.ylim(8.1,8.7)
plt.legend(loc="upper left", prop={'size': 36})

# plt.show()

plt.subplot(7, 1, 2)

# plt.figure(figsize=(60, 8))
plt.plot(lsh_res[0],color='green',linewidth=4.0, label='LSH')
plt.xlim(0,len(lsh_res[0]))
plt.ylim(8.1,8.7)
plt.legend(loc="upper left", prop={'size': 36})

plt.subplot(7, 1, 3)

# plt.figure(figsize=(60, 8))
plt.plot(lsh_res[1],color='green',linewidth=4.0, label='LSH')
plt.xlim(0,len(lsh_res[1]))
plt.ylim(8.1,8.7)
# plt.legend(loc="upper left", prop={'size': 36})
plt.legend(loc="upper left", prop={'size': 36})

plt.subplot(7, 1, 4)

# plt.figure(figsize=(60, 8))
plt.plot(lsh_res[2],color='green',linewidth=4.0, label='LSH')
plt.xlim(0,len(lsh_res[1]))
plt.ylim(8.1,8.7)
# plt.legend(loc="upper left", prop={'size': 36})
plt.legend(loc="upper left", prop={'size': 36})


plt.subplot(7, 1, 5)

# plt.figure(figsize=(60, 8))
plt.plot(graph_res[0],color='red',linewidth=4.0, label='Graph')
plt.xlim(0,len(graph_res[0]))
plt.ylim(8.1,8.7)
plt.legend(loc="upper left", prop={'size': 36})

plt.subplot(7, 1, 6)

# plt.figure(figsize=(60, 8))
plt.plot(graph_res[1],color='red',linewidth=4.0, label='Graph')
plt.xlim(0,len(graph_res[1]))
plt.ylim(8.1,8.7)
plt.legend(loc="upper left", prop={'size': 36})


plt.subplot(7, 1, 7)

# plt.figure(figsize=(60, 8))
plt.plot(graph_res[2],color='red',linewidth=4.0, label='Graph')
plt.xlim(0,len(graph_res[2]))
plt.ylim(8.1,8.7)
plt.legend(loc="upper left", prop={'size': 36})

# plt.show()
plt.savefig('results/plot_lsh_graph.pdf',dpi=1600,
            bbox_inches = 'tight')



# # Metrics

# In[38]:

plt.figure()
plt.hist(data, bins=50, alpha=0.5, label ='real')
plt.hist(lsh_res[0], bins=50, alpha=0.5, label ='lsh')
plt.hist(graph_res[0], bins=50, alpha=0.5, label ='graph')
plt.legend()
# plt.show()
plt.savefig('results/hist_lsh_graph.pdf',dpi=1600,
            bbox_inches = 'tight')


# In[39]:


type(lsh_res[0])


# In[42]:


import csv

with open('results/lsh.csv', 'w') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(lsh_res[0])

with open('results/graph.csv', 'w') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(graph_res[0])


# In[ ]:





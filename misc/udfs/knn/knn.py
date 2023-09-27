try:
	from queue import PriorityQueue
except:
	pass

try:
	from queue import PriorityQueue
except:
	pass

import numpy as np

def distance(a, b):
	return np.linalg.norm(a - b)

def knn_single(label_matrix, labels, datapoint, k):
	n_label = label_matrix.shape[0]
	a = PriorityQueue()
	for i in range(n_label):
		a.put( (-distance(label_matrix[i], datapoint), labels[i]) )
		while a.qsize() > k:
			a.get()
	l_size = a.qsize()
	l = [0] * l_size
	for i in range(l_size):
		l[i] = a.get()[1]
	return max(set(l), key = l.count)


def knn(label_matrix, labels, unlabel_matrix, k):
	n_unlabel = unlabel_matrix.shape[0]
	result = [0] * n_unlabel
	for i in range(n_unlabel):
		result[i] = knn_single(label_matrix, labels, unlabel_matrix[i], k)
	return result

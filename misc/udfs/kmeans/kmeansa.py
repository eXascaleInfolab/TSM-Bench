import random
import numpy as np
from datetime import datetime

def distance(datapoint, cluster):
	return np.sum( np.square( datapoint - cluster ) )

def kmeans(datapoints, clusters_count, iterations):
	lines = datapoints.shape[0]
	columns = datapoints.shape[1]

	clusters = np.asarray( random.sample(list(datapoints), clusters_count) )
	for t in range(iterations):	
		sum_clusters = np.zeros([clusters_count, columns])
		count_clusters = np.zeros([clusters_count])
		for i in range(lines):
			# Calculate the closest cluster
			closest_cluster = 0
			closest_distance = distance(datapoints[i], clusters[0])
			for j in range(1, clusters_count):
				cluster_distance = distance(datapoints[i], clusters[j])
				if cluster_distance < closest_distance:
					closest_distance = cluster_distance
					closest_cluster = j
			
			sum_clusters[closest_cluster] = sum_clusters[closest_cluster] + datapoints[i]
			count_clusters[closest_cluster] = count_clusters[closest_cluster] + 1
		
		for i in range(clusters_count):
			if count_clusters[i] == 0:
				clusters[i] = random.sample(list(datapoints), 1)[0]
			else:
				clusters[i] = sum_clusters[i] / count_clusters[i]

	return clusters

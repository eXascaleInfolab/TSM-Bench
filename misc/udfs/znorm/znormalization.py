import math
import numpy as np

def zscore(datapoints):
	rows = datapoints.shape[0]
	columns = datapoints.shape[1]
	result = np.zeros((rows, columns))
	for j in range(columns):
		avg = 0.0
		for i in range(rows):
			avg = avg + datapoints[i][j]
		avg = avg / rows
		stdev = 0.0
		for i in range(rows): 
			stdev = stdev + ((datapoints[i][j] - avg) ** 2)
		stdev = math.sqrt(stdev / rows)
		if (stdev <= 0.001) and (stdev >= -0.001):
			stdev = 1.0
		for i in range(rows):	
			result[i][j] = (datapoints[i][j] - avg) / stdev
	return result

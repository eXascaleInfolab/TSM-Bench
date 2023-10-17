import saxpy
from saxpy.hotsax import find_discords_hotsax
from tqdm import tqdm

def hotsax(matrix):
	result = []
	index_ts = 0
	for ts in tqdm(matrix.T):
		discords = find_discords_hotsax(ts)
		for anomaly in discords:
			result.append([index_ts, anomaly[0], anomaly[1]])
		index_ts = index_ts + 1
	return result

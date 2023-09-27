import numpy as np
import pickle

class CalcUtil:
	@staticmethod
	def avg(timeSeries, start = 0, end = None):
		if end == None:
			end = len(timeSeries)
		return np.average( np.array( timeSeries[start:end] ) )

	@staticmethod
	def deviation(timeSeries, start = 0, end = None):
		if end == None:
			end = len(timeSeries)
		return np.std( np.array( timeSeries[start:end] ) )

	@staticmethod
	def split(points, minLength):
		newPoints = []
		c = 0
		for i in range(len(points)):
			l = points[i]
			if i > 0:
				l = points[i] - points[i - 1]
			if l >= minLength * 2:
				start = 0
				if i > 0:
					start = points[i - 1]
				newPoints.append( start + int(l / 2) )
			newPoints.append( points[i] )
		return newPoints

	@staticmethod
	def avgBySegments(timeSeries, segments):
		ret = []
		start = 0
		for i in range(len(segments)):
			end = segments[i]
			ret.append( CalcUtil.avg( timeSeries, start, end) )
			start = end
		return ret

	@staticmethod
	def devBySegments(timeSeries, segments):
		ret = []
		start = 0
		for i in range(len(segments)):
			end = segments[i]
			ret.append( CalcUtil.deviation(timeSeries, start, end) )
			start = end
		return ret


class TimeSeriesFileUtil:
	@staticmethod
	def readSeriesFromBinaryFileAtOnce(fileName, nodeSize):
		with open(fileName, "rb") as infile:
			result = []
			for i in range(nodeSize):
				result.append( pickle.load(infile) )
			return result

cache = {}
class DistUtil:
	@staticmethod
	def resetCache():
		cache = {}

	@staticmethod
	def minDistBinary(fileName, nodeSize, queryTs):
		if fileName in cache:
			tss = cache[fileName]
		else:
			tss = TimeSeriesFileUtil.readSeriesFromBinaryFileAtOnce(fileName, nodeSize)
			cache[fileName] = tss
		return DistUtil.minDist(tss, queryTs)

	@staticmethod
	def minDist(dataTimeSeries, queryTs):
		shortestDist = float("inf")
		for data in dataTimeSeries:
			shortestDist = min(shortestDist, DistUtil.euclideanDist(queryTs, data))
		return shortestDist

	@staticmethod
	def euclideanDist(dataTs, queryTs):
		return np.linalg.norm(dataTs - queryTs)


import numpy as np

class TimePoint:
	def __init__(self, timestamp, value):
		self.setTimestamp(timestamp)
		self.setValue(value)
		self.setModified(value)
	
	def getTimestamp(self):
		return self.timestamp

	def setTimestamp(self, timestamp):
		self.timestamp = timestamp

	def getValue(self):
		return self.value

	def setValue(self, value):
		self.value = value

	def getModified(self):
		return self.modified

	def isModified(self):
		return (self.value == self.modified)

	def setModified(self, modified):
		self.modified = modified



class TimeSeries:
	def __init__(self, timeseries=None):
		if timeseries == None:
			self.setTimeseries([])
		else:
			self.setTimeseries(timeseries)

	def getTimeseries(self):
		return self.timeseries

	def setTimeseries(self, timeseries):
		self.timeseries = timeseries

	def __len__(self):
		return len(self.timeseries)

	def addTimePoint(self, tp):
		self.timeseries.append(tp)



class Screen:
	def __init__(self, timeseries, smax, smin, t):
		self.setTimeSeries(timeseries)
		self.setT(t)
		self.setSMAX(smax)
		self.setSMIN(smin)

	def setTimeSeries(self, timeseries):
		self.timeseries = timeseries

	def setT(self, t):
		self.T = t

	def setSMAX(self, smax):
		self.SMAX = smax

	def setSMIN(self, smin):
		self.SMIN = smin

	def mainScreen(self):
		totalList = self.timeseries.getTimeseries()
		size = len(totalList)
		
		preEnd = -1
		curEnd = 0
		wStartTime = 0
		wEndTime = 0
		wGoalTime = 0
		curTime = 0
		prePoint = None
		tp = None
		tempSeries = TimeSeries()
		tempList = []
		readIndex = 1
		tp = totalList[0]
		tempSeries.addTimePoint(tp)
		wEndTime = wStartTime
		wGoalTime = wStartTime + self.T

		while readIndex < size:
			tp = totalList[readIndex]
			curTime = tp.getTimestamp()
			from datetime import datetime 
			if datetime.timestamp(curTime) > wGoalTime:
				while True:
					tempList = tempSeries.getTimeseries()
					if len(tempList) == 0:
						tempSeries.addTimePoint(tp)
						wGoalTime = curTime + self.T
						wEndTime = curTime
						break

					self.kp = tempList[0]
					wStartTime = self.kp.getTimestamp()
					wGoalTime = datetime.timestamp(wStartTime) + self.T

					if datetime.timestamp(curTime) <= wGoalTime:
						tempSeries.addTimePoint(tp)
						wEndTime = curTime
						break

					curEnd = wEndTime

					if preEnd == -1:
						prePoint = self.kp

					self.local(tempSeries, prePoint)

					prePoint = self.kp
					preEnd = curEnd
					del tempSeries.getTimeseries()[0]
			else:
				if curTime > wEndTime:
					tempSeries.addTimePoint(tp)
					wEndTime = curTime

			readIndex = readIndex + 1

		resultSeries = TimeSeries()
		timestamp = 0
		modify = 0

		for timePoint in self.timeseries.getTimeseries():
			timestamp = timePoint.getTimestamp()
			modify = timePoint.getModified()
			tp = TimePoint(timestamp, modify)
			resultSeries.addTimePoint(tp)

		return resultSeries

	def local(self, timeSeries, prePoint):
		tempList = timeSeries.getTimeseries()
		preTime = prePoint.getTimestamp()
		preVal = prePoint.getModified()
		kpTime = self.kp.getTimestamp()
		from datetime import datetime 

		lowerBound = preVal + self.SMIN * (datetime.timestamp(kpTime) - datetime.timestamp(preTime))
		upperBound = preVal + self.SMAX * (datetime.timestamp(kpTime) - datetime.timestamp(preTime))

		xkList = []
		l = len(tempList)

		xkList.append( self.kp.getModified() )

		for i in range(1, l):
			tp = tempList[i]
			val = tp.getModified()
			dTime = datetime.timestamp(kpTime) - datetime.timestamp(tp.getTimestamp())
			xkList.append(val + self.SMIN * dTime)
			xkList.append(val + self.SMAX * dTime)
			
		xkList.sort()

		xMid = xkList[l - 1]
		modify = xMid
		if upperBound < xMid:
			modify = upperBound
		else:
			if lowerBound > xMid:
				modify = lowerBound

		self.kp.setModified(modify)


def screen(matrix, timestamps, sMax, sMin, windowSize):
	rows = matrix.shape[0]
	columns = matrix.shape[1]

	result = np.zeros((rows, columns))
	for i in range(columns):
		alist = [ TimePoint(timestamps[j], matrix[j][i]) for j in range(rows) ]
		screen = Screen(TimeSeries(alist), sMax, sMin, windowSize)
		ts = screen.mainScreen().getTimeseries()
		for j in range(rows):
			result[j][i] = ts[j].getModified()
	return result

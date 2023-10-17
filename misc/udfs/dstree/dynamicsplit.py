import json
import pickle
import os
import shutil
import re
import sys
try:
	import queue
except ImportError:
	import Queue as queue
import math
from datetime import datetime
try:
	from dstree.util import *
except ImportError:
	pass

def current_time_epoch():
	return (datetime.now() - datetime(1970, 1, 1)).total_seconds()

class Sketch(object):
	def __init__(self):
		self.indicators = None

class INodeSegmentSplitPolicy:
	def split(self, nodeSegmentSketch):
		pass
	def getIndicatorSplitIdx(self):
		pass
	def getIndicatorSplitValue(self):
		pass

class INodeSegmentSketchUpdater:
	def updateSketch(self, nodeSegmentSketch, series, fromIdx, toIdx):
		pass

class IRange:
	def calc(self, sketch, l):
		pass

class ISeriesSegmentSketcher:
	def doSketch(self, series, fromIdx, toIdx):
		pass


class PqItem:
	def __init__(self):
		self.node = None
		self.dist = float(0)

	def __lt__(self, other):
		return self.dist < other.dist

	def __gt__(self, other):
		return self.dist > other.dist

	def __eq__(self, other):
		return self.dist == other.dist

	def __le__(self, other):
		return self.dist <= other.dist

	def __ge__(self, other):
		return self.dist >= other.dist

	def __ne__(self, other):
		return self.dist != other.dist


class SplitPolicy:
	def __init__(self):
		self.splitFrom = 0
		self.splitTo = 0
		self.nodeSegmentSplitPolicy = None
		self.indicatorIdx = 0
		self.indicatorSplitValue = float(0)
		self.seriesSegmentSketcher = None

	def getNodeSegmentSplitPolicy(self):
		return self.nodeSegmentSplitPolicy
	
	def setNodeSegmentSplitPolicy(self, nodeSegmentSplitPolicy):
		self.nodeSegmentSplitPolicy = nodeSegmentSplitPolicy
	
	def getSeriesSegmentSketcher(self):
		return self.seriesSegmentSketcher

	def setSeriesSegmentSketcher(self, seriesSegmentSketcher):
		self.seriesSegmentSketcher = seriesSegmentSketcher

	def routeToLeft(self, series):
		seriesSegmentSketch = self.seriesSegmentSketcher.doSketch(series, self.splitFrom, self.splitTo)
		return seriesSegmentSketch.indicators[self.indicatorIdx] < self.indicatorSplitValue

class SeriesSegmentSketch(Sketch):
	def __init__(self):
		Sketch.__init__(self)

class NodeSegmentSketch(Sketch):
	def __init__(self):
		Sketch.__init__(self)

class FileBuffer:
	def __init__(self, fileBufferManager):
		self.fileName = None
		self.lastTouched = 0
		self.bufferedList = []
		self.inDisk = False
		self.diskCount = 0
		self.fileBufferManager = fileBufferManager

	def getBufferCount(self):
		return len(self.bufferedList)

	def getAllTimeSeries(self):
		if self.diskCount > 0:
			ret = []
			self.fileBufferManager.ioRead = self.fileBufferManager.ioRead + 1
			with open(self.fileName, "rb") as f:
				for i in range(self.diskCount):
					ret.append( pickle.load(f) )
			ret = ret + self.bufferedList
			return ret
		return self.bufferedList

	def getTotalCount(self):
		return self.diskCount + self.getBufferCount()

	def append(self, timeSeries):
		self.bufferedList.append(timeSeries)
		self.fileBufferManager.addCount(len(timeSeries))

	def flushBufferToDisk(self):
		if self.getBufferCount() > 0:
			self.appendToFile()

	def appendToFile(self):
		with open(self.fileName, "ab") as f:
			for i in range(len(self.bufferedList)):
				pickle.dump(self.bufferedList[i], f)
		self.fileBufferManager.ioWrite = self.fileBufferManager.ioWrite + 1
		self.fileBufferManager.removeCount( len(self.bufferedList) * len(self.bufferedList[0]) )
		self.diskCount = self.diskCount + len(self.bufferedList)
		self.bufferedList = []
		self.inDisk = True

	def deleteFile(self):
		if self.inDisk:
			os.remove(self.fileName)
			self.fileBuffereManager.ioDelete = self.fileBufferedManager.ioDelete + 1
			self.diskCount = 0
			self.inDisk = False
		if self.getBufferCount() > 0:
			self.fileBufferManager.removeCount( len(self.bufferedList) * len(self.bufferedList[0] ))
			self.bufferedList = []

	def priority(self):
		return self.getBufferedCount()

	def __lt__(self, other):
		return self.priority() > other.priority()
	
	def __gt__(self, other):
		return self.priority() < other.priority()

	def __eq__(self, other):
		return self.priority() == other.priority()

	def __le__(self, other):
		return self.priority() >= other.priority()

	def __ge__(self, other):
		return self.priority() <= other.priority()

	def __ne__(self, other):
		return self.priority() != other.priority()

class FileBufferManager:
	fileBufferManager = None

	def __init__(self):
		self.maxBufferedSize = 1000 * 1000 * 100
		self.bufferedMemorySize = 1024.0
		self.startTime = current_time_epoch()
		self.threshold = 0
		self.tsLength = 0
		self.ioWrite = 0
		self.ioRead = 0
		self.ioDetele = 0
		self.currentCount = 0
		self.batchRemoveSize = self.maxBufferedSize / 100
		self.fileMap = {}

	def getStartTime(self):
		return self.startTime

	def setStartTime(self, t):
		self.startTime = t

	def addCount(self, c):
		self.currentCount = self.currentCount + c

	def removeCount(self, c):
		self.currentCount = self.currentCount - c

	def getThreshold(self):
		return self.threshold

	def setThreshold(self, t):
		self.threshold = t

	def getBufferedMemorySize(self):
		return self.bufferedMemorySize

	def createFileBuffer(self):
		return FileBuffer(self)

	def setBufferedMemorySize(self, bufferedMemorySize):
		self.bufferedMemorySize = bufferedMemorySize
		self.maxBufferedSize = int( bufferedMemorySize * 1024 * 1024 / 8 )
		self.batchRemoveSize = self.maxBufferedSize / 2

	def getFileBuffer(self, fileName):
		if not(fileName in self.fileMap):
			if self.currentCount >= self.maxBufferedSize:
				toSize = self.maxBufferedSize - self.batchRemoveSize
				l = list( self.fileMap.values() )
				l.sort()
				idx = 0
				bufferCount = l[idx].getBufferCount()
				while self.currentCount > toSize:
					self.flushBufferToDisk(l[idx].fileName)
					idx = idx + 1
			fileBuffer = self.createFileBuffer()
			fileBuffer.fileName = fileName
			self.fileMap[fileName] = fileBuffer
		fileBuffer = self.fileMap[fileName]
		fileBuffer.lastTouched = current_time_epoch()
		return fileBuffer

	def saveAllToDisk(self):
		for v in self.fileMap.values():
			v.flushBufferToDisk()

	@staticmethod
	def getInstance():
		if FileBufferManager.fileBufferManager == None:
			FileBufferManager.fileBufferManager = FileBufferManager()
		return FileBufferManager.fileBufferManager

	def flushBufferToDisk(self, fileName):
		self.fileMap.get(fileName).flushBufferToDisk()

	def deleteFile(self, fileName):
		self.fileMap[fileName].deleteFile()
		del self.fileMap[fileName]


class Node:
	def __init__(self, indexPath = None, threshold = None, parent = None):
		self.nodeSegmentSplitPolicies = None
		self.range = None
		self.nodeSegmentSketchUpdater = None
		self.seriesSegmentSketcher = None
		self.parent = None
		self.level = 0
		self.isLeft = False
		self.nodePoints = None
		self.nodeSegmentSketches = []
		self.hsNodePoints = None
		self.hsNodeSegmentSketches = None
		self.threshold = 0
		self.size = 0
		self.left = None
		self.right = None
		self.splitPolicy = None
		if parent != None:
			self.__init__(indexPath = parent.indexPath, threshold = parent.threshold)
			self.nodeSegmentSplitPolicies = parent.nodeSegmentSplitPolicies
			self.range = parent.range
			self.nodeSegmentSketchUpdater = parent.nodeSegmentSketchUpdater
			self.seriesSegmentSketcher = parent.seriesSegmentSketcher
			self.parent = parent
			self.level = parent.level + 1
		else:
			self.indexPath = indexPath
			self.threshold = threshold

	def setNodeSegmentSplitPolicies(self, nodeSegmentSplitPolicies):
		self.nodeSegmentSplitPolicies = nodeSegmentSplitPolicies

	def setRange(self, newRange):
		self.range = newRange

	def isRoot(self):
		return self.parent == None

	def getSegmentSize(self):
		return len(self.nodePoints)

	@staticmethod
	def getSegmentStart(points, idx):
		if idx == 0:
			return 0
		else:
			return points[idx - 1]

	@staticmethod
	def getSegmentEnd(points, idx):
		return points[idx]

	def getSegmentLength(self, i):
		if i == 0:
			return self.nodePoints[0]
		else:
			return self.nodePoints[i] - self.nodePoints[i - 1]

	@staticmethod
	def getSegmentLength(points, i):
		if i == 0:
			return points[0]
		else:
			return points[i] - points[i - 1]

	def getSize(self):
		return self.size

	def isTerminal(self):
		return self.left == None and self.right == None

	def append(self, timeSeries):
		fileBufferManager = FileBufferManager.getInstance()
		fileBuffer = fileBufferManager.getFileBuffer(self.getFileName())
		fileBuffer.append(timeSeries)

	def insert(self, timeSeries):
		self.updateStatistics(timeSeries)
		if (self.isTerminal()):
			self.append(timeSeries)
			if self.threshold == self.size:
				fileName = self.getFileName()
				self.splitPolicy = SplitPolicy()
				self.splitPolicy.setSeriesSegmentSketcher(self.getSeriesSegmentSketcher())
				maxDiffValue = float('-inf')
				avg_children_range_value = 0
				horizontalSplitPoint = -1
				for i in range(len(self.nodePoints)):
					nodeRangeValue = self.range.calc(  self.nodeSegmentSketches[i], Node.getSegmentLength( self.nodePoints, i) )
					for j in range(len(self.nodeSegmentSplitPolicies)):
						nodeSegmentSplitPolicy = self.nodeSegmentSplitPolicies[j]
						childNodeSegmentSketches = nodeSegmentSplitPolicy.split( self.nodeSegmentSketches[i])
						rangeValues = [float(0)] * len(childNodeSegmentSketches)
						for k in range(len(childNodeSegmentSketches)):
							childNodeSegmentSketch = childNodeSegmentSketches[k]
							rangeValues[k] = self.range.calc( childNodeSegmentSketch, Node.getSegmentLength( self.nodePoints, i))
						avg_children_range_value = CalcUtil.avg( rangeValues )
						diffValue = nodeRangeValue - avg_children_range_value
						if diffValue > maxDiffValue:
							maxDiffValue = diffValue
							self.splitPolicy.splitFrom = Node.getSegmentStart(self.nodePoints, i)
							self.splitPolicy.splitTo = Node.getSegmentEnd(self.nodePoints, i)
							self.splitPolicy.indicatorIdx = nodeSegmentSplitPolicy.getIndicatorSplitIdx()
							self.splitPolicy.indicatorSplitValue = nodeSegmentSplitPolicy.getIndicatorSplitValue()
							self.splitPolicy.setNodeSegmentSplitPolicy( nodeSegmentSplitPolicy )
				maxDiffValue = maxDiffValue * 2
				for i in range(len(self.hsNodePoints)):
					nodeRangeValue = self.range.calc( self.hsNodeSegmentSketches[i], Node.getSegmentLength(self.hsNodePoints, i) )
					for j in range(len(self.nodeSegmentSplitPolicies)):
						hsNodeSegmentSplitPolicy = self.nodeSegmentSplitPolicies[j]
						childNodeSegmentSketches = hsNodeSegmentSplitPolicy.split( self.hsNodeSegmentSketches[i] )
						rangeValues = [float(0)] * len(childNodeSegmentSketches)
						for k in range(len(childNodeSegmentSketches)):
							childNodeSegmentSketch = childNodeSegmentSketches[k]
							rangeValues[k] = self.range.calc( childNodeSegmentSketch, Node.getSegmentLength(self.hsNodePoints, i) )
						avg_children_range_value = CalcUtil.avg( rangeValues )
						diffValue = nodeRangeValue - avg_children_range_value
						if diffValue > maxDiffValue:
							maxDiffValue = diffValue
							self.splitPolicy.splitFrom = Node.getSegmentStart( self.hsNodePoints, i)
							self.splitPolicy.splitTo = Node.getSegmentEnd( self.hsNodePoints, i)
							self.splitPolicy.indicatorIdx = hsNodeSegmentSplitPolicy.getIndicatorSplitIdx()
							self.splitPolicy.indicatorSplitValue = hsNodeSegmentSplitPolicy.getIndicatorSplitValue()
							self.splitPolicy.setNodeSegmentSplitPolicy( hsNodeSegmentSplitPolicy )
							horizontalSplitPoint = self.getHorizontalSplitPoint( self.nodePoints, self.splitPolicy.splitFrom, self.splitPolicy.splitTo)
				if horizontalSplitPoint < 0:
					childNodePoint = list(self.nodePoints)
				else:
					childNodePoint = list(self.nodePoints)
					childNodePoint.append( horizontalSplitPoint )
					childNodePoint.sort()
				self.left = Node(parent = self)
				self.left.initSegments(childNodePoint)
				self.left.isLeft = True
				self.right = Node(parent = self)
				self.right.initSegments(childNodePoint)
				self.right.isLeft = False
				fileBufferManager = FileBufferManager.getInstance()
				fileBuffer = fileBufferManager.getFileBuffer( self.getFileName() )
				l = fileBuffer.getAllTimeSeries()
				for i in range(len(l)):
					ts = l[i]
					if self.splitPolicy.routeToLeft(ts):
						self.left.insert(ts)
					else:
						self.right.insert(ts)
				fileBufferManager.deleteFile(self.getFileName())
		else:
			if self.splitPolicy.routeToLeft( timeSeries ):
				self.left.insert(timeSeries)
			else:
				self.right.insert(timeSeries)
		
	@staticmethod
	def getHorizontalSplitPoint(points, f, t):
		l = 0
		r = len(points) - 1
		while l < r:
			m = int( (l + r) / 2 )
			if points[m] == t:
				return f
			if points[m] < t:
				l = m + 1
			else:
				r = m - 1
		return t

	def getSeriesSegmentSketcher(self):
		return self.seriesSegmentSketcher

	def setSeriesSegmentSketcher(self, seriesSegmentSketcher):
		self.seriesSegmentSketcher = seriesSegmentSketcher

	def getNodeSegmentSketchUpdater(self):
		return self.nodeSegmentSketchUpdater

	def setNodeSegmentSketchUpdater(self, nodeSegmentSketchUpdater):
		self.nodeSegmentSketchUpdater = nodeSegmentSketchUpdater

	def updateStatistics(self, timeSeries):
		self.size = self.size + 1
		for i in range(len(self.nodePoints)):
			nodeSegmentSketch = self.nodeSegmentSketches[i]
			self.nodeSegmentSketchUpdater.updateSketch(nodeSegmentSketch, timeSeries, Node.getSegmentStart(self.nodePoints, i), Node.getSegmentEnd(self.nodePoints, i) )
		for i in range(len(self.hsNodePoints)):
			hsNodeSegmentSketch = self.hsNodeSegmentSketches[i]
			self.nodeSegmentSketchUpdater.updateSketch(hsNodeSegmentSketch, timeSeries, Node.getSegmentStart(self.hsNodePoints, i), Node.getSegmentEnd(self.hsNodePoints, i) )

	def getFileName(self):
		ret = self.indexPath
		if not(ret.endswith("/")):
			ret = ret + "/"
		ret = ret + Node.formatInt(self.getSegmentSize(), 2)
		if not(self.isRoot()):
			if self.isLeft:
				ret = ret + "_L"
			else:
				ret = ret + "_R"
			ret = ret + "_" + str(self.parent.splitPolicy.indicatorIdx) + "_"
			ret = ret + "_" + self.parent.splitPolicy.getNodeSegmentSplitPolicy().__class__.__name__ + "_"
			ret = ret + "(" + str(self.parent.splitPolicy.splitFrom) + "," + str(self.parent.splitPolicy.splitTo) + "," + Node.formatDouble( self.parent.splitPolicy.indicatorSplitValue, 10 ) + ")"
		ret = ret + "_" + str(self.level)
		return ret

	@staticmethod
	def formatInt(value, l):
		ret = str(value)
		while len(ret) < l:
			ret = "0" + ret
		return ret

	@staticmethod
	def formatDouble(value, l):
		ret = str(value)
		while len(ret) > l:
			ret = ret[:-1]
		return ret

	def initSegments(self, segmentPoints):
		self.nodePoints = list(segmentPoints)
		self.hsNodePoints = CalcUtil.split( segmentPoints, 1)
		self.nodeSegmentSketches = []
		for i in range(len(self.nodePoints)):
			self.nodeSegmentSketches.append( NodeSegmentSketch() )
		self.hsNodeSegmentSketches = []
		for i in range(len(self.hsNodePoints)):
			self.hsNodeSegmentSketches.append( NodeSegmentSketch() )

	def approximateSearch(self, queryTs):
		if self.isTerminal():
			return self
		else:
			if self.splitPolicy.routeToLeft(queryTs):
				return self.left.approximateSearch(queryTs)
			else:
				return self.right.approximateSearch(queryTs)

	def saveToFile(self, filePath):
		with open(filePath, "wb") as outfile:
			pickle.dump(self, outfile)

	@staticmethod
	def loadFromFile(filePath):
		with open(filePath, "rb") as infile:
			return pickle.load(infile)


class MeanStdevRange(IRange):
	def calc(self, sketch, l):
		mean_width = sketch.indicators[0] - sketch.indicators[1]
		stdev_upper = sketch.indicators[2]
		stdev_lower = sketch.indicators[3]
		return l * (mean_width * mean_width + stdev_upper * stdev_upper)	


class MeanNodeSegmentSplitPolicy(INodeSegmentSplitPolicy):
	def __init__(self):
		self.indicatorSplitIdx = 0
		self.indicatorSplitValue = 0.0

	def split(self, nodeSegmentSketch):
		max_mean = nodeSegmentSketch.indicators[0]
		min_mean = nodeSegmentSketch.indicators[1]
		self.indicatorSplitValue = (max_mean + min_mean) / 2
		ret = [ NodeSegmentSketch(), NodeSegmentSketch() ]
		ret[0].indicators = list(nodeSegmentSketch.indicators)
		ret[1].indicators = list(nodeSegmentSketch.indicators)
		ret[0].indicators[1] = self.indicatorSplitValue
		ret[1].indicators[0] = self.indicatorSplitValue
		return ret

	def getIndicatorSplitIdx(self):
		return self.indicatorSplitIdx

	def getIndicatorSplitValue(self):
		return self.indicatorSplitValue

class MeanStdevNodeSegmentSketchUpdater(INodeSegmentSketchUpdater):
	def __init__(self, seriesSegmentSketcher):
		self.seriesSegmentSketcher = seriesSegmentSketcher

	def updateSketch(self, nodeSegmentSketch, series, fromIdx, toIdx):
		seriesSegmentSketch = self.seriesSegmentSketcher.doSketch(series, fromIdx, toIdx)
		if nodeSegmentSketch.indicators == None:
			nodeSegmentSketch.indicators = [ float('-inf'), float('inf'), float('-inf'), float('inf') ]
		nodeSegmentSketch.indicators[0] = max(nodeSegmentSketch.indicators[0], seriesSegmentSketch.indicators[0])
		nodeSegmentSketch.indicators[1] = min(nodeSegmentSketch.indicators[1], seriesSegmentSketch.indicators[0])
		nodeSegmentSketch.indicators[2] = max(nodeSegmentSketch.indicators[2], seriesSegmentSketch.indicators[1])
		nodeSegmentSketch.indicators[3] = min(nodeSegmentSketch.indicators[3], seriesSegmentSketch.indicators[1])
		return nodeSegmentSketch

class MeanStdevSeriesSegmentSketcher(ISeriesSegmentSketcher):
	def doSketch(self, series, fromIdx, toIdx):
		seriesSegmentSketch = SeriesSegmentSketch()
		seriesSegmentSketch.indicators = [ CalcUtil.avg(series, fromIdx, toIdx), CalcUtil.deviation(series, fromIdx, toIdx) ]
		return seriesSegmentSketch

class StdevNodeSegmentSplitPolicy(INodeSegmentSplitPolicy):
	def __init__(self):
		self.indicatorSplitIdx = 1
		self.indicatorSplitValue = 0.0

	def split(self, nodeSegmentSketch):
		max_stdev = nodeSegmentSketch.indicators[2]
		min_stdev = nodeSegmentSketch.indicators[3]
		self.indicatorSplitValue = ( max_stdev + min_stdev ) / 2
		ret = [ NodeSegmentSketch(), NodeSegmentSketch() ]
		ret[0].indicators = list(nodeSegmentSketch.indicators)
		ret[1].indicators = list(nodeSegmentSketch.indicators)
		ret[0].indicators[2] = self.indicatorSplitValue
		ret[1].indicators[3] = self.indicatorSplitValue
		return ret

	def getIndicatorSplitIdx(self):
		return self.indicatorSplitIdx

	def getIndicatorSplitValue(self):
		return self.indicatorSplitValue	

class DistTools:
	@staticmethod
	def minDist(node, queryTs):
		s = 0
		points = node.nodePoints
		avg = CalcUtil.avgBySegments(queryTs, points)
		stdDev = CalcUtil.devBySegments(queryTs, points)
		for i in range(len(avg)):
			tmpDist = 0
			if (stdDev[i] - node.nodeSegmentSketches[i].indicators[2]) * (stdDev[i] - node.nodeSegmentSketches[i].indicators[3]) > 0:
				tmpDist = tmpDist + min(abs(stdDev[i] - node.nodeSegmentSketches[i].indicators[2]), abs(stdDev[i] - node.nodeSegmentSketches[i].indicators[3])) ** 2
			if (avg[i] - node.nodeSegmentSketches[i].indicators[0]) * (avg[i] - node.nodeSegmentSketches[i].indicators[1]) > 0:
				tmpDist = tmpDist + min(abs(avg[i] - node.nodeSegmentSketches[i].indicators[0]), (avg[i] - node.nodeSegmentSketches[i].indicators[1])) ** 2
			s = s + tmpDist * Node.getSegmentLength(node.nodePoints, i)
		return math.sqrt(s)


class IndexBuilder:
	@staticmethod
	def buildIndex(fileName, indexPath, threshold, segmentSize, bufferedMemorySize, maxTsCount):
		with open(fileName, "r") as tsFile:	
			tsLength = len([ x for x in re.split(" |\t|\n", tsFile.readline()) if x != ''])
		FileBufferManager.getInstance().tsLength = tsLength
		FileBufferManager.getInstance().setBufferedMemorySize(bufferedMemorySize)
		FileBufferManager.getInstance().setThreshold(threshold)

		if indexPath == None:
			indexPath = fileName
		indexPath = indexPath + ".idx_dyn_" + str(threshold) + "_" + str(segmentSize)
		if maxTsCount > 0:
			indexPath = indexPath + "_" + str(maxTsCount)
		resultFile = indexPath + "_result.txt"
		if os.path.exists(indexPath):
			shutil.rmtree(indexPath)
		os.makedirs(indexPath)

		root = Node(indexPath, threshold)
		nodeSegmentSplitPolicies = [MeanNodeSegmentSplitPolicy(), StdevNodeSegmentSplitPolicy() ]
		root.setNodeSegmentSplitPolicies(nodeSegmentSplitPolicies)

		seriesSegmentSketcher = MeanStdevSeriesSegmentSketcher()
		root.setSeriesSegmentSketcher( seriesSegmentSketcher )
		root.setNodeSegmentSketchUpdater( MeanStdevNodeSegmentSketchUpdater( seriesSegmentSketcher ) )
		root.setRange( MeanStdevRange() )

		points = IndexBuilder.calcPoints(tsLength, segmentSize)
		root.initSegments( points )
		c = 0
		with open(fileName, "r") as tsFile:
			for row in tsFile:
				ts = [float(x) for x in  re.split(" |\t|\n", row) if x != '']
				ts = np.array(ts)
				root.insert(ts)
				c = c + 1
				if maxTsCount > 0 and c >= maxTsCount:
					break
		FileBufferManager.getInstance().saveAllToDisk()
		indexFilePath = indexPath + "\\root.idx"
		root.saveToFile(indexFilePath)
		return root

	@staticmethod
	def calcPoints(tsLength, segmentSize):
		avgLength = int(tsLength / segmentSize)
		points = []
		for i in range(segmentSize):
			points.append( (i + 1) * avgLength )
		points[segmentSize - 1] = tsLength
		return points


class IndexExactSearcher:
	@staticmethod
	def search(data, indexPath):
		DistUtil.resetCache()
		result = []
		root = Node.loadFromFile(indexPath + "\\root.idx")
		for queryTs in data:
			searchAnswer = IndexExactSearcher.exactSearch(queryTs, root)
			result.append( searchAnswer.dist )
		return result

	@staticmethod
	def exactSearch(queryTs, root):
		answer = PqItem()
		answer.node = IndexExactSearcher.approximateSearch(queryTs, root)
		answer.dist = DistUtil.minDistBinary(answer.node.getFileName(), answer.node.getSize(), queryTs)
		pq = queue.PriorityQueue()
		tmpItem = PqItem()
		tmpItem.node = root
		tmpItem.dist = DistTools.minDist(root, queryTs)

		pq.put(tmpItem)
		while not(pq.empty()):
			minPqItem = pq.get()
			if minPqItem.dist > answer.dist:
				break
			if minPqItem.node.isTerminal():
				minPqItem.dist = DistUtil.minDistBinary(minPqItem.node.getFileName(), minPqItem.node.getSize(), queryTs)
				if answer.dist >= minPqItem.dist:
					answer.dist = minPqItem.dist
					answer.node = minPqItem.node
			else:
				tmpItem = PqItem()
				tmpItem.node = minPqItem.node.left
				tmpItem.dist = DistTools.minDist(tmpItem.node, queryTs)
				if tmpItem.dist < answer.dist:
					pq.put(tmpItem)

				tmpItem = PqItem()
				tmpItem.node = minPqItem.node.right
				tmpItem.dist = DistTools.minDist(tmpItem.node, queryTs)
				if tmpItem.dist < answer.dist:
					pq.put(tmpItem)
		return answer

	@staticmethod
	def approximateSearch(queryTs, currentNode):
		if currentNode.isTerminal():
			return currentNode
		else:
			if currentNode.splitPolicy.routeToLeft(queryTs):
				return IndexExactSearcher.approximateSearch(queryTs, currentNode.left)
			else:
				return IndexExactSearcher.approximateSearch(queryTs, currentNode.right)

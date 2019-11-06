"""
@time : 2019/11/6下午9:39
@Author: kongwiki
@File: knn.py
@Email: kongwiki@163.com
"""

import heapq
import random


class Classifier:
	def __init__(self, bucketPrefix, testBucketNumber, dataFormat, k):

		"""
		该分类器程序将从bucketPrefix指定的一系列文件中读取数据,
		并留出testBucketNumber指定的桶来做测试集,其余的做训练集。
		dataFormat用来表示数据的格式,如:
		"class	num	num	num	num	num	comment"
		"""

		self.medianAndDeviation = []
		self.k = k
		# 从文件中读取文件
		self.format = dataFormat.strip().split('\t')
		self.data = []
		# 用1-10标记桶
		for i in range(1, 11):
			# 判断该桶是否包含在训练集中
			if i != testBucketNumber:
				filename = "%s-%02i" % (bucketPrefix, i)
				f = open(filename)
				lines = f.readlines()
				f.close()
				for line in lines[1:]:
					fields = line.strip().split('\t')
					ignore = []
					vector = []
					for i in range(len(fields)):
						if self.format[i] == 'num':
							vector.append(float(fields[i]))
						elif self.format[i] == 'comment':
							ignore.append(fields[i])
						elif self.format[i] == 'class':
							classification = fields[i]
					self.data.append((classification, vector, ignore))
		self.rawData = list(self.data)
		# 获取特征向量的长度
		self.vlen = len(self.data[0][1])
		# 标准化数据
		for i in range(self.vlen):
			self.normalizeColumn(i)

	##################################################
	###
	###  计算修正标准分

	def getMedian(self, alist):
		"""均值"""
		if alist == []:
			return []
		blist = sorted(alist)
		length = len(alist)
		if length % 2 == 1:
			# length of list is odd so return middle element
			return blist[int(((length + 1) / 2) - 1)]
		else:
			# length of list is even so compute midpoint
			v1 = blist[int(length / 2)]
			v2 = blist[(int(length / 2) - 1)]
			return (v1 + v2) / 2.0

	def getAbsoluteStandardDeviation(self, alist, median):
		"""计算绝对偏差"""
		sum = 0
		for item in alist:
			sum += abs(item - median)
		return sum / len(alist)

	def normalizeColumn(self, columnNumber):
		"""标准化self.data中的第columnNumber列"""
		# 将该列的所有值提取到一个列表中
		col = [v[1][columnNumber] for v in self.data]
		median = self.getMedian(col)
		asd = self.getAbsoluteStandardDeviation(col, median)
		# print("Median: %f   ASD = %f" % (median, asd))
		self.medianAndDeviation.append((median, asd))
		for v in self.data:
			v[1][columnNumber] = (v[1][columnNumber] - median) / asd

	def normalizeVector(self, v):
		"""通过已保存了每列的中位数和绝对偏差,通过它们来标准化向量v"""
		vector = list(v)
		for i in range(len(vector)):
			(median, asd) = self.medianAndDeviation[i]
			vector[i] = (vector[i] - median) / asd
		return vector

	###
	### OVER
	##################################################

	def testBucket(self, bucketPrefix, bucketNumber):
		"""交叉验证"""

		filename = "%s-%02i" % (bucketPrefix, bucketNumber)
		f = open(filename)
		lines = f.readlines()
		totals = {}
		f.close()
		for line in lines:
			data = line.strip().split('\t')
			vector = []
			classInColumn = -1
			for i in range(len(self.format)):
				if self.format[i] == 'num':
					vector.append(float(data[i]))
				elif self.format[i] == 'class':
					classInColumn = i
			theRealClass = data[classInColumn]
			# print("REAL ", theRealClass)
			classifiedAs = self.classify(vector)
			totals.setdefault(theRealClass, {})
			totals[theRealClass].setdefault(classifiedAs, 0)
			totals[theRealClass][classifiedAs] += 1
		return totals

	def manhattan(self, vector1, vector2):
		"""曼哈顿距离"""
		return sum(map(lambda v1, v2: abs(v1 - v2), vector1, vector2))

	def nearestNeighbor(self, itemVector):
		"""返回最近距离"""
		return min([(self.manhattan(itemVector, item[1]), item)
					for item in self.data])

	def knn(self, itemVector):
		"""knn"""
		# 使用heapq.nsmallest来获得k个近邻

		neighbors = heapq.nsmallest(self.k,
									[(self.manhattan(itemVector, item[1]), item)
									 for item in self.data])
		# 每个近邻都有投票权
		results = {}
		for neighbor in neighbors:
			theClass = neighbor[1][0]
			results.setdefault(theClass, 0)
			results[theClass] += 1
		resultList = sorted([(i[1], i[0]) for i in results.items()], reverse=True)
		# 获取得票最高的分类
		maxVotes = resultList[0][0]
		possibleAnswers = [i[1] for i in resultList if i[0] == maxVotes]
		# 若得票相等则随机选取一个
		answer = random.choice(possibleAnswers)
		return (answer)

	def classify(self, itemVector):
		"""返回分类结果"""
		return (self.knn(self.normalizeVector(itemVector)))


def tenfold(bucketPrefix, dataFormat, k):
	results = {}
	for i in range(1, 11):
		c = Classifier(bucketPrefix, i, dataFormat, k)
		t = c.testBucket(bucketPrefix, i)
		for (key, value) in t.items():
			results.setdefault(key, {})
			for (ckey, cvalue) in value.items():
				results[key].setdefault(ckey, 0)
				results[key][ckey] += cvalue


	categories = list(results.keys())
	categories.sort()
	print("\n       Classified as: ")
	header = "        "
	subheader = "      +"
	for category in categories:
		header += "% 2s   " % category
		subheader += "-----+"
	print(header)
	print(subheader)
	total = 0.0
	correct = 0.0
	for category in categories:
		row = " %s    |" % category
		for c2 in categories:
			if c2 in results[category]:
				count = results[category][c2]
			else:
				count = 0
			row += " %3i |" % count
			total += count
			if c2 == category:
				correct += count
		print(row)
	print(subheader)
	print("\n%5.3f percent correct" % ((correct * 100) / total))
	print("total of %i instances" % total)


print("SMALL DATA SET")
tenfold("pimaSmall/pimaSmall",
		"num	num	num	num	num	num	num	num	class", 3)
print("\n\nLARGE DATA SET")

tenfold("pima/pima",
		"num	num	num	num	num	num	num	num	class", 3)
"""
@time : 2019/9/26下午5:57
@Author: kongwiki
@File: cluster.py
@Email: kongwiki@163.com
"""
import math
import random


def getMedian(alist):
	"""
	获取一个series的中位数
	:param alist: 一个series
	:return:
	"""
	tmp = list(alist)
	tmp.sort()
	alen = len(tmp)
	if (alen % 2) == 1:
		return tmp[alen // 2]
	else:
		return (tmp[alen // 2] + tmp[(alen // 2) - 1]) / 2


def normalizeColumn(column):
	"""
	计算修正标准分
	:param column:
	:return:
	"""
	median = getMedian(column)
	asd = sum([abs(x - median) for x in column]) / len(column)
	result = [(x - median) / asd for x in column]
	return result


class kClusterer:
	"""KMeans聚类算法 第一列是分类， 其余列是数值型特征"""

	def __init__(self, filename, k):
		"""
		k是簇的数量
		主要完成功能为：
		1. 读取文件内容
		2. 按列存储在self.data中
		3. 计算修正标准分
		4. 随机选择起始点
		5. 将各个点分配给中心点
		:param filename: 文件名
		:param k: 簇的个数
		"""
		file = open(filename)
		self.data = {}
		self.k = k
		self.counter = 0
		self.iterationNumber = 0
		# 用于跟踪本次迭代有多少点的分类发生了变动
		self.pointsChanged = 0
		# 误差平方和
		self.sse = 0
		lines = file.readlines()
		file.close()
		header = lines[0].split(',')
		self.cols = len(header)
		self.data = [[] for i in range(len(header))]
		# 按列存储数据,如self.data[0]是第一列的数据
		# 如：self.data[0][10]是第一列第十行的数据
		for line in lines[1:]:
			cells = line.split(',')
			toggle = 0
			for cell in range(self.cols):
				if toggle == 0:
					self.data[cell].append(cells[cell])
					toggle = 1
				else:
					self.data[cell].append(float(cells[cell]))

		self.datasize = len(self.data[1])
		self.memberOf = [-1 for x in range(len(self.data[1]))]
		#
		# 标准化
		#
		for i in range(1, self.cols):
			self.data[i] = normalizeColumn(self.data[i])

		# 随机选择点
		random.seed()
		self.centroids = [[self.data[i][r] for i in range(1, len(self.data))]
						  for r in random.sample(range(len(self.data[0])),
												 self.k)]
		self.assignPointsToCluster()

	def updateCentroids(self):
		"""
		根据分配结果重新确定聚类中心点
		:return:
		"""
		members = [self.memberOf.count(i) for i in range(len(self.centroids))]
		self.centroids = [[sum([self.data[k][i]
								for i in range(len(self.data[0]))
								if self.memberOf[i] == centroid]) / members[centroid]
						   for k in range(1, len(self.data))]
						  for centroid in range(len(self.centroids))]

	def assignPointToCluster(self, i):
		"""
		根据距离计算所属中心点
		:param i:
		:return:
		"""
		min = 999999
		clusterNum = -1
		for centroid in range(self.k):
			dist = self.euclideanDistance(i, centroid)
			if dist < min:
				min = dist
				clusterNum = centroid
		# 跟踪变动的点
		if clusterNum != self.memberOf[i]:
			self.pointsChanged += 1
		# 计算距离平方和
		self.sse += min ** 2
		return clusterNum

	def assignPointsToCluster(self):
		"""
		分配所有的点
		:return:
		"""
		self.pointsChanged = 0
		self.sse = 0
		self.memberOf = [self.assignPointToCluster(i)
						 for i in range(len(self.data[1]))]

	def euclideanDistance(self, i, j):
		"""
		计算欧几里得距离
		:param i:
		:param j:
		:return:
		"""
		sumSquares = 0
		for k in range(1, self.cols):
			sumSquares += (self.data[k][i] - self.centroids[j][k - 1]) ** 2
		return math.sqrt(sumSquares)

	def kCluster(self):
		"""
		开始进行聚类 步骤如下
		1. 更新中心点
		2. 重新分配
		直至变动的点小于20%
		:return:
		"""
		done = False

		while not done:
			self.iterationNumber += 1
			self.updateCentroids()
			self.assignPointsToCluster()
			#
			# 变动的点少于1%则停止迭代
			#
			if float(self.pointsChanged) / len(self.memberOf) < 0.01:
				done = True
		print("最终误差平方和为(sse): %f" % self.sse)

	def showMembers(self):
		"""
		结果展示
		:return:
		"""
		for centroid in range(len(self.centroids)):
			print("\n\nClass %i\n========" % centroid)
			for name in [self.data[0][i] for i in range(len(self.data[0]))
						 if self.memberOf[i] == centroid]:
				print(name)


if __name__ == '__main__':
	km = kClusterer('../data/cluster/cereal.csv', 3)
	km.kCluster()
	km.showMembers()

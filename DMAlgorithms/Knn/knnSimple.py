"""
@time : 2019/11/6下午9:47
@Author: kongwiki
@File: knnSimple.py
@Email: kongwiki@163.com
"""


class Classifier:

	def __init__(self, filename):

		self.medianAndDeviation = []

		# 读取文件
		f = open(filename)
		lines = f.readlines()
		f.close()
		self.format = lines[0].strip().split('\t')
		self.data = []
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
		# 获取向量的长度
		self.vlen = len(self.data[0][1])
		# 标准化
		for i in range(self.vlen):
			self.normalizeColumn(i)

	##################################################
	###
	###  修正标准分

	def getMedian(self, alist):
		"""从一个数组中获取均值"""
		if alist == []:
			return []
		blist = sorted(alist)
		length = len(alist)
		if length % 2 == 1:
			# 若为奇数
			return blist[int(((length + 1) / 2) - 1)]
		else:
			# 若为偶数
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
	### over
	##################################################

	def manhattan(self, vector1, vector2):
		"""曼哈顿距离"""
		return sum(map(lambda v1, v2: abs(v1 - v2), vector1, vector2))

	def nearestNeighbor(self, itemVector):
		"""近邻"""
		return min([(self.manhattan(itemVector, item[1]), item)
					for item in self.data])

	def classify(self, itemVector):
		"""返回最近的"""
		return (self.nearestNeighbor(self.normalizeVector(itemVector))[1][0])


# 单元测试
def unitTest():
	classifier = Classifier('athletesTrainingSet.txt')
	br = ('Basketball', [72, 162], ['Brittainey Raven'])
	nl = ('Gymnastics', [61, 76], ['Viktoria Komova'])
	cl = ("Basketball", [74, 190], ['Crystal Langhorne'])
	brNorm = classifier.normalizeVector(br[1])
	nlNorm = classifier.normalizeVector(nl[1])
	clNorm = classifier.normalizeVector(cl[1])
	assert (brNorm == classifier.data[1][1])
	assert (nlNorm == classifier.data[-1][1])
	print('normalizeVector fn OK')
	assert (round(classifier.manhattan(clNorm, classifier.data[1][1]), 5) == 1.16823)
	assert (classifier.manhattan(brNorm, classifier.data[1][1]) == 0)
	assert (classifier.manhattan(nlNorm, classifier.data[-1][1]) == 0)
	print('Manhattan distance fn OK')
	result = classifier.nearestNeighbor(brNorm)
	assert (result[1][2] == br[2])
	result = classifier.nearestNeighbor(nlNorm)
	assert (result[1][2] == nl[2])
	assert (classifier.nearestNeighbor(clNorm)[1][2][0] == "Jennifer Lacy")
	print("Nearest Neighbor fn OK")
	assert (classifier.classify(br[1]) == 'Basketball')
	assert (classifier.classify(cl[1]) == 'Basketball')
	assert (classifier.classify(nl[1]) == 'Gymnastics')
	print('Classify fn OK')


def main(training_filename, test_filename):
	"""测试"""
	classifier = Classifier(training_filename)
	f = open(test_filename)
	lines = f.readlines()
	f.close()
	numCorrect = 0.0
	for line in lines:
		data = line.strip().split('\t')
		vector = []
		classInColumn = -1
		for i in range(len(classifier.format)):
			if classifier.format[i] == 'num':
				vector.append(float(data[i]))
			elif classifier.format[i] == 'class':
				classInColumn = i
		theClass = classifier.classify(vector)
		prefix = '-'
		if theClass == data[classInColumn]:
			# 准确率
			numCorrect += 1
			prefix = '+'
		print("%s  %12s  %s" % (prefix, theClass, line))
	print("%4.2f%% correct" % (numCorrect * 100 / len(lines)))


if __name__ == '__main__':
	main('athletesTrainingSet.txt', 'athletesTestSet.txt')

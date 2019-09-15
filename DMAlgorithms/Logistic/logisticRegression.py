"""
@time : 2019/9/15下午8:34
@Author: kongwiki
@File: logisticRegression.py
@Email: kongwiki@163.com
"""
"""
逻辑回归算法的实现
基于梯度算法
"""
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = './data/testSet.txt'


# with open(data) as f:
# 	reader = f.readlines()
# f.close()
# for i in reader:
# 	print(i.strip())

def load_data_set():
	"""
	加载数据及
	:return: 返回两个数组
		data_arr: 原始数据的特征
		label_arr: 原始数据集的标签
	"""
	data_arr = []
	label_arr = []
	f = open('./data/testSet.txt')
	for line in f.readlines():
		line_arr = line.strip().split()
		data_arr.append([1.0, np.float(line_arr[0]), np.float(line_arr[1])])
		label_arr.append(int(line_arr[2]))
	return data_arr, label_arr


def sigmoid(x):
	return 1.0/(1+np.exp(-x))


def plotBestFit(dataArr, labelMat, weight):
	"""
	将得到的数据可视化
	:param dataArr:  样本数据特征
	:param labelMat:  样本数据的类别标签
	:param weight:  回归系数
	:return: None
	"""
	n = np.shape(dataArr)[0]
	xcord1 = []
	ycord1 = []
	xcord2 = []
	ycord2 = []
	for i in range(n):
		if int(labelMat[i]) == 1:
			xcord1.append(dataArr[i, 1])
			ycord1.append(dataArr[i, 2])
		else:
			xcord2.append(dataArr[i, 1])
			ycord2.append(dataArr[i, 2])
	fig, [ax1, ax2] = plt.subplots(3, 1, figsize=(20, 15))
	sns.scatterplot(x=xcord1, y=ycord1, frozenset=15, ax=ax1)
	ax1.set_title("训练集数据")
	ax1.set_xlabel('x')
	ax1.set_ylabel('y')

	sns.scatterplot(x=xcord2, y=ycord2, frozenset=15, ax=ax2)
	ax2.set_title("测试集数据")
	ax2.set_xlabel('x')
	ax2.set_ylabel('y')

	x = np.arange(-3.0, 3.0, 0.1)
	y = (-weight[0] - weight[1]*x)/weight[2]
	plt.show()


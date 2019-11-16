"""
@time : 2019/11/9下午4:39
@Author: kongwiki
@File: decisionTree.py
@Email: kongwiki@163.com
"""
from math import log
import operator
import csv
import numpy as np


# 测试数据
def createDataSet():
	dataSet = [[1, 1, 'yes'],
			   [1, 1, 'yes'],
			   [1, 0, 'no'],
			   [0, 1, 'no'],
			   [0, 1, 'no']]
	labels = ['no surfacing', 'flippers']
	# change to discrete values
	return dataSet, labels


def createDataSetByFile():
	reader = csv.reader(open("/home/kongweikun/PycharmProjects/DataMining/InAction/Bank/数字化之后的数据集.csv"))
	header = next(reader)
	dataSet = []
	for row in reader:
		singRow = [int(i) for i in row]
		dataSet.append(singRow)
	labels = header

	return dataSet, labels


## 计算香农熵
def calcShannonEnt(dataSet):
	numEntries = len(dataSet)
	labelCounts = {}
	for featVec in dataSet:
		currentLabel = featVec[-1]
		if currentLabel not in labelCounts.keys(): labelCounts[currentLabel] = 0
		labelCounts[currentLabel] += 1
	shannonEnt = 0.0
	for key in labelCounts:
		prob = float(labelCounts[key]) / numEntries
		shannonEnt -= prob * log(prob, 2) # 公式 具体公式详见<统计学习方法>
	return shannonEnt


## 切分数据
def splitDataSet(dataSet, axis, value):
	retDataSet = []
	for featVec in dataSet:
		if featVec[axis] == value:
			reducedFeatVec = featVec[:axis]
			reducedFeatVec.extend(featVec[axis + 1:])
			retDataSet.append(reducedFeatVec)
	return retDataSet


def chooseBestFeatureToSplit(dataSet, labels):
	"""
	选取当前迭代的最佳特征
	:param dataSet:  去标签的数据集
	:param labels:  标签
	:return: 最佳特征名称, 对应的索引
	"""
	numFeatures = len(dataSet[0]) - 1  # 特征的数量-1
	baseEntropy = calcShannonEnt(dataSet) # 计算香农熵
	bestInfoGain = 0.0
	bestFeature = -1
	for i in range(numFeatures):  # 迭代
		featList = [example[i] for example in dataSet]  # n*m的数组 储存特征
		uniqueVals = set(featList)  # 去除重复
		newEntropy = 0.0
		for value in uniqueVals:
			subDataSet = splitDataSet(dataSet, i, value)
			prob = len(subDataSet) / float(len(dataSet))
			newEntropy += prob * calcShannonEnt(subDataSet)
		infoGain = baseEntropy - newEntropy  # 计算信息增益
		print("特征{}的信息增益为{}".format(labels[i],infoGain))
		if (infoGain > bestInfoGain):  # 获取当前最好的特征
			bestInfoGain = infoGain
			bestFeature = i
	print("当前选取的特征为{} 信息增益为{}".format(labels[bestFeature], bestInfoGain))
	print("\n")
	return labels[bestFeature] , bestFeature  # 返回特征名称


def majorityCnt(classList):

	classCount = {}
	for vote in classList:
		if vote not in classCount.keys():
			classCount[vote] = 0
		classCount[vote] += 1
	print(classCount)
	# sortedClassCount = sorted(classCount, key=lambda x:x[1], reverse=True)
	# print(classCount.values())
	# return sortedClassCount[0][0]


def createTree(dataSet, labels):
	classList = [example[-1] for example in dataSet]
	if classList.count(classList[0]) == len(classList):
		return classList[0]  # stop splitting when all of the classes are equal
	if len(dataSet[0]) == 1:  # stop splitting when there are no more features in dataSet
		return majorityCnt(classList)
	bestFeat = chooseBestFeatureToSplit(dataSet, labels)[1]
	bestFeatLabel = labels[bestFeat]
	myTree = {bestFeatLabel: {}}
	del (labels[bestFeat])
	featValues = [example[bestFeat] for example in dataSet]
	uniqueVals = set(featValues)
	for value in uniqueVals:
		subLabels = labels[:]  # copy all of labels, so trees don't mess up existing labels
		myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
	return myTree


def classify(inputTree, featLabels, testVec):
	firstStr = inputTree.keys()[0]
	secondDict = inputTree[firstStr]
	featIndex = featLabels.index(firstStr)
	key = testVec[featIndex]
	valueOfFeat = secondDict[key]
	if isinstance(valueOfFeat, dict):
		classLabel = classify(valueOfFeat, featLabels, testVec)
	else:
		classLabel = valueOfFeat
	return classLabel


def storeTree(inputTree, filename):
	import pickle
	fw = open(filename, 'w')
	pickle.dump(inputTree, fw)
	fw.close()


def grabTree(filename):
	import pickle
	fr = open(filename)
	return pickle.load(fr)

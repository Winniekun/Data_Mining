## 概述

### 开发环境

1. 操作系统： Ubuntu18.04 LTS
2. 处理器： Intel® Core™ i5-6200U CPU @ 2.30GHz × 4
3. 语言&版本： Python3.6.8

### 数据挖掘过程

数据挖掘的实现过程是由以下几个阶段来完成，其中包括原始数据、数据准备、数据挖掘、模式的评估解释、知识的运用这几个方面。在数据挖掘的过程需要多次的循环往复，一旦某个步骤与预期目标不符，则需要回溯到前面的步骤，重新调整和执行。

步骤分为:

1. 数据准备

   根据已经建好的数据仓库，进行数据预处理，然后对数据进行选择、清洗、转换、数据缩减等。

2. 数据挖掘

   选择相应的算法，分析数据

### 本次数据挖掘的背景

此次案例基于某银行的一次电话营销，数据记录了在此次案例中银行联系的每位客户的基本情况，例如客户的工作类型、是否已婚、教育层次以及上一次电话的营销结果的信息，以此来分辨哪一类客户较容易订购银行的定期存款。

本项目根据记录在案的各项数据，通过数据挖掘技术来预测本次电话营销是否会成功

## 决策树算法

#### 算法描述

1. 决策树是一种基本的分类与回归方法。
2. 决策树模型是描述对样本进行分类的树形结构。树由结点和有向边组成：
    2.1: 内部结点表示一个特征或者属性。
    2.2: 叶子结点表示一个分类。
    2.3: 有向边代表了一个划分规则。
3. 决策树从根结点到子结点的的有向边代表了一条路径。决策树的路径是互斥并且是完备的。
4. 用决策树分类时，对样本的某个特征进行测试，根据测试结果将样本分配到树的子结点上。
    此时每个子结点对应该特征的一个取值。
    递归地对样本测试，直到该样本被划分叶结点。最后将样本分配为叶结点所属的类。
5. 决策树的优点：可读性强，分类速度快。
6. 决策树学习通常包括3个步骤：
    6.1: 特征选择。
    6.2: 决策树生成。
    6.3: 决策树剪枝。

#### 树的生成

1. 构建根结点：将所有训练数据放在根结点。
2. 选择一个最优特征，根据这个特征将训练数据分割成子集，使得各个子集有一个在当前条件下最好的分类。
    2.1: 若这些子集已能够被基本正确分类，则将该子集构成叶结点。
    2.2: 若某个子集不能够被基本正确分类，则对该子集选择新的最优的特征，继续对该子集进行分割，构建相应的结点。

3. 如此递归下去，直至所有训练数据子集都被基本正确分类，或者没有合适的特征为止。



## 算法实现

以下是算法实现的程序代码:

```python
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

```

#### 第一次每个特征对应的信息增益

| **特征**  | **信息增益**           |
| --------- | ---------------------- |
| job       | 0.011311004896739252   |
| marital   | 0.0017391272677400038  |
| education | 0.004015602339691449   |
| default   | 0.004804910611133195   |
| housing   | 0.00011749654789877662 |
| loan      | 0.00020655592683432866 |
| month     | 0.03557626139529624    |
| poutcome  | 0.04696434901697255    |

### 树的可视化

因为生成的树过于大,无法进行直观的表示,所以换了一种数据结构进行表示(字典)

```
myTree = {'poutcome': {0: {'month': {0: {'job': {0: {'housing': {0: {'education': {1: 1, 2: 0, 3: {'marital': {1: 1, 2: 0}}, 5: 0}}, 1: 0, 2: 0}}, 1: {'education': {0: 0, 1: 0, 2: {'default': {0: {'housing': {0: 0, 2: {'y': {0: 0, 1: 1}}}}, 1: 0}}, 3: 0, 5: 0, 7: 0}}, 2: 0, 4: 0, 5: {'education': {0: 1, 3: 0, 6: 0}}, 6: 0, 7: 0, 9: {'housing': {0: 0, 1: 1, 2: 0}}, 10: 0}}, 1: {'loan': {0: {'job': {0: {'marital': {0: 0, 1: {'housing': {0: 1, 2: 0}}, 2: 0}}, 4: {'education': {2: 0, 6: 1}}, 5: 0, 6: 0, 8: {'education': {3: {'y': {0: 0, 1: 1}}, 5: 1, 7: {'default': {0: {'y': {0: 0, 1: 1}}, 1: 0}}}}, 9: {'education': {5: 0, 6: 1, 7: 0}}}}, 2: 1}}, 2: {'job': {0: {'marital': {1: 1, 2: 0}}, 4: 0, 5: 0, 6: 1, 9: 1, 11: 1}}, 3: {'job': {0: 0, 1: 1, 5: {'marital': {0: 0, 1: 1}}, 6: 0, 8: 0, 9: 0}}, 4: {'job': {0: {'marital': {0: 0, 1: 1, 2: 1}}, 1: 1, 5: 0, 7: {'marital': {1: 0, 2: 1}}, 8: 0, 9: {'marital': {0: 0, 1: {'education': {5: 1, 6: 0}}, 2: 1}}, 10: 1, 11: 0}}, 5: {'housing': {0: {'job': {0: 1, 1: 1, 5: 1, 6: 0, 8: 1}}, 1: 1, 2: 0}}, 6: {'job': {0: {'education': {0: 0, 1: 0, 2: 0, 3: 0, 5: 0, 6: {'marital': {0: 0, 1: {'housing': {0: 0, 2: {'y': {0: 0, 1: 1}}}}, 2: 0}}}}, 1: {'education': {0: 0, 1: 0, 2: {'marital': {0: 0, 1: {'loan': {0: {'contact': {0: {'housing': {0: {'default': {0: 0, 1: None}}, 2: {'default': {0: 1, 1: 0}}}}, 1: 0}}, 2: 0}}, 2: 0}}, 3: {'housing': {0: 0, 2: {'marital': {0: 1, 1: {'y': {0: 0, 1: 1}}}}}}, 5: {'housing': {0: {'marital': {1: 1, 2: 0}}, 2: 0}}, 7: 0}}, 2: 0, 3: 0, 4: {'housing': {0: {'marital': {1: {'y': {0: 0, 1: 1}}, 2: 0}}, 2: 0}}, 5: {'marital': {0: 1, 1: 0}}, 6: {'education': {2: {'housing': {0: 0, 2: {'contact': {0: 1, 1: 0}}}}, 3: 0, 5: {'marital': {1: 0, 2: 1}}, 6: 0}}, 7: {'education': {2: {'marital': {0: 0, 1: {'housing': {0: 1, 2: 0}}, 2: 0}}, 3: 0, 5: 0, 6: 0, 7: 0}}, 8: {'education': {3: 0, 7: 1}}, 9: {'housing': {0: {'education': {3: 0, 5: {'loan': {0: {'y': {0: 0, 1: 1}}, 2: 0}}}}, 1: 1, 2: {'education': {3: 0, 5: {'marital': {1: 0, 2: {'y': {0: 0, 1: 1}}}}, 6: 0, 7: 0}}}}, 10: 0}}, 7: {'job': {0: {'education': {3: {'housing': {0: {'loan': {0: {'marital': {1: {'y': {0: 0, 1: 1}}, 2: {'y': {0: 0, 1: 1}}}}, 2: 0}}, 1: 0, 2: 0}}, 6: 0}}, 1: 0, 2: {'marital': {1: 0, 2: 1}}, 3: 0, 4: {'education': {0: 1, 1: 0, 2: 0, 5: 0, 6: 0, 7: 0}}, 5: 0, 6: 0, 7: 0, 8: 0, 9: {'marital': {0: 1, 1: 0, 2: {'education': {2: 0, 5: {'y': {0: 0, 1: 1}}, 6: {'y': {0: 0, 1: 1}}}}}}, 10: 0, 11: 0}}, 8: {'job': {0: {'loan': {0: {'marital': {1: {'housing': {0: 1, 2: 0}}, 2: 0}}, 2: 1}}, 1: 0, 2: 0, 4: 1, 5: {'default': {0: 1, 1: 0}}, 7: 0, 8: {'education': {2: 0, 3: 1, 7: 0}}, 9: {'housing': {0: 0, 2: 1}}}}, 9: {'job': {0: {'education': {3: 0, 5: 1, 6: {'marital': {1: 0, 2: {'y': {0: 0, 1: 1}}}}, 7: 0}}, 2: 0, 4: {'housing': {0: 0, 1: 1}}, 5: 0, 7: 0, 8: 0, 9: 1, 10: 0}}}}, 1: {'month': {0: {'job': {0: {'marital': {0: {'education': {3: 0, 6: 1}}, 1: {'education': {3: {'housing': {0: 0, 2: 1}}, 5: 1, 6: {'loan': {0: {'y': {0: 0, 1: 1}}, 2: {'y': {0: 0, 1: 1}}}}}}, 2: {'loan': {0: {'education': {3: {'housing': {0: {'contact': {0: {'y': {0: 0, 1: 1}}, 1: 0}}, 2: 0}}, 6: {'housing': {0: 0, 2: {'y': {0: 0, 1: 1}}}}, 7: 0}}, 2: 0}}}}, 1: {'education': {0: 0, 1: {'loan': {0: {'y': {0: 0, 1: 1}}, 2: 0}}, 2: 0, 3: 0, 5: 0, 7: 0}}, 2: {'education': {0: 1, 6: 0}}, 3: 0, 4: {'marital': {0: 0, 1: 0, 2: {'housing': {0: 0, 2: 1}}}}, 5: {'education': {0: {'housing': {0: 0, 2: 1}}, 1: 0, 2: 0, 6: {'y': {0: 0, 1: 1}}}}, 6: 0, 7: {'education': {0: 0, 1: 0, 2: 0, 3: {'marital': {0: {'default': {0: 1, 1: 0}}, 1: 0, 2: 0}}, 6: 0, 7: 1}}, 8: 0, 9: {'education': {1: 0, 2: 0, 3: {'marital': {1: 1, 2: 0}}, 5: {'default': {0: {'y': {0: 0, 1: 1}}, 1: 0}}, 6: {'contact': {0: 0, 1: 1}}, 7: 1}}, 10: 0}}, 1: {'job': {0: {'marital': {0: {'housing': {0: {'education': {3: 0, 6: {'default': {0: {'y': {0: 0, 1: 1}}, 1: 0}}}}, 2: 0}}, 1: {'loan': {0: {'housing': {0: {'education': {2: 0, 3: 0, 6: {'default': {0: {'y': {0: 0, 1: 1}}, 1: 0}}, 7: 0}}, 2: {'education': {0: 0, 2: 0, 3: {'default': {0: {'y': {0: 0, 1: 1}}, 1: 0}}, 5: 0, 6: {'default': {0: {'contact': {0: None, 1: 0}}, 1: {'y': {0: 0, 1: 1}}}}, 7: 0}}}}, 1: 0, 2: 0}}, 2: {'loan': {0: {'education': {3: 0, 5: 0, 6: {'default': {0: {'contact': {0: {'housing': {0: None, 2: None}}, 1: 0}}, 1: 0}}}}, 1: 0, 2: 0}}, 3: 1}}, 1: {'education': {0: {'contact': {0: 0, 1: 1}}, 1: 0, 2: {'default': {0: {'loan': {0: {'marital': {0: 0, 1: {'contact': {0: {'housing': {0: None, 2: 1}}, 1: 0}}}}, 2: 0}}, 1: 0}}, 3: 0, 5: 0, 7: 0}}, 2: {'education': {0: 0, 3: 0, 6: {'default': {0: {'housing': {0: 0, 2: {'y': {0: 0, 1: 1}}}}, 1: 0}}, 7: 0}}, 3: {'education': {0: 0, 1: 0, 3: 0, 5: 0, 6: {'marital': {1: {'loan': {0: {'y': {0: 0, 1: 1}}, 2: 0}}, 2: 0}}, 7: 0}}, 4: {'housing': {0: {'marital': {0: 1, 1: {'loan': {0: {'education': {3: {'y': {0: 0, 1: 1}}, 6: {'default': {0: {'y': {0: 0, 1: 1}}, 1: 0}}}}, 2: 0}}, 2: 0}}, 1: 0, 2: 0}}, 5: {'education': {0: 0, 2: 1, 3: 0, 4: 0, 5: {'default': {0: 0, 1: {'y': {0: 0, 1: 1}}}}, 6: {'loan': {0: 0, 2: 1}}, 7: 1}}, 6: 0, 7: {'marital': {1: 0, 2: {'housing': {0: 0, 1: 0, 2: 1}}}}, 8: {'education': {2: 0, 6: 1, 7: 0}}, 9: {'marital': {0: 0, 1: {'education': {3: {'housing': {0: {'default': {0: {'y': {0: 0, 1: 1}}, 1: 1}}, 1: 0, 2: 0}}, 5: {'housing': {0: 0, 2: {'loan': {0: {'default': {0: {'contact': {0: None, 1: 0}}, 1: 0}}, 2: 0}}}}, 6: 0, 7: 0}}, 2: {'education': {3: {'housing': {0: {'y': {0: 0, 1: 1}}, 2: {'loan': {0: 0, 2: {'y': {0: 0, 1: 1}}}}}}, 5: {'housing': {0: 0, 1: 0, 2: {'loan': {0: {'y': {0: 0, 1: 1}}, 2: 0}}}}, 6: {'housing': {0: 0, 2: {'default': {0: {'contact': {0: {'loan': {0: None, 2: None}}, 1: 0}}, 1: 0}}}}}}, 3: 0}}, 10: 0, 11: {'contact': {0: 0, 1: 1}}}}, 2: {'job': {0: 1, 1: 0, 3: 0, 4: 1, 5: 0, 6: 1, 8: 0, 10: 1}}, 3: {'job': {0: {'education': {1: {'default': {0: 0, 1: 1}}, 2: {'marital': {0: {'housing': {0: 1, 2: 0}}, 1: 0, 2: 0}}, 3: {'default': {0: 0, 1: {'marital': {0: 1, 1: 0, 2: {'housing': {0: {'y': {0: 0, 1: 1}}, 2: 0}}}}}}, 5: 0, 6: {'default': {0: {'marital': {0: {'loan': {0: 0, 2: 1}}, 1: {'loan': {0: {'housing': {0: {'contact': {0: None, 1: None}}, 2: {'contact': {0: None, 1: 0}}}}, 2: 0}}, 2: {'contact': {0: {'loan': {0: {'housing': {0: None, 2: None}}, 2: 0}}, 1: 0}}, 3: 0}}, 1: 0}}, 7: 0}}, 1: {'education': {0: {'default': {0: {'loan': {0: {'marital': {0: 0, 1: {'contact': {0: {'housing': {0: None, 2: None}}, 1: 0}}, 2: 0}}, 1: 0, 2: {'marital': {1: 1, 2: 0}}}}, 1: 0}}, 1: {'marital': {0: {'default': {0: 0, 1: 1}}, 1: {'default': {0: 0, 1: {'housing': {0: {'loan': {0: {'y': {0: 0, 1: 1}}, 2: 0}}, 2: 0}}}}, 2: {'loan': {0: 0, 1: 0, 2: {'y': {0: 0, 1: 1}}}}}}, 2: {'default': {0: {'marital': {0: 0, 1: {'loan': {0: {'contact': {0: {'housing': {0: None, 2: None}}, 1: 0}}, 2: 0}}, 2: {'loan': {0: 0, 2: {'y': {0: 0, 1: 1}}}}}}, 1: 0}}, 3: {'marital': {0: {'default': {0: 1, 1: 0}}, 1: 0, 2: 0}}, 5: {'marital': {1: {'y': {0: 0, 1: 1}}, 2: 0}}, 6: 0, 7: 0}}, 2: {'marital': {0: 0, 1: 0, 2: {'education': {6: 0, 7: 1}}}}, 3: {'marital': {0: 1, 1: 0, 2: 0}}, 4: {'education': {0: 0, 3: {'housing': {0: 0, 2: 1}}, 5: 0, 6: 0, 7: 0}}, 5: {'education': {0: {'default': {0: {'housing': {0: {'loan': {0: {'y': {0: 0, 1: 1}}, 2: 0}}, 2: 0}}, 1: 0}}, 1: 0, 2: 0, 3: {'marital': {1: 1, 2: 0}}, 5: 0, 6: 0}}, 6: {'education': {0: 0, 2: 0, 3: 0, 5: 0, 6: {'housing': {0: {'loan': {0: {'marital': {0: 0, 1: 0, 2: {'y': {0: 0, 1: 1}}}}, 2: 1}}, 1: 0, 2: 0}}, 7: 0}}, 7: {'education': {0: {'marital': {0: 0, 1: 1}}, 1: 0, 2: {'marital': {0: 0, 1: {'housing': {0: 0, 2: {'default': {0: {'contact': {0: 1, 1: 0}}, 1: 0}}}}, 2: 0}}, 3: {'default': {0: {'marital': {0: 0, 1: 0, 2: {'loan': {0: {'contact': {0: {'y': {0: 0, 1: 1}}, 1: 0}}, 1: 0, 2: 0}}}}, 1: {'marital': {0: 1, 1: {'contact': {0: 0, 1: 1}}, 2: {'housing': {0: 1, 2: 0}}}}}}, 5: {'loan': {0: 0, 2: {'y': {0: 0, 1: 1}}}}, 6: 0, 7: 1}}, 8: 0, 9: {'education': {1: 0, 2: {'loan': {0: 0, 2: 1}}, 3: {'housing': {0: 0, 2: {'marital': {0: 0, 1: {'default': {0: 0, 1: {'loan': {0: 1, 2: 0}}}}, 2: {'contact': {0: {'y': {0: 0, 1: 1}}, 1: 0}}}}}}, 5: {'contact': {0: {'default': {0: {'housing': {0: {'loan': {0: {'marital': {0: 0, 1: None, 2: None}}, 2: {'y': {0: 0, 1: 1}}}}, 2: {'marital': {0: {'loan': {0: None, 2: 0}}, 1: {'loan': {0: None, 2: 0}}, 2: 0}}}}, 1: 0}}, 1: 0}}, 6: 0, 7: 0}}, 10: {'education': {0: 1, 2: 0, 3: 0, 5: {'default': {0: 0, 1: 1}}, 6: 0, 7: 0}}, 11: {'education': {0: {'default': {0: {'housing': {0: 0, 2: 1}}, 1: 0}}, 2: 0, 3: 0, 7: 0}}}}, 4: {'contact': {0: {'job': {0: {'marital': {0: {'education': {3: 1, 6: 0}}, 1: 1, 2: {'education': {3: 1, 6: {'housing': {0: 0, 2: {'loan': {0: {'y': {0: 0, 1: 1}}, 2: 0}}}}}}}}, 1: 1, 3: 0, 4: 0, 5: {'education': {0: 0, 3: {'y': {0: 0, 1: 1}}, 5: 1}}, 6: {'marital': {1: {'housing': {0: 1, 2: {'y': {0: 0, 1: 1}}}}, 2: 0}}, 7: {'education': {3: {'marital': {1: 0, 2: 1}}, 7: 1}}, 8: {'education': {3: 1, 5: 0, 7: 1}}, 9: {'education': {3: 1, 5: {'marital': {1: 0, 2: {'housing': {0: 1, 2: 0}}}}, 6: {'housing': {0: {'marital': {1: {'y': {0: 0, 1: 1}}, 2: {'y': {0: 0, 1: 1}}}}, 2: 1}}}}, 10: {'marital': {1: 0, 2: 1, 3: 0}}}}, 1: {'job': {0: {'education': {0: 0, 1: 0, 2: 0, 3: {'housing': {0: {'marital': {1: {'default': {0: {'y': {0: 0, 1: 1}}, 1: 0}}, 2: 0}}, 1: 0, 2: 0}}, 5: 0, 6: {'marital': {0: {'housing': {0: 0, 2: 1}}, 1: 0, 2: {'default': {0: 0, 1: {'housing': {0: 0, 2: 1}}}}}}, 7: 0}}, 1: {'education': {0: {'marital': {0: {'default': {0: {'housing': {0: 1, 2: 0}}, 1: 0}}, 1: {'default': {0: 0, 1: {'housing': {0: {'loan': {0: 0, 2: None}}, 2: {'loan': {0: None, 2: 0}}}}}}, 2: {'housing': {0: {'loan': {0: {'y': {0: 0, 1: 1}}, 2: 0}}, 2: 0}}}}, 1: 0, 2: {'loan': {0: {'marital': {0: 0, 1: {'default': {0: {'housing': {0: None, 2: None}}, 1: {'housing': {0: None, 2: 0}}}}, 2: {'housing': {0: {'default': {0: None, 1: 0}}, 2: 0}}}}, 1: 0, 2: {'housing': {0: 0, 2: 1}}}}, 3: 0, 5: 0, 7: 0}}, 2: 0, 3: 0, 4: {'education': {0: 0, 1: 0, 2: {'marital': {0: 0, 1: {'loan': {0: {'y': {0: 0, 1: 1}}, 2: 0}}}}, 3: 0, 6: {'housing': {0: {'marital': {0: 0, 1: {'default': {0: {'y': {0: 0, 1: 1}}, 1: 0}}, 2: {'y': {0: 0, 1: 1}}}}, 2: 0}}, 7: 0}}, 5: {'education': {0: {'marital': {0: 0, 1: {'housing': {0: 1, 2: 0}}, 2: 0}}, 1: 0, 2: 0, 5: 0, 6: 0}}, 6: 0, 7: {'housing': {0: 0, 1: {'marital': {1: 0, 2: {'education': {1: 0, 2: 1}}}}, 2: 0}}, 8: {'education': {3: 0, 5: 0, 6: {'default': {0: 0, 1: 1}}, 7: 0}}, 9: {'education': {0: 0, 1: 0, 2: 0, 3: 0, 5: {'default': {0: {'housing': {0: 0, 2: {'marital': {0: 0, 1: {'y': {0: 0, 1: 1}}, 2: 0}}}}, 1: {'loan': {0: {'marital': {0: 0, 1: 0, 2: {'housing': {0: 1, 2: 0}}}}, 1: 0, 2: 1}}}}, 6: 0, 7: 0}}, 10: 0, 11: {'housing': {0: 1, 2: 0}}}}}}, 5: {'job': {0: {'marital': {1: {'education': {3: 1, 6: 0}}, 2: 1}}, 1: 0, 4: {'housing': {0: 1, 2: 0}}, 5: {'marital': {0: 0, 1: 1}}, 6: {'y': {0: 0, 1: 1}}, 7: 1, 8: 1, 9: {'education': {5: {'loan': {0: 0, 2: {'marital': {1: 1, 2: 0}}}}, 6: 1}}}}, 6: {'contact': {0: {'job': {0: {'education': {0: 0, 1: 0, 2: {'housing': {0: 0, 2: 1}}, 3: {'marital': {0: 0, 1: {'default': {0: {'housing': {0: 0, 2: {'loan': {0: None, 2: 0}}}}, 1: {'y': {0: 0, 1: 1}}}}, 2: 0}}, 5: {'marital': {1: 0, 2: {'housing': {0: 0, 2: 1}}}}, 6: {'marital': {0: {'y': {0: 0, 1: 1}}, 1: {'default': {0: {'loan': {0: {'housing': {0: None, 2: None}}, 2: {'y': {0: 0, 1: 1}}}}, 1: 0}}, 2: {'loan': {0: {'default': {0: {'housing': {0: None, 2: None}}, 1: 0}}, 2: 0}}}}, 7: 0}}, 1: {'education': {0: 0, 1: {'housing': {0: 0, 2: {'marital': {0: 0, 1: {'default': {0: {'y': {0: 0, 1: 1}}, 1: {'y': {0: 0, 1: 1}}}}, 2: 0}}}}, 2: {'housing': {0: {'marital': {0: 0, 1: {'default': {0: {'loan': {0: None, 2: 0}}, 1: 0}}, 2: 0}}, 1: 0, 2: 0}}, 3: {'marital': {0: 1, 1: 0, 2: {'housing': {0: {'default': {0: {'loan': {0: None, 2: 0}}, 1: 0}}, 2: 0}}}}, 5: 0, 6: 0, 7: 0}}, 2: {'education': {0: 1, 1: 0, 2: 0, 6: 0}}, 3: 0, 4: {'education': {2: {'default': {0: {'housing': {0: 0, 2: 1}}, 1: 0}}, 3: {'housing': {0: {'marital': {1: {'y': {0: 0, 1: 1}}, 2: 0}}, 2: 0}}, 5: 1, 6: {'marital': {0: 0, 1: {'housing': {0: 0, 2: {'default': {0: {'loan': {0: None, 2: 0}}, 1: 0}}}}, 2: 0}}}}, 5: {'education': {0: 1, 2: 0, 3: 0, 5: 0, 6: 0}}, 6: {'education': {2: 0, 3: {'marital': {1: 1, 2: 0}}, 5: 0, 6: 0}}, 7: {'marital': {0: {'education': {0: 0, 2: 0, 3: {'default': {0: {'housing': {0: {'y': {0: 0, 1: 1}}, 2: 1}}, 1: 0}}, 7: 0}}, 1: {'housing': {0: 0, 2: {'default': {0: {'loan': {0: {'y': {0: 0, 1: 1}}, 2: 0}}, 1: 0}}}}, 2: 0}}, 8: 0, 9: {'education': {2: 0, 3: 0, 5: {'loan': {0: {'marital': {0: {'housing': {0: 0, 2: {'y': {0: 0, 1: 1}}}}, 1: {'housing': {0: {'default': {0: 1, 1: 0}}, 2: 0}}, 2: 0}}, 1: {'marital': {1: 0, 2: {'y': {0: 0, 1: 1}}}}, 2: 0}}, 6: {'marital': {1: 0, 2: {'housing': {0: 0, 2: {'y': {0: 0, 1: 1}}}}}}}}, 10: 0, 11: 0}}, 1: {'job': {0: {'marital': {0: 0, 1: 0, 2: {'education': {0: 0, 1: 0, 2: 0, 3: {'housing': {0: {'default': {0: {'loan': {0: None, 2: 0}}, 1: 0}}, 2: 0}}, 5: 0, 6: {'loan': {0: {'housing': {0: {'default': {0: None, 1: 0}}, 2: 0}}, 2: {'y': {0: 0, 1: 1}}}}, 7: {'default': {0: {'housing': {0: 0, 2: 1}}, 1: 0}}}}, 3: 0}}, 1: {'education': {0: 0, 1: {'marital': {0: 0, 1: {'loan': {0: {'default': {0: {'housing': {0: None, 2: None}}, 1: 0}}, 2: {'default': {0: 0, 1: {'y': {0: 0, 1: 1}}}}}}, 2: 0}}, 2: {'housing': {0: {'default': {0: {'marital': {0: 0, 1: {'loan': {0: None, 2: None}}, 2: {'y': {0: 0, 1: 1}}}}, 1: {'marital': {0: 0, 1: {'loan': {0: None, 2: 0}}, 2: 0}}}}, 1: 0, 2: 0}}, 3: 0, 5: {'housing': {0: {'default': {0: {'y': {0: 0, 1: 1}}, 1: 0}}, 2: 0}}, 6: {'default': {0: 0, 1: 1}}, 7: {'default': {0: 0, 1: {'loan': {0: {'marital': {1: {'housing': {0: 1, 2: 0}}, 2: 0}}, 2: 0}}}}}}, 2: {'education': {0: 0, 1: 0, 2: 0, 3: 0, 5: 0, 6: {'housing': {0: 0, 2: {'marital': {0: 0, 1: {'y': {0: 0, 1: 1}}, 2: 0}}}}, 7: 0}}, 3: {'education': {0: {'loan': {0: 0, 2: {'y': {0: 0, 1: 1}}}}, 1: 0, 2: 0, 3: 0, 5: 0, 6: 0, 7: 1}}, 4: {'education': {0: 0, 1: 0, 2: {'marital': {0: 0, 1: {'default': {0: 0, 1: 1}}, 2: 0}}, 3: 0, 5: 0, 6: 0, 7: 0}}, 5: {'education': {0: {'default': {0: 0, 1: {'housing': {0: 1, 1: 0, 2: 0}}}}, 1: 0, 2: 0, 3: 0, 5: 0, 6: 0}}, 6: 0, 7: {'housing': {0: 0, 1: 0, 2: {'education': {0: 1, 2: 0, 3: {'marital': {0: 0, 1: {'loan': {0: {'default': {0: None, 1: None}}, 2: 0}}, 2: 0}}, 5: 0, 7: 0}}}}, 8: 0, 9: {'education': {0: 0, 1: 0, 2: 0, 3: 0, 5: {'marital': {0: 0, 1: {'default': {0: {'loan': {0: {'housing': {0: None, 2: None}}, 1: 0, 2: 0}}, 1: 0}}, 2: 0}}, 6: {'loan': {0: {'default': {0: {'housing': {0: 0, 2: {'marital': {1: None, 2: 0}}}}, 1: {'marital': {1: 0, 2: {'y': {0: 0, 1: 1}}}}}}, 2: 0}}, 7: 0}}, 10: 0, 11: 0}}}}, 7: {'job': {0: {'education': {1: 0, 2: 0, 3: {'housing': {0: 0, 1: 0, 2: {'marital': {0: {'y': {0: 0, 1: 1}}, 1: {'contact': {0: {'default': {0: {'y': {0: 0, 1: 1}}, 1: 0}}, 1: 0}}, 2: 0}}}}, 5: 0, 6: {'marital': {0: 0, 1: 0, 2: {'housing': {0: {'y': {0: 0, 1: 1}}, 1: 0, 2: 0}}}}, 7: 0}}, 1: {'education': {0: 0, 1: {'marital': {0: 0, 1: 0, 2: {'contact': {0: 1, 1: 0}}}}, 2: 0, 3: 0, 5: 0, 7: 0}}, 2: {'education': {0: 0, 2: 0, 3: 0, 5: {'housing': {0: 1, 2: 0}}, 6: {'marital': {0: 0, 1: {'default': {0: {'housing': {0: 0, 2: {'loan': {0: {'contact': {0: None, 1: 0}}, 2: 0}}}}, 1: 0}}, 2: 0}}}}, 3: {'education': {0: {'marital': {0: 0, 1: 1}}, 2: 0, 3: 1, 6: {'marital': {0: 1, 1: 0}}, 7: 0}}, 4: {'housing': {0: 0, 2: {'education': {0: 0, 1: 0, 2: 0, 3: 0, 6: {'marital': {1: {'loan': {0: 0, 2: {'y': {0: 0, 1: 1}}}}, 2: {'loan': {0: {'y': {0: 0, 1: 1}}, 2: 0}}}}}}}}, 5: {'education': {0: {'housing': {0: 0, 2: 1}}, 2: 0, 3: 0, 5: 0, 6: 0}}, 6: 0, 7: 0, 8: {'education': {3: {'contact': {0: {'y': {0: 0, 1: 1}}, 1: 0}}, 5: 0, 6: 0, 7: 0}}, 9: {'loan': {0: {'education': {1: 0, 2: 0, 3: {'marital': {0: 0, 1: {'housing': {0: {'y': {0: 0, 1: 1}}, 2: 0}}, 2: 0}}, 5: {'housing': {0: 0, 2: {'marital': {0: 0, 1: {'y': {0: 0, 1: 1}}, 2: {'default': {0: {'y': {0: 0, 1: 1}}, 1: 0}}}}}}, 6: {'housing': {0: 0, 2: {'marital': {0: 0, 1: {'default': {0: {'y': {0: 0, 1: 1}}, 1: 0}}, 2: {'y': {0: 0, 1: 1}}}}}}}}, 2: 0}}, 10: {'education': {0: 0, 1: 0, 2: 0, 3: 0, 5: 1, 6: {'loan': {0: {'y': {0: 0, 1: 1}}, 1: 0, 2: 0}}, 7: 0}}}}, 8: {'job': {0: {'marital': {0: 0, 1: {'housing': {0: 1, 2: 0}}, 2: {'education': {3: 0, 6: {'housing': {0: {'y': {0: 0, 1: 1}}, 2: 1}}}}}}, 1: {'loan': {0: 0, 1: 0, 2: 1}}, 3: 0, 5: {'marital': {0: 1, 1: {'loan': {0: 0, 2: 1}}, 2: 0}}, 6: 0, 7: 0, 8: 1, 9: {'housing': {0: {'default': {0: {'loan': {0: {'contact': {0: 0, 1: 1}}, 2: 0}}, 1: 1}}, 2: 0}}, 10: 0}}, 9: {'job': {0: {'marital': {1: {'education': {3: 0, 6: {'loan': {0: {'contact': {0: {'y': {0: 0, 1: 1}}, 1: 0}}, 2: 0}}}}, 2: 0}}, 1: 0, 3: {'marital': {0: 0, 2: 1}}, 4: {'marital': {1: {'housing': {0: 0, 2: 1}}, 2: 0}}, 5: 1, 6: 0, 7: {'marital': {1: 0, 2: 1}}, 9: {'marital': {1: 0, 2: 1}}, 10: {'housing': {0: 1, 2: 0}}}}}}, 2: {'job': {0: {'month': {0: 1, 1: {'contact': {0: {'education': {3: {'marital': {0: {'y': {0: 0, 1: 1}}, 1: 1, 2: 1}}, 6: {'housing': {0: {'loan': {0: {'y': {0: 0, 1: 1}}, 2: 0}}, 2: {'marital': {1: 1, 2: {'y': {0: 0, 1: 1}}}}}}}}, 1: 1}}, 2: 1, 3: {'education': {3: 1, 5: 0, 6: 0}}, 4: 1, 5: 1, 6: {'education': {3: 0, 6: {'y': {0: 0, 1: 1}}}}, 7: {'marital': {0: 1, 1: {'housing': {0: {'education': {5: 1, 6: 0}}, 2: 1}}, 2: {'education': {3: 0, 6: {'loan': {0: 1, 2: 0}}}}}}, 8: {'housing': {0: 0, 2: 1}}, 9: {'housing': {0: 1, 2: 0}}}}, 1: {'education': {0: 0, 1: 1, 2: {'month': {2: 0, 5: 1, 6: {'housing': {0: 0, 2: 1}}, 7: 1}}, 3: {'month': {5: 1, 6: 0, 7: 1}}}}, 2: 0, 3: 1, 4: {'month': {0: 1, 1: {'education': {6: 0, 7: 1}}, 2: 0, 3: {'marital': {1: 1, 2: 0}}, 4: 1, 6: 1, 7: 0, 9: 1}}, 5: {'month': {0: 0, 1: {'education': {3: 0, 5: 1}}, 4: {'education': {3: 0, 5: 1}}, 5: 1, 6: 1, 7: 1, 8: {'education': {0: 0, 3: 1}}, 9: {'education': {0: 0, 7: 1}}}}, 6: {'month': {9: 1, 4: 1, 6: 1, 7: 0}}, 7: 1, 8: {'month': {9: 1, 3: 1, 6: 0, 1: 0}}, 9: {'month': {1: {'marital': {1: {'housing': {0: 1, 2: 0}}, 2: 1}}, 3: {'education': {5: 0, 6: 1, 7: 0}}, 4: {'education': {5: 1, 6: 0}}, 5: 1, 6: {'education': {3: 0, 6: 1}}, 7: {'loan': {0: 1, 2: 0}}, 9: 1}}, 10: {'education': {0: 0, 2: 1, 3: 1, 5: 1, 6: 1}}, 11: 0}}}}

```



### 样例数据测试

```
样例数据1: 
	工作类型: 白领
	是否结婚: 已婚
	教育层度: 研究生
	是否有住房贷款: 否
	是否有个人贷款: 是
	联系方式: 移动电话
	上一次营销联系是哪一个月: 3月
	上次营销活动结果: 成功
	
---> 本次是否成功: 否
```

```
样例数据2: 
	工作类型: 白领
	是否结婚: 已婚
	教育层度: 研究生
	是否有住房贷款: 否
	是否有个人贷款: 是
	联系方式: 移动电话
	上一次营销联系是哪一个月: 3月
	上次营销活动结果: 成功
---> 本次是否成功: 是 
```

## 模型评估

![image-20191110215238836](/home/kongweikun/.config/Typora/typora-user-images/image-20191110215238836.png)



ROC曲线是与二元分类器一起使用的另一种常用工具。 虚线表示纯随机分类器的ROC曲线; 一个好的分类器尽可能远离该线（朝左上角）,所以本次的模型的是一个相比而言很好的模型

## 总结

![image-20191110215314522](/home/kongweikun/.config/Typora/typora-user-images/image-20191110215314522.png)

在影响显著的月份中 五月、七月对成功营销存在负面影响，三月、九月、十月、十二月对成功营销有促进作用

![image-20191110215333150](/home/kongweikun/.config/Typora/typora-user-images/image-20191110215333150.png)

之前营销成功此次再次成功的比例达到64%，说明之前成功营销对此次能够顺利推销产品有重要影响

银行需要作如下的调整:

1. 建立激励客户忠诚和约束客户流失的机制

2. 维护与客户之间的关系
   1. 提高服务质量,及其独一无二性
   2.  建立客户分类信息系统
   3. 不同教育程度,婚姻状况的等对营销的成功率有影响,所以营销时注意划分群体
3. 注意电话营销的技巧 


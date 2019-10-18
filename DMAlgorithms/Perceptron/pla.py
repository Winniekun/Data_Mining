"""
@time : 2019/10/17下午6:42
@Author: kongwiki
@File: pla.py
@Email: kongwiki@163.com
"""
import numpy as np


def makeLinearSpeparableData(weights, numLines):
	w = np.array(weights)
	numFeatures = len(weights)
	dataSet = np.zeros((numLines, numFeatures + 1))
	for i in range(numLines):
		x = np.random.rand(1, numFeatures) * 20 - 10
		innerProduct = sum(w * x)
		if innerProduct <= 0:
			dataSet[i] = np.append(x, -1)
		else:
			dataSet[i] = np.append(x, 1)
	return dataSet




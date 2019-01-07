''' 
@author: kongwiki
@file:   visualize.py
@time:   19-1-7下午6:54
@contact: kongwiki@163.com
'''

"""
决策树可视化

"""

from sklearn.datasets import load_iris

iris = load_iris()
print("feature为：", iris.feature_names)
print("target为：", iris.target_names)
print("data example:", iris.data[1])
print("target:", iris.target[0])
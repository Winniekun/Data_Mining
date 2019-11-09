"""
@time : 2019/11/9下午7:42
@Author: kongwiki
@File: unitest.py
@Email: kongwiki@163.com
"""
import InAction.Bank.decisionTree as tree
import InAction.Bank.treePlotter as tp

myDat, labels = tree.createDataSet()
print("=====================================")
print(myDat)
print(labels)
print("=====================================")
# tp.createPlot()
print("=====================================")
# print(tp.retrieveTree(1))
# myTree = tp.retrieveTree(1)
# print(tp.getNumLeafs(myTree))
# print(tp.getTreeDepth(myTree))
print("=====================================")
myTree = tp.retrieveTree(0)
tp.createPlot(myTree)
myTree['no surfacing'][3] = 'maybe'
tp.createPlot(myTree)
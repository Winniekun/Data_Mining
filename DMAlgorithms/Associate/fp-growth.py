'''
@author：KongWeiKun
@file: fp-growth.py
@time: 18-5-17 下午5:32
@contact: kongwiki@163.com
'''
"""
fp-growth算法
"""

def loadSimpDat():
    simpDat = [['r','z','h','j','p'],
               ['z','y','x','w','v','u','t','s'],
               ['z'],
               ['r','x','n','o','s'],
               ['y','r','x','z','q','t','p'],
               ['y','z','x','e','q','s','t','m']]
    return simpDat

def createInitSet(dataset):
    retDict = {}
    for trans in dataset:
        #集合不可更改 无add remove方法
        retDict[frozenset(trans)] = 1
    return retDict

class treeNode:

    def __init__(self,nameValue,numOccur,parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None # 链接相似的元素
        self.parent = parentNode # #指向父节点
        self.children = {}

    def inc(self, numOccur):
        """
         count增加值
        :param numOccur: 
        :return: 
        """
        self.count += numOccur

    def disp(self, ind=1):
        """
        将树以文本的形式展示
        :param ind: 
        :return: 
        """
        print('  '*ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind+1)

def createTree(dataset,minSup=1):
    """
    fp树构建
    :param minSup: 最小支持度
    :return: 
    """
    headerTable = {} # 头指针表
    for trans in dataset:
        for item in trans:
            # 统计每个元素的次数
            headerTable[item] = headerTable.get(item,0) + 1
    #筛选符合最小支持度的元素
    # 需要将字典的键list化 否者会报错
    for k in list(headerTable.keys()):
        if headerTable[k] < minSup:
            del (headerTable[k])
    print(headerTable)
    freqItemSet = set(headerTable.keys())
    if not freqItemSet:
        return None,None
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]
        print(headerTable)
    # retTree = treeNode('Null Set', 1, None)
    # for tranSet, count in dataset.items():
    #     localD = {}
    #     for item in tranSet:
    #         if item in freqItemSet:
    #             localD[item] = headerTable[item][0]
    #     if len(localD) > 0:
    #         orderedItems = [v[0] for v in sorted(localD.items(),
    #                                              key=lambda p:p[1],
    #                                              reverse=True)]
    #         updateTree(orderedItems,retTree,headerTable,count)
    # return retTree,headerTable

def updateTree(items,inTree,headerTable,count):
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else:
        inTree.children[items[0]] = treeNode(items[0],count,inTree)
        if headerTable[items[0][1]] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateTree(headerTable[items[0]][1],
                       inTree.children[items[0]])
    if len(items) > 1:
        updateTree(items[1::],inTree.children[items[0]],headerTable,count)

def updateHeader(nodeToTest,targetNode):
    while(nodeToTest.targetNode != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


if __name__ == '__main__':
    # rootNode = treeNode('pyr',9,None)
    print('---------------------')
    # rootNode.disp()
    # rootNode.children['eye'] = treeNode('eye',13,None)
    print('---------------------')
    # rootNode.disp()
    # rootNode.children['pho'] = treeNode('pho',15,None)
    print('---------------------')
    # rootNode.disp()
    print('---------------------')
    simpDat = loadSimpDat()
    # print(simpDat)
    print('---------------------')
    initSet = createInitSet(simpDat)
    # print(initSet)
    createTree(initSet,3)


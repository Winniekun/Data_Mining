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
    :type minSup: 最小支持度
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
    freqItemSet = set(headerTable.keys())
    if not freqItemSet:
        return None,None
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]
    # 创建根节点
    retTree = treeNode('Null Set', 1, None)
    for tranSet, count in dataset.items():
        localD = {}
        # 重新整理数据表 排除不符合频繁一项集的数据
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        # print('local',localD)
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(),
                                                 key=lambda p:p[1],
                                                 reverse=True)]
            # print('整理之后的项集',orderedItems)
            updateTree(orderedItems,retTree,headerTable,count)
    return retTree,headerTable

def updateTree(items,inTree,headerTable,count):
    """
    更新树
    :type items:项集 
    :type inTree:目前的树 
    :type headerTable:头指针表 
    :type count:每个元素的次数 
    :rtype: 
    """
    # print('传入的项集',items)
    # inTree.disp()
    # 判断第一个元素是否作为子节点存在
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else:
        inTree.children[items[0]] = treeNode(items[0],count,inTree)
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1],
                       inTree.children[items[0]])
    if len(items) > 1:
        updateTree(items[1::],inTree.children[items[0]],headerTable,count)

def updateHeader(nodeToTest,targetNode):
    while(nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode

def ascendTree(leafNode,prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent,prefixPath)

def findPrefixPath(basePat,treeNode):
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode,prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats

def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(),key=lambda p:p[0])]
    # print(bigL)
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat,headerTable[basePat][1])
        myCondTree, myHead = createTree(condPattBases,minSup)

        if myHead != None:
            print('conditional tree for: ',newFreqSet)
            myCondTree.disp(1)
            mineTree(myCondTree,myHead,minSup,newFreqSet,freqItemList)



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
    tree,headerTable = createTree(initSet,3)
    # print(headerTable['x'][1].disp())
    # print(findPrefixPath('x',headerTable['x'][1]))
    print('---------------------')
    freqItems = []
    print(mineTree(tree,headerTable,3,set([]),freqItems))



'''
@author：KongWeiKun
@file: HierarchicalClustering.py
@time: 18-4-27 下午5:53
@contact: kongwiki@163.com
'''

"""
层次聚类
"""
from queue import PriorityQueue
import math


def getMedian(alist):
    """计算中位数"""
    tmp = list(alist)
    tmp.sort()
    alen = len(tmp)
    if (alen % 2) == 1:
        return tmp[alen // 2]
    else:
        return (tmp[alen // 2] + tmp[(alen // 2) - 1]) / 2


def normalizeColumn(column):
    """计算修正标准分"""
    median = getMedian(column)
    asd = sum([abs(x - median) for x in column]) / len(column)
    result = [(x - median) / asd for x in column]
    return result


class hClusterer:
    """该聚类器默认第一列是标签其他列是数值型的特征"""

    def __init__(self, filename):
        file = open(filename)
        self.data = {}
        self.counter = 0
        self.queue = PriorityQueue()
        lines = file.readlines()
        file.close()
        header = lines[0].split(',')
        self.cols = len(header)
        self.data = [[] for i in range(len(header))]
        for line in lines[1:]:
            cells = line.split(',')
            toggle = 0
            for cell in range(self.cols):
                if toggle == 0:
                    self.data[cell].append(cells[cell])
                    toggle = 1
                else:
                    self.data[cell].append(float(cells[cell]))
        # 标准化特征列（第一行跳过）
        for i in range(1, self.cols):
            self.data[i] = normalizeColumn(self.data[i])

        ###
        ###  对每条数据的操作步骤
        ###     1. 计算该分类和其他分类的距离，比如当前是1，
        ###  它和下标为2及下标为3的分类之间的距离用以下形式表示：
        ### {2:((1,2),1.23),3:((1,3),2.3)...}
        ###
        ###
        ###
        ###     2. 找出距离最近的分类
        ###
        ###     3. 将该分类插入到优先队列中



        # 插入队列
        rows = len(self.data[0])
        for i in range(rows):
            minDistance = 99999
            nearestNeighbor = 0
            neighbors = {}
            for j in range(rows):
                if i != j:
                    dist = self.distance(i, j)
                    if i < j:
                        pair = (i, j)
                    else:
                        pair = (j, i)
                    neighbors[j] = (pair, dist)
                    if dist < minDistance:
                        minDistance = dist
                        nearestNeighbor = j
                        nearestNum = j
            # 记录这两个分类的配对信息
            if i < nearestNeighbor:
                nearestPair = (i, nearestNeighbor)
            else:
                nearestPair = (nearestNeighbor, i)

            # 插入优先队列
            self.queue.put((minDistance, self.counter,
                            [[self.data[0][i]], nearestPair, neighbors]))
            self.counter += 1

    def distance(self, i, j):
        sumSquares = 0
        for k in range(1, self.cols):
            sumSquares += (self.data[k][i] - self.data[k][j]) ** 2
        return math.sqrt(sumSquares)

    def cluster(self):
        done = False
        while not done:
            topOne = self.queue.get()
            nearestPair = topOne[2][1]
            if not self.queue.empty():
                nextOne = self.queue.get()
                nearPair = nextOne[2][1]
                tmp = []
                ##
                ##  从队列中取出两个元素：1,2
                ##  检查两个分类是否是一对，若不是继续从优先队列中取出元素
                ##  直到找到1的配对为止
                ##

                while nearPair != nearestPair:
                    tmp.append((nextOne[0], self.counter, nextOne[2]))
                    self.counter += 1
                    nextOne = self.queue.get()
                    nearPair = nextOne[2][1]
                ##不处理的元素退回给优先队列
                ##
                for item in tmp:
                    self.queue.put(item)

                if len(topOne[2][0]) == 1:
                    item1 = topOne[2][0][0]
                else:
                    item1 = topOne[2][0]
                if len(nextOne[2][0]) == 1:
                    item2 = nextOne[2][0][0]
                else:
                    item2 = nextOne[2][0]
                ##  curCluster即合并后的分类
                curCluster = (item1, item2)

                ## 对于新的分类需要做两件事情：1.找到离它最近的分类然后合并距离字典
                ## 使用单链聚类
                minDistance = 99999
                nearestPair = ()
                nearestNeighbor = ''
                merged = {}
                nNeighbors = nextOne[2][2]
                for (key, value) in topOne[2][2].items():
                    if key in nNeighbors:
                        if nNeighbors[key][1] < value[1]:
                            dist = nNeighbors[key]
                        else:
                            dist = value
                        if dist[1] < minDistance:
                            minDistance = dist[1]
                            nearestPair = dist[0]
                            nearestNeighbor = key
                        merged[key] = dist

                if merged == {}:
                    return curCluster
                else:
                    self.queue.put((minDistance, self.counter,
                                    [curCluster, nearestPair, merged]))
                    self.counter += 1


def printDendrogram(T, sep=3):
    """打印二叉树 是的每个节点是一个二元组 摘自
    http://code.activestate.com/recipes/139422-dendrogram-drawing/ """

    def isPair(T):
        return type(T) == tuple and len(T) == 2

    def maxHeight(T):
        if isPair(T):
            h = max(maxHeight(T[0]), maxHeight(T[1]))
        else:
            h = len(str(T))
        return h + sep

    activeLevels = {}

    def traverse(T, h, isFirst):
        if isPair(T):
            traverse(T[0], h - sep, 1)
            s = [' '] * (h - sep)
            s.append('|')
        else:
            s = list(str(T))
            s.append(' ')

        while len(s) < h:
            s.append('-')

        if (isFirst >= 0):
            s.append('+')
            if isFirst:
                activeLevels[h] = 1
            else:
                del activeLevels[h]

        A = list(activeLevels)
        A.sort()
        for L in A:
            if len(s) < L:
                while len(s) < L:
                    s.append(' ')
                s.append('|')

        print(''.join(s))

        if isPair(T):
            traverse(T[1], h - sep, 0)

    traverse(T, maxHeight(T), -1)



filename = '/home/kongweikun/PycharmProjects/Data_Mining/data/DMGuideBook/cluster/cereal.csv'

hg = hClusterer(filename)
cluster = hg.cluster()
printDendrogram(cluster)
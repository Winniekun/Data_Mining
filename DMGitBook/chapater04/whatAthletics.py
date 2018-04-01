'''
@author：KongWeiKun
@file: whatAthletics.py
@time: 18-4-1 上午10:15
@contact: kongwiki@163.com
'''
class Classifier:

    def __init__(self,filename):
        self.medianAndDeviation = []
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
                    vector.append(int(fields[i]))
                elif self.format[i] == 'comment':
                    ignore.append(fields[i])
                elif self.format[i] == 'class':
                    classification = fields[i]
            self.data.append((classification,vector,ignore))

        self.vlen = len(self.data[0][1])
        for i in range(self.vlen):
            self.normalizeColumns(i)

    def getMedian(self,alist):
        """返回中位数"""
        if not alist:
            return []
        alist = sorted(alist)
        length = len(alist)
        if length % 2 == 1:
            return alist[int(length-1)//2]
        else:
            v1 = alist[int(length //2 )]
            v2 = alist[int(length //2 )-1]
            return (v1+v2)/2

    def getAbsoluteStandardDeviation(self,alist,median):
        """计算绝对值偏差"""
        sum = 0
        for item in alist:
            sum += abs(item-median)
        return sum/len(alist)

    def normalizeColumns(self,columnNumber):
        """标准化self.data中的columnNumber列"""
        col = [v[1][columnNumber] for v in self.data]
        median = self.getMedian(col)
        asd = self.getAbsoluteStandardDeviation(col,median)
        self.medianAndDeviation.append((median,asd))
        for v in self.data:
            v[1][columnNumber] = (v[1][columnNumber] - median) /asd

    def normalizeVector(self,v):
        """通过中位数和绝对偏差，标准化向量v"""
        vector = list(v)
        for i in range(len(vector)):
            (median,asd) = self.medianAndDeviation[i]
            vector[i] = (vector[i] - median)/asd
        return vector

    def manhattan(self,vector1,vector2):
        """计算曼哈顿距离"""
        return sum(map(lambda v1,v2:abs(v1-v2),vector1,vector2))

    def nearestNeighboor(self,itemVector):
        """返回itemVector的近邻"""
        return min([(self.manhattan(itemVector,item[1]), item)
                    for item in self.data])

    def classify(self,itemVector):
        """预测itemVector的分类"""
        return self.nearestNeighboor(self.normalizeVector(itemVector))[1][0]


def unitTest():
    filename = '../../data/DMGuideBook/sort/athletesTrainingSet.txt'
    classifier = Classifier(filename)
    print(classifier.medianAndDeviation)
    print(classifier.classify([70,140]))

def fileTest(training_filename,test_filename):
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
            # it is correct
            numCorrect += 1
            prefix = '+'
        print("%s  %12s  %s" % (prefix, theClass, line))
    print("%4.2f%% correct" % (numCorrect * 100 / len(lines)))

if __name__ == '__main__':
    trainingfilename = '../../data/DMGuideBook/sort/athletesTrainingSet.txt'
    testfilename = '../../data/DMGuideBook/sort/athletesTestSet.txt'
    fileTest(trainingfilename, testfilename)
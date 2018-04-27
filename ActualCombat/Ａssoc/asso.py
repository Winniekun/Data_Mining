from collections import Counter
import itertools

file = '../../data/basket.txt'
MINSUPPORTPCT = 31
allCustome = [] # 所有的商品
allSingletonTags = [] # 符合阀值的单项标签
allDoubletonTags = set() # 符合阀值的二元标签
doubletonSet = set() # 符合阀值的二元标签组合
allTripletonTags = set() # 符合阀值的三元标签
tripletonSet = [] # 符合阀值的三元标签组合
allQuadrupletonTags = set() # 符合阀值的四元标签
quadrupletonSet = [] # 符合阀值的四元标签组合
basketCustome = {} #篮子+商品
customeCount ={} #商品在每个篮子中出现的次数
baskets = 0 #篮子
custom = []
with open(file) as f:
    lines = f.readlines()
    striptext = [line.replace('\n\n', ' ') for line in lines]
    striptext = [s.replace('\n', ' ') for s in striptext]
    striptext = [s.replace('\t', ' ') for s in striptext]
    striptext = ["".join(s) for s in striptext]

for l in striptext:
    baskets += 1
    arr = l.split(" ")
    #商品
    for singleton in arr:
        if singleton:
            custom.append(singleton)
            basketCustome.setdefault(baskets,[])
            basketCustome[baskets].append(singleton)
            if singleton not in allCustome :
                allCustome.append(singleton)
print("共有{}个商品".format(len(allCustome)))
print("共记录{}个商品".format(len(custom)))
print("商品分别为",allCustome)
print("共有{}个篮子".format(baskets))
minsupport = baskets*(MINSUPPORTPCT/100)
print("最小支持度为{}".format(minsupport))
shoping = Counter(custom)
print("商品统计",shoping)
for k,v in shoping.items():
    if v > minsupport:
        allSingletonTags.append(k)
print("符合最小支持度的频繁一项标签项{}".format(allSingletonTags))
#寻找频繁二项集
def findDoubletons():
    print("=======================")
    print("二项集搜寻")
    print("=======================")
    doubleCandiates =  list(itertools.combinations(allSingletonTags,2))
    for index,candiate in enumerate(doubleCandiates):
        flag = 0
        count = 0
        tag1 = candiate[0]
        tag2 = candiate[1]
        for v in basketCustome.values():
            if tag2 and tag1 in v:
                count += 1
            else:
                flag = 1
        if  flag == 1:
            if count > minsupport:
                doubletonSet.add(candiate)
                allDoubletonTags.add(tag1)
                allDoubletonTags.add(tag2)
                # writeFile1(tag1,tag2,count,'two')
    print('频繁二项标签数量为',len(allDoubletonTags))
    print('频繁二项标签有',allDoubletonTags)
    print('频繁二项的组合', doubletonSet)

def fingTripletons():
    print("=======================")
    print("三项集搜寻")
    print("=======================")
    tripletonCandiates = list(itertools.combinations(allDoubletonTags,3))
    tripletonCandaitesSorted = []
    for tc in tripletonCandiates:
        tripletonCandaitesSorted.append(sorted(tc))
    for index,candiate in enumerate(tripletonCandaitesSorted):
        #考虑闭包属性
        doubletonsInsideTripleton = list(itertools.combinations(candiate,2))
        tripletonCandiateRejected = 0
        for index,doubleton in enumerate(doubletonsInsideTripleton):
            if doubleton not in doubletonSet:
                tripletonCandiateRejected = 1
                break
            if tripletonCandiateRejected == 0:
                flag = 0
                count = 0
                tag1 = candiate[0]
                tag2 = candiate[1]
                tag3 = candiate[2]
                for v in basketCustome.values():
                    if tag2 and tag1 and tag3  in v:
                        count += 1
                    else:
                        flag = 1
                if flag == 1:
                    if count > minsupport:
                        tripletonSet.append(candiate)
                        allTripletonTags.add(tag1)
                        allTripletonTags.add(tag2)
                        allTripletonTags.add(tag3)
                        # writeFile(tag1,tag2,tag3,count,'three')
    print('频繁三项标签数量为', len(allTripletonTags))
    print('频繁三项标签有', allTripletonTags)
    print('频繁三项组合有', tripletonSet)

def fingQuadrupletons():
    print("=======================")
    print("四项集搜寻")
    print("=======================")
    quadrupletonCandiates = list(itertools.combinations(allTripletonTags,4))
    quadrupleCandaitesSorted = []
    for tc in quadrupletonCandiates:
        quadrupleCandaitesSorted.append(sorted(tc))
    for (index,candiate) in enumerate(quadrupleCandaitesSorted):
        #考虑闭包属性
        tripletonsInsideQuadrupleTon = list(itertools.combinations(candiate,3))
        tripletonCandiateRejected = 0
        for index,tripleton in enumerate(tripletonsInsideQuadrupleTon):
            if tripleton not in doubletonSet:
                tripletonCandiateRejected = 1
                break
            if tripletonCandiateRejected == 0:
                flag = 0
                count = 0
                tag1 = candiate[0]
                tag2 = candiate[1]
                tag3 = candiate[2]
                tag4 = candiate[3]
                for v in basketCustome.values():
                    if tag2 and tag1 and tag3 and tag4  in v:
                        count += 1
                    else:
                        flag = 1
                if flag == 1:
                    if count > minsupport:
                        quadrupletonSet.append(candiate)
                        allQuadrupletonTags.add(tag1)
                        allQuadrupletonTags.add(tag2)
                        allQuadrupletonTags.add(tag3)
                        allQuadrupletonTags.add(tag4)
    print('频繁四项标签数量为', len(allQuadrupletonTags))
    print('频繁四项标签有', allQuadrupletonTags)
    print('频繁四项的组合',quadrupletonSet)

def generateRules():
    print("=======================")
    print("规则生成")
    print("=======================")
    with open('three.txt') as f:
        lines = f.readlines()
    for row in lines:
        arr = row.split(' ')
        tag1 = arr[0]
        tag2 = arr[1]
        tag3 = arr[2]
        ruleSupport = int(arr[3])
        print(ruleSupport)
        calsSCAV(tag1,tag2,tag3,ruleSupport)
        # calsSCAV(tag1,tag3,tag2,ruleSupport)
        # calsSCAV(tag2,tag3,tag1,ruleSupport)

def calsSCAV(tagA,tagB,tagC,ruleSupport):
    with open('two.txt') as f:
        lines = f.readlines()
    pairDict = {}
    for row in lines:
        arr = row.split(' ')
        tag1 = arr[0]
        tag2 = arr[1]
        tags = (tag1,tag2)
        pairDict.setdefault(tags,)
        pairDict[tags] = int(arr[2])
    # 支持度
    ruleSupportPct = round((ruleSupport/baskets),2)
    #置信度
    pairSupport = pairDict[(tagA,tagB)]
    confidence = round((ruleSupport/pairSupport),2)
    print(tagA,tagB,'--->',tagC,'[S=',ruleSupportPct,', C=',confidence,']')

def writeFile1(tag1,tag2,count,filename):
    with open(filename+'.txt','a') as f:
        f.write(tag1+' ')
        f.write(tag2+' ')
        f.write(str(count))
        f.write('\n')

def writeFile(tag1,tag2,tag3,count,filename):
    with open(filename+'.txt','a') as f:
        f.write(tag1+' ')
        f.write(tag2+' ')
        f.write(tag3 + ' ')
        f.write(str(count))
        f.write('\n')

if __name__ == '__main__':
    findDoubletons()
    fingTripletons()
    fingQuadrupletons()
    generateRules()

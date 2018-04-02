'''
@author：KongWeiKun
@file: knn.py
@time: 18-4-2 下午2:29
@contact: kongwiki@163.com
'''
import random

def buckets(filename,bucketName,separator,classColumn):
    """
    :type filename: 源文件名
    :type bucketName: 十个目标文件的前缀名
    :type separator: 分隔符
    :type classColumn: 数据所属分类的那一列的序号
    :rtype: 
    """
    numberOfBuckets = 10
    data = {}
    
    #读取数据
    with open(filename) as f:
        lines = f.readlines()
    for line in lines:
        if separator != '\t':
            line = line.replace(separator,'\t')

        #获取分类
        category = line.split()[classColumn]
        data.setdefault(category,[])
        data[category].append(line)

    #初始化分桶
    buckets = []
    for i in range(numberOfBuckets):
        buckets.append([])

    #将各个类别的数据均匀的放置桶中
    for k in data.keys():
        random.shuffle(data[k])
        bNum = 0
        #分桶
        for item in data[k]:
            buckets[bNum].append(item)
            bNum = (bNum + 1) % numberOfBuckets

    #写入文件
    for bNum in range(numberOfBuckets):
        f = open("%s-%02i" % (bucketName, bNum + 1), 'w')
        for item in buckets[bNum]:
            f.write(item)
        f.close()

buckets("pimaSmall.txt",'pimaSmall',',',8)
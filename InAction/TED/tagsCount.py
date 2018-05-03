'''
@author：KongWeiKun
@file: tagsCount.py
@time: 18-3-27 下午2:35
@contact: 836242657@qq.com
'''
"""
tags 统计
"""
import glob as gb
from collections import defaultdict, Counter


# import os
# _,filename = os.path.split('../../data/txt/9_11_healing_the_mothers_who_found_forgiveness_friendship.txt')
# print(filename)

# txt_path = gb.glob('../../data/txt//*')
# print(txt_path[3])
# 统计频率
def get_counts(sequence):
    counts = defaultdict(int)
    for x in sequence:
        counts[x] += 1
    return counts
#　tag转化为数字
def tagsMap(sequences):
    tagsMaps = {'technology': 0,
               'science': 1,
               'globalissues': 2,
               'culture': 3,
               'TEDx': 4,
               'design': 5,
               'business': 6,
               'society': 7,
               'entertainment': 8,
               'socialchange': 9}
    for l in sequences:
        if l[1] in tagsMaps:
            l[1] = tagsMaps[l[1]]
    return sequences
# year转化为数字
def yearMap(sequences):
    hours = {1984:0, 1990:1, 1991:2, 1994:3, 1998:4, 2001:5, 2002:6, 2003:7, 2004:8, 2005:9, 2006:10, 2007:11, 2008:12,
             2009:13, 2010:14, 2011:15, 2012:16, 2013:17, 2014:18, 2015:19, 2016:20, 2017:21, 2018:22}
    for l in sequences:
        if l[0] in hours:
            l[0] = hours[l[0]]
    return sequences

file = '../../data/year_tags_views.txt'
with open(file) as f:
    lines = f.readlines()
    lines = [line.strip('\n') for line in lines]
yearTags = dict()
tagSequences = []
for row in lines:
    arr = row.split('|')
    tags = arr[2].split(',')
    # print(year+" "+tags)
    for tag in tags:
        tagSequences.append(tag)

counts = get_counts(tagSequences)
arr = sorted(counts.items(),key=lambda x:x[1],reverse=True)[:10]
# 前10的topics
topCounts = [single[0] for single in arr]
print(topCounts)
for row in lines:
    arr = row.split('|')
    y = int(arr[0])
    tags = arr[-1].split(',')
    yearTags.setdefault(y,[])
    for tag in tags:
        if tag in topCounts:
            yearTags[y].append(tag)

totals = []
#　符合要求的数据格式
for k,v in yearTags.items():
    vCounts = get_counts(v)
    for k1,v1 in vCounts.items():
        single = [k,k1,v1]
        totals.append(single)
# 数据格式完全数字化
totals = tagsMap(totals)
totals = yearMap(totals)
print(totals)
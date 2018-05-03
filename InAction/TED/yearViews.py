'''
@author：KongWeiKun
@file: yearViews.py
@time: 18-3-31 上午11:59
@contact: kongwiki@163.com
'''
from collections import Counter

import pyecharts

file = '../../data/year_tags_views.txt'
yearViews = dict()
with open(file) as f :
    lines = [q.strip() for q in f.readlines()]
for l in lines:
    arr = l.split('|')
    year = int(arr[0])
    views = int(arr[1])
    yearViews.setdefault(year,[])
    yearViews[year].append(views)

count = dict()
for k,v in yearViews.items():
    info = {
        'max': max(v),
        'min': min(v),
        'ave': int((sum(v) / len(v))),
        'most': Counter(v).most_common(1)[0][0]
    }
    # print("{}年max{}most{}".format(k,max(v),Counter(v).most_common(1)[0][0]))
    count.setdefault(k,info)
sortInfo = sorted(count.items(),key=lambda x:x[0],reverse=False)
stackBar = pyecharts.Line('每年浏览量')
label = []
legend = ['max','min','ave','most']
maxSizes = []
minSizes = []
aveSizes = []
mostSizes = []
for row in sortInfo:
    label.append(row[0])
    maxSizes.append(row[1]['max'])
    minSizes.append(row[1]['min'])
    aveSizes.append(row[1]['ave'])
    mostSizes.append(row[1]['most'])
#
stackBar.add(legend[1],label,minSizes,is_smooth=True)
stackBar.add(legend[2],label,aveSizes,is_smooth=True)
stackBar.add(legend[3],label,mostSizes,is_smooth=True,mark_line=["average"])
stackBar.add(legend[0],label,maxSizes,is_datazoom_show=True,is_smooth=True)
stackBar.render('templates/{}.html'.format('line'))
'''
@author：KongWeiKun
@file: top10_tech.py
@time: 18-3-28 下午7:24
@contact: 836242657@qq.com
'''
import glob as gb
txt_path = gb.glob('../../../data/txt/*')
topic = 'technology'
tecPath = []
for i in txt_path:
    with open(i) as f:
        line = f.readline().strip('\n').split(',')
        if topic in line:
            tecPath.append(i)
        f.close()
# print(tecPath)
with open('../../../data/year_tags_views.txt') as f:
    row = f.readlines()
    row = [line.strip('\n') for line in row]
fd = dict()
for l in row:
    arr = l.split('|')
    views = arr[1]
    topics = arr[2]
    fd.setdefault(topics, [])
    fd[topics].append(views)
#
vie = {}
for path in tecPath:
    with open(path) as file:
        row = file.readline().strip('\n')
        if row in fd:
            vie.setdefault(path, [])
            vie[path].append("".join(fd[row][0]))
s = sorted(vie.items(), key=lambda x: x[1], reverse=False)[:10]
print(s)
#
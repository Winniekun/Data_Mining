'''
@author：KongWeiKun
@file: count.py
@time: 18-3-29 下午2:14
@contact: 836242657@qq.com
'''
with open('score.txt',encoding='utf-8') as f:
    year_score =[l.strip() for l in  f.readlines()]
grade = {}
for row in year_score:
    arr = row.split(' ')
    year = int(arr[0])
    score = float(arr[1])
    grade.setdefault(year,[])
    grade[year].append(score)
grade = sorted(grade.items(),key=lambda x:x[0],reverse=False)
total = []
for l in grade:
    for r in l[1]:
        t = [l[0],r]
        total.append(t)
x= []
y = []
for s in total:
    x.append(float(s[0]))
    y.append(s[1])
# print(x)
# print(y)
import matplotlib.pyplot as plt
plt.boxplot(y)
plt.savefig('/home/kongweikun/PycharmProjects/Data_Mining/ActualCombat/TED/img/box.png')
plt.show()
# import pyecharts
# scatter = pyecharts.Scatter('情感分析')
# scatter.add('',x,y,is_visualmap=True,is_datazoom_show=True,symbol_size=5)
# scatter.render('/home/kongweikun/PycharmProjects/Data_Mining/ActualCombat/TED/sentiment/templates/scatter.html')

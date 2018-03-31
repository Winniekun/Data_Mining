'''
@author：KongWeiKun
@file: year_txt.py
@time: 18-3-29 下午2:26
@contact: 836242657@qq.com
'''
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def writ_file(k,s):
    with open('score.txt','a') as f:
        f.write(str(k)+' '+str(s) +'\n')

with open('../../../data/year_tags_views.txt',encoding='utf-8') as f:
    full = [l.strip() for l  in f.readlines()]
tags_year = {}
year_path = {}
for row in full:
    arr = row.split('|')
    year = arr[0]
    tags = arr[2]
    tags_year.setdefault(tags, [])
    tags_year[tags].append(year)
import glob as gb
txt_path = gb.glob('../../../data/txt/*')
l = []
for i in txt_path:
    with open(i) as f:
        line = f.readline().strip('\n')
        if line in tags_year:
            year = "".join(tags_year[line][0])
            year_path.setdefault(year,[])
            year_path[year].append(i)
count = 0
for k,v in year_path.items():
    for path in v:
        count += 1
        with open(path, encoding='utf-8') as f:
            ubuntuLines = [line.strip() for line in f.readlines()[2:-1]]
        f.close()

        sid = SentimentIntensityAnalyzer()
        finalScore = 0
        for line in ubuntuLines:
            ss = sid.polarity_scores(line)
            score = ss['compound']
            finalScore = finalScore + score
            roundedFinalScore = round(finalScore / len(ubuntuLines), 4)
        print(count)
        print("score", roundedFinalScore)
        writ_file(k,roundedFinalScore)


'''
@author：KongWeiKun
@file: sentiment_test.py
@time: 18-3-29 下午1:37
@contact: 836242657@qq.com
'''
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import glob as gb


def writ_file(s):
    with open('score.txt','a') as f:
        f.write(str(s) +'\n')


txt_path = gb.glob('../../../data/txt//*')
txt_sore = []
i = 1
for l in txt_path:
    i += 1
    with open(l,encoding='utf-8') as f:
        ubuntuLines = [line.strip() for line in f.readlines()[2:-1]]
    f.close()

    sid  = SentimentIntensityAnalyzer()
    finalScore = 0
    for line in ubuntuLines:
        ss = sid.polarity_scores(line)
        score = ss['compound']
        finalScore = finalScore +score
        roundedFinalScore = round(finalScore/len(ubuntuLines),4)
    print(i)
    print("score",roundedFinalScore)
    writ_file(roundedFinalScore)


    # print(line)
    # ss = sid.polarity_scores(line)
    # for k in sorted(ss):
    #     print("{0}:{1}\n".format(k,ss[k]))

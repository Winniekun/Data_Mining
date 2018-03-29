'''
@author：KongWeiKun
@file: tf-idf.py
@time: 18-3-28 上午10:29
@contact: 836242657@qq.com
'''
import numpy as np
import glob as gb
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import  CountVectorizer
stop_words = stopwords.words('english')

def get_words(file):
    with open(file) as f:
        lines  = f.readlines()
        lines = [i.lower() for i in lines[2:-1]]
        striptext = [line.replace('\n\n',' ') for line in lines]
        striptext = [s.replace('\n',' ') for s in striptext]
    txt = "".join(striptext)
    words = nltk.word_tokenize(txt)
    # print(words)
    letter = [word for word in words
              if word not in stop_words and word.isalpha()]
    return letter

def wordlist(file):
    with open(base_path + file) as file:
        lines = file.readlines()[2:-1]
        lines = [i.lower() for i in lines]
        striptext = [line.replace('\n\n', ' ') for line in lines]
        striptext = [s.replace('\n', ' ') for s in striptext]
    txt = "".join(striptext)
    words = nltk.word_tokenize(txt)
    # print(words)
    letter = [word for word in words
              if word not in stop_words and word.isalpha()]
    txt = " ".join(letter)
    yield txt

def tfidf(txt):
    vectorizer = CountVectorizer()
    # 计算个词语出现的次数
    X = vectorizer.fit_transform(txt)
    # 获取词袋中所有文本关键词
    word = vectorizer.get_feature_names()
    # print(word)
    # 类调用
    transformer = TfidfTransformer()
    # print(transformer)
    # 将词频矩阵X统计成TF-IDF值
    tfidf = transformer.fit_transform(X)
    # 查看数据结构 tfidf[i][j]表示i类文本中的tf-idf权重
    weight = tfidf.toarray()
    wordWeight = []
    for i in range(len(weight)):
        # print("-------这里输出第",i,u"类文本的词语tf-idf权重------" )
        for j in range(len(word)):
            if weight[i][j] != 0.0:
                l = [word[j], weight[i][j]]
                wordWeight.append(l)
                # print(word[j],weight[i][j])

    return wordWeight

if __name__ == '__main__':
    import pyecharts
    # base_path = '../../data/txt/'
    # ll = []
    # with open('../../data/top10.txt') as f:
    #     row = f.readlines()
    #     arr = [ss.strip('\n') for ss in row]
    #     for l in arr:
    #         txt = wordlist(l)
    #         wordWeight = tfidf(txt)
    #         s = sorted(wordWeight,key=lambda x:x[1],reverse=True)[:3]
    #         ll.append(s)
    # print(ll)
    ll = [[['stuff', 0.44233918732073285]],
[['network', 0.30221302424344187]],
[['boys', 0.43515469193302975]],
[['universe', 0.48004267235639847]],
[['world', 0.26678657924332194]],
[['right', 0.35641846295458396]],
[['information', 0.27579849586805472]],
[['people', 0.43308190878605118]],
[['brain', 0.34786262139146906]],
[['cancer', 0.52024972856630003]]]
    pie = pyecharts.Pie('top10文章中的关键词')
    x = []
    y = []
    for s in ll:
        for l in s:
            print(s)
            x.append(l[0])
            y.append(l[1])
    pie.add('',x,y,is_random=True,legend_pos='right',legend_orient='vertical',radius=[20,75],rosetype='radius')
    pie.render('/home/kongweikun/PycharmProjects/Data_Mining/ActualCombat/TED/tf-idf/templates/{}.html'.format(0))





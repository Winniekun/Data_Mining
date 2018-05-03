'''
@author：KongWeiKun
@file: ted_wordcount.py
@time: 18-3-27 下午8:53
@contact: 836242657@qq.com
'''
import os
import jieba
import numpy as np
from PIL import Image
from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt
stopwords = STOPWORDS.copy()
stopwords.add('laughter')
stopwords.add('one')
def content(name):
    with open('../../data/{}.txt'.format(name),'rb') as f:
        text = f.read()
        return text
text = content(name='frequent')

backgroundImage =  np.array(Image.open("/home/kongweikun/PycharmProjects/Data_Mining/InAction/TED/img/ted.png"))

wordlist = jieba.cut(text,cut_all=False)
#cut_all True 为全局模式 False为精准模式
wordlist_space_split = ' '.join(wordlist)
wordcloud = WordCloud(
    width=960,
    height=896,
    stopwords = stopwords,
    background_color='white',  # 设置背景颜色
    max_words=5000,  # 设置最大现实的字数
    # max_font_size=400,  # 设置字体最大值
    mask=backgroundImage,
    random_state=20,  # 设置有多少种随机生成状态，即有多少种配色方案
).generate(wordlist_space_split)

plt.imshow(wordcloud)
plt.axis('off')                     # 关闭坐标轴
plt.show()

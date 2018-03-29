'''
@author：KongWeiKun
@file: wordsCounts.py
@time: 18-3-27 下午7:21
@contact: 836242657@qq.com
'''
import nltk
import glob as gb
import pprint
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
# print(stop_words)
def most_words(file):
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
    most_frequent_words = nltk.FreqDist(letter).most_common(20)
    return most_frequent_words

def write_file(frequent_words):
    with open('../../data/frequent.txt','a') as f:
        for word,score in frequent_words:
            f.write(word + '\n')


if __name__ == '__main__':
    txt_path = gb.glob('../../data/txt/*')
    for path in txt_path:
        s = most_words(path)
        print(s)
        write_file(s)



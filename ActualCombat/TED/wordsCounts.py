'''
@author：KongWeiKun
@file: wordsCounts.py
@time: 18-3-27 下午7:21
@contact: 836242657@qq.com
'''
import nltk
import pprint
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
# print(stop_words)
file = '/home/kongweikun/PycharmProjects/Data_Mining/data/txt/9_11_healing_the_mothers_who_found_forgiveness_friendship.txt'

candidte_sentences = {}
candidte_sentences_counts = {}
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
word_frequencies = nltk.FreqDist(letter)
most_frequent_words = nltk.FreqDist(letter).most_common(20)
print(most_frequent_words)
# sentences = nltk.sent_tokenize(txt)
# for sentence in sentences:
#     candidte_sentences[sentence] = sentence
#
# for long,short in candidte_sentences.items():
#     count = 0
#     for freq_word,frequency_score in most_frequent_words:
#         if  freq_word in short:
#             count += frequency_score
#             candidte_sentences_counts[long] = count
#
# sorted_sentences = nltk.OrderedDict(sorted(candidte_sentences_counts.items(),key=lambda x:x[1],reverse=True)[:4])
# print(sorted_sentences)
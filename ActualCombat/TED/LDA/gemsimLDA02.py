'''
@author：KongWeiKun
@file: gemsimLDA02.py
@time: 18-3-29 上午10:34
@contact: 836242657@qq.com
'''
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from gensim.parsing.preprocessing import  STOPWORDS
import pprint

def makeLDA(path,num_topics,num_words,passes):
    num_topics = num_topics  # 模型中寻找主题的数量
    num_words = num_words  # 从每个主题中看到多少单词
    passes = passes  # 重复检查数据多少次
    with open(path, encoding='utf-8') as f:
        documents = f.readlines()
        texts = [[word for word in document.lower().split()
                  if word not in STOPWORDS and word.isalnum()]
                 for document in documents]

    # print(texts)
    # 从单词列表中创建一个字典和一个语料库
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    lda = LdaModel(corpus,
                   id2word=dictionary,
                   num_topics=num_topics,
                   passes=passes)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(lda.print_topics(num_words=num_words))
    # unseennText = '../../../data/LDA_data/lkmlSingleNewEmail.txt'
    # with open(unseennText,encoding='utf-8') as fenw:
    #     newdoc = fenw.read()
    # newcourpus = dictionary.doc2bow(newword for newword in newdoc.lower().split()
    #                                 if newword  not in STOPWORDS and newword.isalnum())
    #
    # #将新的语料库传入现有的LDA模型
    # pp.pprint(lda[newcourpus])

if __name__ == '__main__':
    filename = '../../../data/LDA_data/lkmlLinusAll.txt'
    makeLDA(filename,num_topics=10,num_words=5,passes=1)
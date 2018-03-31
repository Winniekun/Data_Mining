'''
@author：KongWeiKun
@file: techTop1LDA.py
@time: 18-3-29 上午11:15
@contact: 836242657@qq.com
'''
import math
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
    dictionary.save('model/lkml.dict')
    corpus = [dictionary.doc2bow(text) for text in texts]
    lda = LdaModel(corpus,
                   id2word=dictionary,
                   num_topics=num_topics,
                   passes=passes)
    # lda.save('model/lkml.gensim')
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

def applyLDA(file_path,lda_path):
    unseennText = file_path
    lda = LdaModel.load(lda_path,mmap='r')
    dictionary = corpora.Dictionary.load('model/lkml.dict')
    with open(unseennText,encoding='utf-8') as fenw:
        newdoc = fenw.read()
    newcourpus = dictionary.doc2bow(newword for newword in newdoc.lower().split()
                                    if newword  not in STOPWORDS and newword.isalnum())
    pp = pprint.PrettyPrinter(indent=4)
    #将新的语料库传入现有的LDA模型
    pp.pprint(lda[newcourpus])



if __name__ == '__main__':
    base_path = '../../../data/txt/juan_enriquez_wants_to_grow_energy.txt'
    makeLDA(base_path,5,5,20)
    # lda_path = 'model/lkml.gensim'
    # pp = pprint.PrettyPrinter(indent=4)
    # lda = LdaModel.load(lda_path, mmap='r')
    # pp.pprint(lda.print_topics(num_words=5))
    # with open('../../../data/top10.txt') as f:
    #     row = f.readlines()
    #     arr = [ss.strip('\n') for ss in row]
    #     for l in arr:
    #         makeLDA(base_path+l,num_words=3,num_topics=1,passes=50)
                # applyLDA(base_path+l,lda_path=lda_path)

    # makeLDA(filename,num_topics=4,num_words=5,passes=100)
    # dictionary = corpora.Dictionary.load('model/lkml.dict')
    # print(dictionary)


# s  =[[(0, '0.014*"stuff" + 0.013*"oil" + 0.013*"think"')],
# [(0, '0.014*"new" + 0.013*"network" + 0.011*"people"')],
# [(0, '0.020*"boys" + 0.016*"need" + 0.013*"write"')],
# [(0, '0.020*"worldwide" + 0.020*"going" + 0.018*"think"')],
# [(0, '0.010*"world" + 0.009*"new" + 0.008*"people"')],
# [(0, '0.013*"science" + 0.013*"people" + 0.011*"like"')],
# [(0, '0.019*"ones" + 0.018*"looking" + 0.015*"code"')],
# [(0, '0.021*"people" + 0.011*"think" + 0.010*"things"')],
# [(0, '0.015*"brain" + 0.015*"look" + 0.013*"visual"')],
# [(0, '0.032*"cancer" + 0.028*"skeletal" + 0.026*"muscle"')]]
data = [{'name':'stuff','value':0.014},{'name':'oil','value':0.013},{'name':'think','value':0.013},
            {'name':'new','value':0.014},{'name':'network','value':0.013},{'people':'a','value':0.011},
            {'name':'boys','value':0.020},{'name':'need','value':0.016},{'name':'write','value':0.013},
            {'name':'worldwide','value':0.020},{'name':'going','value':0.020},{'name':'think','value':0.018},
            {'name':'world','value':0.010},{'name':'new','value':0.009},{'name':'people','value':0.008},
            {'name': 'science', 'value': 0.013}, {'name': 'people', 'value': 0.013}, {'name': 'like', 'value': 0.011},
            {'name':'ones','value':0.019},{'name':'looking','value':0.018},{'name':'code','value':0.015},
            {'name':'people','value':0.021},{'name':'think','value':0.011},{'name':'things','value':0.010},
            {'name': 'brain', 'value': 0.015}, {'name': 'look', 'value': 0.015}, {'name': 'visual', 'value': 0.013},
            {'name':'cancer','value':0.032},{'name':'skeletal','value':0.028},{'name':'muscle','value':0.026},
             ]
labelData = [{'name':'stuff','value':1},{'name':'oil','value':1},{'name':'think','value':1},
            {'name':'new','value':1},{'name':'network','value':1},{'name':'people','value':1},
            {'name':'boys','value':1},{'name':'need','value':1},{'name':'write','value':1},
            {'name':'worldwide','value':1},{'name':'going','value':1},{'name':'think','value':1},
            {'name':'world','value':1},{'name':'new','value':1},{'name':'people','value':1},
            {'name': 'science', 'value': 1}, {'name': 'people', 'value': 1}, {'name': 'like', 'value': 1},
            {'name':'ones','value':1},{'name':'looking','value':1},{'name':'code','value':1},
            {'name':'people','value':1},{'name':'think','value':1},{'name':'things','value':1},
            {'name': 'brain', 'value': 1}, {'name': 'look', 'value': 1}, {'name': 'visual', 'value': 1},
            {'name':'cancer','value':1},{'name':'skeletal','value':1},{'name':'muscle','value':1},
             ]
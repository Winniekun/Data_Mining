'''
@author：KongWeiKun
@file: tf-idf-test.py
@time: 18-3-28 下午3:48
@contact: 836242657@qq.com
'''
from sklearn.feature_extraction.text import  CountVectorizer,TfidfTransformer
vectorizer = CountVectorizer()
corpus = [
    'This is the first document.',
    'This is the second second document.',
    'And the third one.',
    'Is this the first document?',]
# 计算每个词语出现的次数
x = vectorizer.fit_transform(corpus)
# 获取关键词
print(vectorizer.get_feature_names())
# 查看词频结果
print(x.toarray())

transformer = TfidfTransformer()
print(transformer)
tfidf = transformer.fit_transform(x)
print(tfidf.toarray())


'''
@author：KongWeiKun
@file: test.py
@time: 18-3-24 上午9:54
@contact: 836242657@qq.com
'''
import re
data = '/home/kongweikun/PycharmProjects/Data_Mining/data/PA_chapter3_data/wine.names'
pattern = re.compile('.*[0-9]+\)\s?(\w+).*')
with open(data) as f:
    for l in f:
        if pattern.findall(l.strip()):
            print(pattern.findall(l.strip())[0])
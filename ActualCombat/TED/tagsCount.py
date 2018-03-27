'''
@author：KongWeiKun
@file: tagsCount.py
@time: 18-3-27 下午2:35
@contact: 836242657@qq.com
'''
"""
tags 统计
"""
import glob as gb
# import os
# _,filename = os.path.split('../../data/txt/9_11_healing_the_mothers_who_found_forgiveness_friendship.txt')
# print(filename)

txt_path = gb.glob('../../data/txt//*')
# print(txt_path[0])
with open(txt_path[100]) as f:
    tags = f.readline().strip("\n").split(',')
    print()




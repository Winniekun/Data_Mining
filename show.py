'''
@author：KongWeiKun
@file: show.py
@time: 18-4-10 下午8:09
@contact: kongwiki@163.com
'''
import matplotlib.font_manager as fm
myfont = fm.FontProperties(fname='/usr/local/share/fonts/msyh.ttf')

import matplotlib.pyplot as plt

plt.clf()  # 清空画布
plt.plot([1, 2, 3], [4, 5, 6])
plt.xlabel("横轴",fontproperties=myfont)
plt.ylabel("纵轴",fontproperties=myfont)
plt.title("pythoner.com",fontproperties=myfont)
plt.show()


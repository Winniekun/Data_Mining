'''
@author：KongWeiKun
@file: assoc.py
@time: 18-3-8 下午5:14
@contact: 836242657@qq.com
'''
"""
发现软件项目标签中的关联规则
apriori算法
计算篮子数量 使用最小阀值找出单例
"""
import itertools
import pymysql

#设置阀值百分比
MINSUPPORTPCT = 5
allSingletonTags = []
allDoubletonTags = set()
doubletonSet = []

#链接本地数据库
db = pymysql.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'Hanhuan.0214',
    db = 'ml',
    charset = 'utf8mb4')
cursor = db.cursor()

#计算篮子中的数量 - 数据库表中项目数
queryBaskets = "select count(distinct project_id) from fc_project_tags"
cursor.execute(queryBaskets)
baskets = cursor.fetchone()[0]

#使用篮子数和前面设置的最小支持阀值 计算篮子的最小数量
minsupport = baskets*(MINSUPPORTPCT/100)
print("Minimum support count:",minsupport,"(",MINSUPPORTPCT,"%of",baskets,")")



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
print(baskets)
#使用篮子数和前面设置的最小支持阀值 计算篮子的最小数量
minsupport = baskets*(MINSUPPORTPCT/100)
print("Minimum support count:",minsupport,"(",MINSUPPORTPCT,"%of",baskets,")")
#
# #得到最小支持阀值的标签
# cursor.execute("select distinct tag_name from fc_project_tags "
#                "GROUP by 1 HAVING COUNT(project_id) >=%s ORDER by tag_name",(minsupport))
# singletons = cursor.fetchall()
#
# for singleton in singletons:
#     allSingletonTags.append(singleton[0])
#
#
# def findDoubletons():
#     print("======")
#     print("Frequent doubletons found:")
#     print("======")
#     # use the list of allSingletonTags to make the doubleton candidates
#     doubletonCandidates = list(itertools.combinations(allSingletonTags, 2))
#     for (index, candidate) in enumerate(doubletonCandidates):
#         # figure out if this doubleton candidate is frequent
#         tag1 = candidate[0]
#         tag2 = candidate[1]
#         getDoubletonFrequencyQuery = "SELECT count(fpt1.project_id) \
#                                      FROM fc_project_tags fpt1 \
#                                      INNER JOIN fc_project_tags fpt2 \
#                                      ON fpt1.project_id = fpt2.project_id \
#                                      WHERE fpt1.tag_name = %s \
#                                      AND fpt2.tag_name = %s"
#         insertPairQuery = "INSERT INTO ml.fc_project_tag_pairs \
#                                 (tag1, tag2, num_projs) \
#                                 VALUES (%s,%s,%s)"
#         cursor.execute(getDoubletonFrequencyQuery, (tag1, tag2))
#         count = cursor.fetchone()[0]
#
#         # add frequent doubleton to database
#         if count > minsupport:
#             print(tag1, tag2, "[", count, "]")
#
#             cursor.execute(insertPairQuery, (tag1, tag2, count))
#
#             # save the frequent doubleton to our final list
#             doubletonSet.append(candidate)
#             # add terms to a set of all doubleton terms (no duplicates)
#             allDoubletonTags.add(tag1)
#             allDoubletonTags.add(tag2)
#
#
# def findTripletons():
#     print("======")
#     print("Frequent tripletons found:")
#     print("======")
#     # use the list of allDoubletonTags to make the tripleton candidates
#     tripletonCandidates = list(itertools.combinations(allDoubletonTags, 3))
#
#     # sort each candidate tuple and add these to a new sorted candidate list
#     tripletonCandidatesSorted = []
#     for tc in tripletonCandidates:
#         tripletonCandidatesSorted.append(sorted(tc))
#
#     # figure out if this tripleton candidate is frequent
#     for (index, candidate) in enumerate(tripletonCandidatesSorted):
#         # all doubletons inside this tripleton candidate MUST also be frequent
#         doubletonsInsideTripleton = list(itertools.combinations(candidate, 2))
#         tripletonCandidateRejected = 0
#         for (index, doubleton) in enumerate(doubletonsInsideTripleton):
#             if doubleton not in doubletonSet:
#                 tripletonCandidateRejected = 1
#                 break
#         # set up queries
#         getTripletonFrequencyQuery = "SELECT count(fpt1.project_id) \
#                                         FROM fc_project_tags fpt1 \
#                                         INNER JOIN fc_project_tags fpt2 \
#                                         ON fpt1.project_id = fpt2.project_id \
#                                         INNER JOIN fc_project_tags fpt3 \
#                                         ON fpt2.project_id = fpt3.project_id \
#                                         WHERE (fpt1.tag_name = %s \
#                                         AND fpt2.tag_name = %s \
#                                         AND fpt3.tag_name = %s)"
#         insertTripletonQuery = "INSERT INTO ml.fc_project_tag_triples \
#                                 (tag1, tag2, tag3, num_projs) \
#                                 VALUES (%s,%s,%s,%s)"
#         # insert frequent tripleton into database
#         if tripletonCandidateRejected == 0:
#             cursor.execute(getTripletonFrequencyQuery, (candidate[0],
#                                                         candidate[1],
#                                                         candidate[2]))
#             count = cursor.fetchone()[0]
#             if count > minsupport:
#                 print(candidate[0], ",",
#                       candidate[1], ",",
#                       candidate[2],
#                       "[", count, "]")
#                 cursor.execute(insertTripletonQuery,
#                                (candidate[0],
#                                 candidate[1],
#                                 candidate[2],
#                                 count))
#
#
# def generateRules():
#     print("======")
#     print("Association Rules:")
#     print("======")
#
#     # pull final list of tripletons to make the rules
#     getFinalListQuery = "SELECT tag1, tag2, tag3, num_projs \
#                    FROM msquire.fc_project_tag_triples"
#     cursor.execute(getFinalListQuery)
#     triples = cursor.fetchall()
#     for (triple) in triples:
#         tag1 = triple[0]
#         tag2 = triple[1]
#         tag3 = triple[2]
#         ruleSupport = triple[3]
#
#         calcSCAV(tag1, tag2, tag3, ruleSupport)
#         calcSCAV(tag1, tag3, tag2, ruleSupport)
#         calcSCAV(tag2, tag3, tag1, ruleSupport)
#         print("*")
#
#
# def calcSCAV(tagA, tagB, tagC, ruleSupport):
#     # Support
#     ruleSupportPct = round((ruleSupport / baskets), 2)
#
#     # Confidence
#     queryConf = "SELECT num_projs \
#               FROM msquire.fc_project_tag_pairs \
#               WHERE (tag1 = %s AND tag2 = %s) \
#               OR    (tag2 = %s AND tag1 = %s)"
#     cursor.execute(queryConf, (tagA, tagB, tagA, tagB))
#     pairSupport = cursor.fetchone()[0]
#     confidence = round((ruleSupport / pairSupport), 2)
#
#     # Added Value
#     queryAV = "SELECT count(*) \
#               FROM test.fc_project_tags \
#               WHERE tag_name= %s"
#     cursor.execute(queryAV, tagC)
#     supportTagC = cursor.fetchone()[0]
#     supportTagCPct = supportTagC / baskets
#     addedValue = round((confidence - supportTagCPct), 2)
#
#     # Result
#     print(tagA, ",", tagB, "->", tagC,
#           "[S=", ruleSupportPct,
#           ", C=", confidence,
#           ", AV=", addedValue,
#           "]")
#
#
#
# findDoubletons()
# findTripletons()
# generateRules()

# db.close()
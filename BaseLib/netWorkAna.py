"""
@time : 2019/10/8上午10:20
@Author: kongwiki
@File: netWorkAna.py
@Email: kongwiki@163.com
"""
import networkx as nx

G = nx.Graph()

# 添加节点
G.add_node(1)
G.add_nodes_from([2, 3])


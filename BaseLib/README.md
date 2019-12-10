## 网络分析

现实世界网络表达为图的一些方式

* 电子邮件

  节点可以是人，链接表示“向某人发邮件”，此为有向图

* Web

  节点可以是网页，边可以表示“包含一个指向该网页的URL“，也为有向图

  若是对页面A有多少个指向B页面的链接感兴趣，则为有向加权图。

* Facebook点赞

  节点是人，边是”在某人发表的内容上点赞“，为有向加权图

* Facebook好友

  节点是人，边可以是”与某人有好友关系“，Facebook好友是双向的，所以其可能是一个无向不加权图，若是希望为加权图，可以为链接添加一个值，例如共同好友数

### 网络计量

网络分析大部分工作时间上就是对其各个组成部分的计量。

1. 有多少个节点
2. 这些节点如何链接
3. 有多少条边
4. 有多少种方式进行遍历这些边

#### 网络的度数

无向图：节点的度数是和它相连的边数。

有向图： 入度，出度之分

#### 网络直径

图中两个节点的最大距离

距离的计算：链接对应的节点所需要的最小跳数

距离是两点之间的最短路径，直径为图上任意两点的最长距离，有时候称直径为`最长最短距离`

#### 网络中的通路、路径、迹

计量一个节点到另一个节点需要花费多长时间，有时候想限制实现这一路径时使用同一节点和边的次数

**通路**: 图中的通路，字面意思，就是遍历节点之间的链接

**路径**: 图中的路径，字面意思，点到点之间路径

**迹**: 图的迹遍历图时对每条链接最多使用一次，但是节点可以使用多次

#### 图的中心性

##### 接近中心性

一种方法为找出很容易接近许多其他节点的节点，计算接近中心性分为三个步骤

1. 算出网络中每对节点之间的最短路径距离
2. 对每个节点，计算它和所有其他节点的距离总和。
3. 网络的可能最小距离（节点数量-1）除以距离总和

##### 度中心性

该点的度除以图的总共节点数。

##### 中介中心性

是否有些节点是网络中不可缺少的，删除它们会导致图的不连通。其也可以称为桥、瓶颈、门卫、跨界者、中介

中介中心性越高，对于图的顺利运行越重要。

1. 计算网络上每对节点之间的最短路径，然后对每个节点计算有多少条网络最短路径包含该节点但是不至于该节点。
2. （节点数量-1）×（节点数量-2）/2
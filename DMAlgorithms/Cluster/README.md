## 聚类算法

#### 流程图

![image](https://raw.githubusercontent.com/KongWiki/Data_Mining/master/pic/kmeans.png)

**其步骤可简答的概括为**:

1. 分配：样本分配到簇
2. 移动： 移动聚类中心到簇中样本的平均位置

```
# 伪码
创建 k 个点作为起始质心（随机选择）
当任意一个点的簇分配结果发生改变时（不改变时算法结束）
    对数据集中的每个数据点
        对每个质心
            计算质心与数据点之间的距离
        将数据点分配到距其最近的簇
    对每一个簇, 计算簇中所有点的均值并将均值作为质心
```



#### 层次聚类

* 待完成

#### k-means

* 已经完成
  * [最基础版](https://github.com/KongWiki/Data_Mining/blob/master/DMAlgorithms/Cluster/kmeans.ipynb)
  * [优化版](https://github.com/KongWiki/Data_Mining/blob/master/DMAlgorithms/Cluster/kmeans.py)
* [讲解]([https://www.kongwiki.top/2019/08/24/k-means%e8%81%9a%e7%b1%bb%e7%ae%97%e6%b3%95/](https://www.kongwiki.top/2019/08/24/k-means聚类算法/))

#### k-means优化--- k-means ++

**核心优化**：

* 其主要是优化最初如何进行选点，从而能够最大程度的产生最佳结果



 


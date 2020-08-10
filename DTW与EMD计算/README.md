# 轨迹相似度计算
**轨迹的相似度包含时间相似度与空间相似度，空间相似度用DTW，时间相似度用EMD**

**1. 空间相似度计算**

![DTW示意图](https://github.com/zhoujian-hub/Tourism-Trip-Chain-Extraction-Based-on-Multi-Big-Data/blob/master/ImageStore/DTW示意图.png)

- 先计算每轨迹间任意两点的距离矩阵
- 在计算轨迹的累计距离矩阵，依据动态规划
- 累计距离矩阵的最后的点就是DTW距离


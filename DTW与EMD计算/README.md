# 轨迹相似度计算
**轨迹的相似度包含时间相似度与空间相似度，空间相似度用DTW，时间相似度用EMD**

**1. 空间相似度计算**

<div align=center><img src="https://github.com/zhoujian-hub/Tourism-Trip-Chain-Extraction-Based-on-Multi-Big-Data/blob/master/ImageStore/DTW示意图.png" width="520" height="250" /></div>

- 先计算每轨迹间任意两点的距离矩阵
- 在计算轨迹的累计距离矩阵，依据动态规划
- 累计距离矩阵的最后的点就是DTW距离

<div align=center><img src="https://github.com/zhoujian-hub/Tourism-Trip-Chain-Extraction-Based-on-Multi-Big-Data/blob/master/ImageStore/OptimalAlignment.png" width="400" height="200" /></div>

**2.时间相似度计算**

- 利用python中已有的集成函数计算scipy.stats中的EMD计算函数

**3.时空相似度衡量**

- 将DTW与EMD距离进行归一化，合成为一个指标，最后的轨迹相似的的效果如图

<div align=center><img src="https://github.com/zhoujian-hub/Tourism-Trip-Chain-Extraction-Based-on-Multi-Big-Data/blob/master/ImageStore/相似度衡量.png" width="200" height="200" /></div>

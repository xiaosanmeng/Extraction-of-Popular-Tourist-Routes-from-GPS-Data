def get_dist(ax, ay, headx, heady, tailx, taily):
    """点到直线距离计算"""
    a = taily - heady
    b = headx - tailx
    c = tailx * heady - headx * taily
    if (a == 0) & (b == 0):
        return sqrt((ax - headx) ** 2 + (ay - heady) ** 2)
    return abs(a * ax + b * ay + c) / sqrt(a ** 2 + b ** 2)


def getSparse(head, tail, workRoute, thres=50):
    """Douglas-Peuker抽稀"""
    if (tail - head) < 2:
        return [head, tail]
    # 计算轨迹中每个点到首末点连线的距离
    dists = [
        get_dist(
            workRoute.loc[x, 'x'], workRoute.loc[x, 'y'],
            workRoute.loc[head, 'x'], workRoute.loc[head, 'y'],
            workRoute.loc[tail, 'x'], workRoute.loc[tail, 'y'])
        for x in range(head + 1, tail)
    ]

    if max(dists) > thres:
        # 若最大距离超过阈值，则将最大距离点标记为一个稀疏拐点
        # 对首末点和拐点两端的轨迹点递归抽稀
        return getSparse(
            head,
            dists.index(max(dists)) + head + 1, workRoute) + getSparse(
            dists.index(max(dists)) + head + 1, tail, workRoute)
    else:
        # 若最大距离超过阈值，则认为该段轨迹已是原轨迹的稀疏表示
        return [head, tail]


"""轨迹抽稀"""
Result = []
thres = 50
sparseRoute = {}
workRoute = [x for x in range(len(group_key))]
for i in tqdm(range(len(group_key))):
    Result.append(Point[(Point['userID'] == group_key[i][0]) & (Point['date'] == group_key[i][1])])
    workRoute[i] = Result[i].copy().reset_index(drop=True)
    head = 0
    tail = len(workRoute[i]) - 1
    sparseRoute[group_key[i]] = sorted(list(set(getSparse(head, tail, workRoute[i], thres))))
"""游客抽稀轨迹提取，里面得到的是相关的索引"""
sparseRoute_info = []
for i in range(len(group_key)):
    sparseRoute_info.append(workRoute[i].loc[sparseRoute[group_key[i]], :])
sparseRoute_info = pd.concat(sparseRoute_info).reset_index(drop=True)


import numpy as np
from sklearn.cluster import KMeans
import sklearn.metrics as metric
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

def kmeans_cluster_test_n(start,N,x, debug=False):
    # N=最大聚类数+1
    # x为numpy array
    d_pool = np.arange(start, N, 1)
    score_list=[]
    for i, d in enumerate(d_pool):
        # 训练模型
        # n_clusters: 簇的个数，即你想聚成几类
        # init: 初始簇中心的获取方法
        # n_init: k-means算法将运行不同质心种子的次数。
        # max_iter: 最大迭代次数（因为kmeans算法的实现需要迭代）
        # tol: 容忍度，即kmeans运行准则收敛的条件
        model = KMeans(n_clusters=d)
        model.fit(x)
        if debug:
            print(u'划分%d个类：' % d)
        label_pred = model.labels_  # 获取聚类标签
        # print(label_pred)
        # centroids = model.cluster_centers_  # 获取聚类中心
        # print(centroids)
        # inertia = model.inertia_  # 获取聚类准则的总和，惯性准则的最终值(训练集中所有观测值到最近质心距离的平方和)。簇数越多越小
        # print(inertia)
        # 轮廓系数 值越大，表示聚类效果越好
        score=metric.silhouette_score(x, label_pred, metric='euclidean')
        if debug:
            print(score)
        score_list.append(score)
    index_list=np.argsort(score_list)
    max_index=index_list[-1]+start
    return  max_index



def kmeans_cluster_result(n,x):
    model = KMeans(n_clusters=n)
    model.fit(x)
    last_label_pred = model.labels_  # 获取聚类标签
    # print(last_label_pred)
    # print(type(last_label_pred))
    return last_label_pred


def tsne_show(n,x,last_label_pred):

    tsne=TSNE(n_components=2)
    newX = tsne.fit_transform(x)

    clrs = []  # 颜色  红到蓝
    for c in np.linspace(16711680, 255, n):  # linspace(初始值, 结束值, 值的个数) 生成的序列包含结束值。
        # print('#%06x' % int(c))
        clrs.append('#%06x' % int(c))

    #画图
    plt.figure(figsize=(9, 5), facecolor='w')
    plt.subplot(1, 1, 1)  # # plt.subplot(222)表示将整个图像窗口分为2行2列, 当前位置为2.
    # x, y对应了平面点的位置，
    # s控制点大小，
    # c对应颜色指示值，也就是如果采用了渐变色的话，我们设置c = x就能使得点的颜色根据点的x值变化，
    for jj in range(0,len(last_label_pred)):
        plt.scatter(newX[jj][0], newX[jj][1],c=clrs[last_label_pred[jj]] , s=20)  # 点样式，
    plt.grid(False) # 网格线
    plt.title('k-mean,tsne', fontsize=16)  # 标题
    plt.xlabel('X', fontsize=14)
    plt.ylabel('Y', fontsize=14)
    # plt.tight_layout(1, rect=(0, 0, 1, 0.95))   # tight_layout会自动调整子图参数，使之填充整个图像区域。
    plt.show()



def pca_show(n,x,last_label_pred):
    pca=PCA(n_components=2)
    newX = pca.fit_transform(x)

    clrs = []  # 颜色
    for c in np.linspace(16711680, 255, n):  # linspace(初始值, 结束值, 值的个数) 生成的序列包含结束值。
        # print('#%06x' % int(c))
        clrs.append('#%06x' % int(c))

    #画图
    plt.figure(figsize=(9, 5), facecolor='w')
    plt.subplot(1, 1, 1)  # # plt.subplot(222)表示将整个图像窗口分为2行2列, 当前位置为2.
    # x, y对应了平面点的位置，
    # s控制点大小，
    # c对应颜色指示值，也就是如果采用了渐变色的话，我们设置c = x就能使得点的颜色根据点的x值变化，
    for jj in range(0,len(last_label_pred)):
        plt.scatter(newX[jj][0], newX[jj][1],c=clrs[last_label_pred[jj]] , s=20)  # 点样式，
    plt.grid(False) # 网格线
    plt.title('k-means,PCA', fontsize=16)  # 标题
    plt.xlabel('X', fontsize=14)
    plt.ylabel('Y', fontsize=14)
    # plt.tight_layout(1, rect=(0, 0, 1, 0.95))   # tight_layout会自动调整子图参数，使之填充整个图像区域。
    plt.show()
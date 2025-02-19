import time
import os
from ..utils.data_operation import IMGDataset, transform_convert_save, load_csv_pair_tensor, PSDataset, read_csv_normal, \
    load_csv_patches_tensor, load_mask_component, load_mask_object, read_csv_int, read_csv_np, get_start_and_end
import numpy as np
from ..utils.cluster_and_decomposition import kmeans_cluster_test_n, kmeans_cluster_result, tsne_show, pca_show

def hierarchical_class_concept_tree(pathManager, config):
    """
    严格按照概念树的结构进行层次性的聚类，获得类概念树
    cluster_path/cluster_co.csv：组件层级聚类结果，size是superpixel_tensor长度
    cluster_path/cluster_ob.csv：物体层级聚类结果，size是patch_tensor长度
    """
    folder_path = os.path.join(pathManager.dir_cal_cluster_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # patch聚类
    folder_path1 = os.path.join(pathManager.dir_data_cal_image_patch_mid_pair_tensor_path)

    data_patch = []
    data_patch_fn = []
    # 按序号加载
    for i in range(config["dataset_img_num"]):
        filename = str(i) + '.csv'
        # 一个上级概念和它下辖的下级概念的组合tensor，第一条是上级概念的tensor
        tensor = read_csv_normal(os.path.join(folder_path1, filename))

        # Range from 1 is to get rid of the upper(parent) concept.
        for j in range(1, len(tensor)):
            data_patch.append(tensor[j].numpy())
            data_patch_fn.append(str(i) + '-' + str(j - 1))

    x = np.array(data_patch)
    data_patch_fn = np.array(data_patch_fn)
    # print(x.shape)
    n = kmeans_cluster_test_n(2, 7, x)  #
    print('对象级最佳划分簇数: ', n)

    ob_label = kmeans_cluster_result(n, x)

    # TODO: Get patch-level images to show
    print(type(ob_label))
    print(np.where(ob_label == 0)[0])
    patch_cluster1 = [data_patch_fn[i] for i in [np.where(ob_label == 0)[0]]][0]
    patch_cluster2 = [data_patch_fn[i] for i in [np.where(ob_label == 1)[0]]][0]
    print(len(patch_cluster1), patch_cluster1)
    print(len(patch_cluster2), patch_cluster2)

    ob_cluster_filename = 'cluster_ob'
    tmp = [ob_label]
    path = os.path.join(folder_path, ob_cluster_filename + '.csv')
    np.savetxt(path, tmp, delimiter=',')

    # 标记patch-level的分类簇个数？
    num_p1 = np.max(ob_label) + 1


    # ----------------------------------------------------------------------------
    patch_superpixel_mid_pair_tensor_folder_path = os.path.join(pathManager.dir_data_cal_patch_superpixel_mid_pair_tensor_path)
    s_label_list = []
    i_list = []

    # patch下辖superpixel聚类
    class_count = 0
    for i in range(num_p1):
        order = np.where(ob_label == i)[0]
        filename_list_patches = data_patch_fn[order]

        # print('filename_list_patches:',filename_list_patches)
        filename_list_s1 = []
        tensor_superpixels = []

        cnt = 0
        length = 0
        # 第i个类别中遍历每一个patch
        for ff in filename_list_patches:
            filename = ff + '.csv'
            filepath = os.path.join(patch_superpixel_mid_pair_tensor_folder_path, filename)
            # 一个上级概念和它下辖的下级概念的组合tensor，第一条是上级概念的tensor
            tensor = read_csv_normal(filepath)

            # print(len(tensor)-1, filename)
            length += len(tensor)-1
            for j in range(1, len(tensor)):

                tensor_superpixels.append(tensor[j].numpy())
                filename_list_s1.append(ff + '-' + str(j - 1))

        # 第i个类别所有的superpixel_tensor
        tensor_superpixels = np.array(tensor_superpixels)
        # print(tensor_superpixels.shape)
        n = kmeans_cluster_test_n(8, 13, tensor_superpixels)  #
        print('组件级最佳划分簇数: ', n)

        # TODO: all patch-superpixel tensors constraints to cluster classes. The processing tensor is in pair
        # For tabby class, cluster 0 number of patches is 49, cluster 1 number of patches is 61.

        superpixels_label = kmeans_cluster_result(n, tensor_superpixels)
        superpixels_label = superpixels_label + class_count

        s_label_list.extend(superpixels_label.tolist())
        i_list.extend(filename_list_s1)
        # print(len(superpixels_label), superpixels_label)
        # print(len(filename_list_s1), filename_list_s1)
        print("Belong to patch: ", i)
        for k in range(class_count, class_count+n):
            patch_cluster1 = [np.array(filename_list_s1)[j] for j in [np.where(superpixels_label == k)[0]]][0]
            print(patch_cluster1)
        class_count = class_count + n

    # 转换
    s_label_list = np.array(s_label_list)
    i_list = np.array(i_list)
    s_label_f = []
    i_list_f = []
    for i in range(config["dataset_img_num"]):
        for j in range(config["patch_num"]):
            for k in range(config["seg_num"]):
                ff = str(i) + '-' + str(j) + '-' + str(k)
                indices = np.where(i_list == ff)[0]
                if len(indices) > 0:
                    i_list_f.append(i)
                    s_label_f.append(s_label_list[indices[0]])
                else:
                    break

    path = os.path.join(folder_path, 'cluster_co.csv')
    np.savetxt(path, [np.array(s_label_f)], delimiter=',')
    path = os.path.join(folder_path, 'image_id.csv')
    np.savetxt(path, [np.array(i_list_f)], delimiter=',')

def run_clustering(pathManager, config):
    # 6.66s
    start_time = time.time()
    hierarchical_class_concept_tree(pathManager, config)
    end_time = time.time()
    execution_time = end_time - start_time
    print("函数执行时间为：", execution_time, "秒")
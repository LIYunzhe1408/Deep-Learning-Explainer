import argparse
import os
import numpy as np
import torch

from utils.data_operation import read_csv_int, read_csv_np, get_start_and_end, load_mask_component, IMGDataset, \
    transform_convert_save, load_mask_object

# parser = argparse.ArgumentParser()
# parser.add_argument('--class_name', type=str, default='/tabby', help='name of the explained class ')
# parser.add_argument('--class_dim', type=int, default=281, help='order of the explained class ')
# parser.add_argument('--dataset_path', type=str, default='/n02123045', help='path of folder of a class')
# # parser.add_argument('--class_name', type=str, default='/sorrel', help='name of the explained class ')
# # parser.add_argument('--class_dim', type=int, default=339, help='order of the explained class ')
# # parser.add_argument('--dataset_path', type=str, default='/n02389026', help='path of folder of a class')
# parser.add_argument('--data_path', type=str, default='./dataset', help='path of image dataset folders')
#
# parser.add_argument('--mid_cal_folder', type=str, default='./data_cal', help='mid result folder ')
# parser.add_argument('--result_save_path', type=str, default='./result_save', help='save result')
# parser.add_argument('--cluster_path', type=str, default='/cluster_path', help='save the cluster label')
# parser.add_argument('--image_co_mask_path', type=str, default='/image_co_mask_path', help='save the image segment mask about component level')
# parser.add_argument('--image_ob_mask_path', type=str, default='/image_ob_mask_path', help='save the image segment mask about object level')
#
# parser.add_argument('--ob_concept_img_path', type=str, default='ob_concept_imgs', help='save object concept images')
# parser.add_argument('--co_concept_img_path', type=str, default='co_concept_imgs', help='save component concept images')
#
#
# parser.add_argument('--method_version', type=str, default='/official_version', help='Official version')
# parser.add_argument('--img_num', type=int, default=6, help='order of explained image')
# # parser.add_argument('--img_num', type=int, default=21, help='order of explained image')
# parser.add_argument('--model_name', type=str, default='/googlenet', help='name of explained model')
# parser.add_argument('--patch_num', type=int, default=21, help='number of semantics segments')
# parser.add_argument('--seg_num', type=int, default=15, help='number of superpixel segments')  # 11
#
# args = parser.parse_args()
# args.cluster_path = args.mid_cal_folder + args.class_name + args.method_version + args.cluster_path + args.model_name
# args.result = args.result_save_path + args.class_name + args.method_version + args.model_name
# args.image_co_mask_path = args.mid_cal_folder + args.class_name + args.method_version + args.image_co_mask_path
# args.image_ob_mask_path = args.mid_cal_folder + args.class_name + args.method_version + args.image_ob_mask_path
# args.data_path = args.data_path + args.dataset_path


def run_local_explanation(pathManager, configuration):
    # ob------------------------------------------------------
    # 加载ob级别图片的所属概念信息
    label = read_csv_int(os.path.join(pathManager.dir_cal_cluster_path, 'cluster_ob.csv'))
    list_i = []
    for i in range(50):
        for j in range(configuration["patch_num"]):
            fn=str(i)+'-'+str(j)+'.csv'
            if os.path.exists(os.path.join(pathManager.dir_cal_image_ob_mask_path,fn)):
                list_i.append(i)
            else:
                break

    # 加载shapley value
    value_path = os.path.join(pathManager.dir_score_save, str(configuration["img_num"]), 'object_value.csv')
    value_list = read_csv_np(value_path)
    print('value_list: ', value_list)
    # 获取序号图片的ob的序号
    start, end = get_start_and_end(list_i, configuration["img_num"])
    # 图片的ob的概念 #
    cluser_label = label[start:end + 1]
    print('cluser_label: ',cluser_label)
    # 获取不重复概念编号
    concept_list = list(set(label[start:end + 1]))
    print('不重复ob概念编号:', concept_list)

    # 确定概念分数
    concept_score_list = np.zeros(len(concept_list))
    for i in range(len(value_list)):
        for j in range(len(concept_list)):
            if cluser_label[i] == concept_list[j]:
                concept_score_list[j] = concept_score_list[j] + value_list[i]
                break

    masks = load_mask_object(pathManager.dir_cal_image_ob_mask_path, configuration["img_num"], configuration["patch_num"])
    dataSet = IMGDataset(data_dir=os.path.join(pathManager.dir_source_folder))
    img_tensor=dataSet[configuration["img_num"]]

    folder_path = os.path.join(pathManager.dir_ob_co_each_image,str(configuration["img_num"]), "ob_concept_imgs")

    patch_score = {}
    for i in range(len(concept_list)):
        ob_mask=torch.zeros([224, 224])
        for j in range(len(cluser_label)):
            if cluser_label[j]==concept_list[i]:
                ob_mask=ob_mask+masks[j]
        print('ob_concept: ',concept_list[i],', score: ',concept_score_list[i])
        concept_img=ob_mask*img_tensor
        transform_convert_save(concept_img, dataSet.return_transform_tensor(), folder_path, str(concept_list[i])+ '.jpg')
        patch_score.update({concept_list[i]: {"src": '',
                                              "score": concept_score_list[i],
                                              "label": '',
                                              "contributors": []}})



    # co------------------------------------------------------

    # 加载co级别图片的所属概念信息
    label = read_csv_int(os.path.join(pathManager.dir_cal_cluster_path, 'cluster_co.csv'))
    list_i = read_csv_int(os.path.join(pathManager.dir_cal_cluster_path, 'image_id.csv'))
    # 加载shapley value
    value_path = os.path.join(pathManager.dir_score_save, str(configuration["img_num"]), 'component_value.csv')
    value_list = read_csv_np(value_path)
    print('value_list: ',value_list)
    # 获取序号图片的co的序号
    start, end = get_start_and_end(list_i, configuration["img_num"])
    # print(start, end)
    # 图片的co的概念 #
    cluser_label = label[start:end + 1]
    print('cluser_label: ',cluser_label)
    # 获取不重复概念编号
    concept_list = list(set(label[start:end + 1]))
    print('不重复co概念编号:', concept_list)

    # 确定概念分数
    concept_score_list = np.zeros(len(concept_list))
    for i in range(len(value_list)):
        for j in range(len(concept_list)):
            if cluser_label[i] == concept_list[j]:
                concept_score_list[j] = concept_score_list[j] + value_list[i]
                break

    masks = load_mask_component(pathManager.dir_cal_image_co_mask_path, configuration["img_num"], configuration["patch_num"], configuration["seg_num"])
    dataSet = IMGDataset(data_dir=os.path.join(pathManager.dir_source_folder))
    img_tensor=dataSet[configuration["img_num"]]

    folder_path = os.path.join(pathManager.dir_ob_co_each_image, str(configuration["img_num"]), "co_concept_imgs")

    contributors = {}
    for i in range(len(concept_list)):
        co_mask=torch.zeros([224, 224])
        for j in range(len(cluser_label)):
            if cluser_label[j]==concept_list[i]:
                co_mask=co_mask+masks[j]
        print('co_concept: ',concept_list[i],', score: ',concept_score_list[i])
        concept_img=co_mask*img_tensor
        transform_convert_save(concept_img, dataSet.return_transform_tensor(), folder_path, str(concept_list[i])+ '.jpg')
        contributors.update({concept_list[i]: {"src": '', "score": concept_score_list[i], "label": ''}})


    patch_and_component = {"patch": patch_score, "contributors": contributors}
    print(patch_and_component)
    local_explanation_path = os.path.join(pathManager.dir_ob_co_each_image, str(configuration["img_num"]), "score.txt")
    if isinstance(patch_and_component, str):
        patch_and_component = eval(patch_and_component)
    with open(local_explanation_path, 'w', encoding='utf-8') as f:
        f.write(str(patch_and_component))  # dict to str
    with open(local_explanation_path, 'r', encoding='utf-8') as f:
        dict_cluster = eval(f.read())  # eval
        print(dict_cluster == patch_and_component)
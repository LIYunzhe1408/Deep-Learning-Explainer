import os
from utils.data_operation import IMGDataset, transform_convert_save, load_csv_pair_tensor, PSDataset, read_csv_normal, \
    load_csv_patches_tensor, load_mask_component, load_mask_object, read_csv_int, read_csv_np, get_start_and_end
import numpy as np
import torch
from utils.visualization import patches_vis, superpixel_vis, result_heatmap, result_ssc, result_sdc, \
    ssc_concept_consistency, sdc_concept_consistency, ssc_concept_prob, sdc_concept_prob, \
    ssc_concept_consistency_mask, sdc_concept_consistency_mask, ssc_concept_prob_mask, sdc_concept_prob_mask, \
    ssc_concept_prob_conpect_exist, sdc_concept_prob_conpect_exist, ssc_concept_prob_mask_conpect_exist, \
    sdc_concept_prob_mask_conpect_exist
from utils.hie_model import HRE, loss_function, model_save, HREEM1_googlenet, HRE_DEEP


def run_sscc_sdcc_consistency(configuration, pathManager, test_img_id, class_name):
    """
    图片可视化结果,保存在
    ./result_save/class/version/model/imageid/sscc_sdcc_re_5.csv
    """
    # 以概念为单位的ssc、sdc

    # 加载co级别图片的所属概念信息
    label = read_csv_int(os.path.join(pathManager.dir_cal_cluster_path, 'cluster_co.csv'))
    list_i = read_csv_int(os.path.join(pathManager.dir_cal_cluster_path, 'image_id.csv'))
    # 加载shapley value
    value_path = os.path.join(pathManager.dir_score_save, str(test_img_id), 'component_value.csv')
    value_list = read_csv_np(value_path)
    print(value_list)
    # 获取序号图片的co的序号
    start, end = get_start_and_end(list_i, test_img_id)
    print(start, end)
    # 图片的co的概念所属的cluster #
    cluser_label = label[start:end + 1]
    print(cluser_label)
    # 获取不重复概念编号
    concept_list = list(set(label[start:end + 1]))
    print('不重复概念编号:', concept_list)

    # 确定概念排序  从小到大
    concept_score_list = np.zeros(len(concept_list))
    for i in range(len(value_list)):
        for j in range(len(concept_list)):
            if cluser_label[i] == concept_list[j]:
                concept_score_list[j] = concept_score_list[j] + value_list[i]
                break

    concept_score_id = np.argsort(concept_score_list)
    # print(concept_score_id)
    sort_concept_list = [concept_list[i] for i in concept_score_id]
    print('重要概念排序:', sort_concept_list)

    # 加载mid_tensor
    ps_tensor_list = []
    for i in range(configuration["patch_num"]):
        file_path = os.path.join(pathManager.dir_data_cal_hre_ps_code_path, str(test_img_id) + '-' + str(i) + '.csv')
        if os.path.exists(file_path):
            ps_tensor_list.append(read_csv_normal(file_path))
        else:
            break

    # [0]是取出指定图片的第0个patch，[1:]取出除patch-tensor外所有的superpixel-tensor
    tensor_ssc_sdc = ps_tensor_list[0][1:].clone()
    for i in range(1, len(ps_tensor_list)):
        tensor_ssc_sdc = torch.cat((tensor_ssc_sdc, ps_tensor_list[i][1:].clone()), dim=0)
    print(tensor_ssc_sdc.shape)

    ip_tensor = read_csv_normal(os.path.join(pathManager.dir_data_cal_hre_ip_code_path, str(test_img_id) + '.csv'))
    image_tensor = ip_tensor[0]

    # 加载模型
    HREEM_model1 = HREEM1_googlenet(hre_model_path=pathManager.dir_model_save).eval()

    # sscc sdcc
    # HRE Model, patch-tensor+superpixel-tensor, image_tensor, sorted list, all labels of superpixels
    sscc = ssc_concept_consistency(HREEM_model1, tensor_ssc_sdc, image_tensor, configuration["image chooser"][class_name]["class_dim"], sort_concept_list,
                                   cluser_label, configuration["concept_num"])
    sdcc = sdc_concept_consistency(HREEM_model1, tensor_ssc_sdc, image_tensor, configuration["image chooser"][class_name]["class_dim"], sort_concept_list,
                                   cluser_label, configuration["concept_num"])
    file_path = os.path.join(pathManager.dir_score_save, str(test_img_id), 'sscc_sdcc_re_' + str(configuration["concept_num"]) + '.csv')
    np.savetxt(file_path, [np.array([sscc, sdcc])], delimiter=',')
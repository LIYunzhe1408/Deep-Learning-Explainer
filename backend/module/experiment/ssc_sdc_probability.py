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


def run_ssc_sdc_probability(config, pathManager, test_img_id):
    """
    单图片ssc、sdc计算,保存在
    ./result_save/class/version/model/imageid/ssc_sdc_re_ce_5.csv
    """
    label = read_csv_int(os.path.join(pathManager.dir_cal_cluster_path, 'cluster_co.csv'))
    list_i = read_csv_int(os.path.join(pathManager.dir_cal_cluster_path, 'image_id.csv'))
    start, end = get_start_and_end(list_i, test_img_id)
    cluser_label = label[start:end + 1]
    print(len(cluser_label), cluser_label)
    print(list(set(cluser_label)))
    sort_concept_id = read_csv_int(os.path.join(pathManager.dir_class_concept_value_save, 'concept_id.csv'))

    print('sort_concept_id:', sort_concept_id)
    # 加载mid_tensor
    ps_tensor_list = []
    for i in range(config["patch_num"]):
        file_path = os.path.join(pathManager.dir_data_cal_hre_ps_code_path, str(test_img_id) + '-' + str(i) + '.csv')
        if os.path.exists(file_path):
            ps_tensor_list.append(read_csv_normal(file_path))
        else:
            break

    tensor_ssc_sdc = ps_tensor_list[0][1:].clone()
    for i in range(1, len(ps_tensor_list)):
        tensor_ssc_sdc = torch.cat((tensor_ssc_sdc, ps_tensor_list[i][1:].clone()), dim=0)
    print(tensor_ssc_sdc.shape)

    ip_tensor = read_csv_normal(os.path.join(pathManager.dir_data_cal_hre_ip_code_path, str(test_img_id) + '.csv'))
    image_tensor = ip_tensor[0]

    # 加载模型
    HREEM_model1 = HREEM1_googlenet(hre_model_path=pathManager.dir_model_save).eval()

    # ssc sdc
    # 增加概念，观测是否最大的概率维度为原本的预测类别
    # ssccp1,ssccp2=ssc_concept_prob(HREEM_model1, tensor_ssc_sdc, image_tensor, sort_concept_id, cluser_label,args.concept_num)
    ssccp1, ssccp2 = ssc_concept_prob_conpect_exist(HREEM_model1, tensor_ssc_sdc, image_tensor, sort_concept_id,
                                                    cluser_label, config["concept_num"])
    # 删去概念，观测是否最大的概率维度为原本的预测类别
    sdccp1, sdccp2 = sdc_concept_prob_conpect_exist(HREEM_model1, tensor_ssc_sdc, image_tensor, sort_concept_id,
                                                    cluser_label, config["concept_num"])
    file_path = os.path.join(pathManager.dir_score_save, str(test_img_id), 'ssc_sdc_re_ce_' + str(config["concept_num"]) + '.csv')
    np.savetxt(file_path, np.array([ssccp1, ssccp2, sdccp1, sdccp2]), delimiter=',')
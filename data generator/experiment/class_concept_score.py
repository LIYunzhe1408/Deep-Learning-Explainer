import os
from utils.data_operation import IMGDataset, transform_convert_save, load_csv_pair_tensor, PSDataset, read_csv_normal, \
    load_csv_patches_tensor, load_mask_component, load_mask_object, read_csv_int, read_csv_np, get_start_and_end
import numpy as np


def run_class_concept_score(config, pathManager):
    """
    类全局概念计算,保存在
    ./result_save/class/version/model/class_concept_value_path/concept_id.csv,concept_value.csv
    """
    label = read_csv_int(os.path.join(pathManager.dir_cal_cluster_path, 'cluster_co.csv'))
    value_list_all = []
    for i in range(config["dataset_img_num"]):
        value_path = os.path.join(pathManager.dir_score_save, str(i), 'component_value.csv')
        value_list = read_csv_np(value_path)
        value_list_all.extend(value_list)
    print(len(label), len(value_list_all))
    concept_num = list(set(label))
    concept_score_list = np.zeros(len(concept_num))
    concept_score_idsum = np.zeros(len(concept_num))
    for i in range(len(label)):
        concept_score_list[label[i]] = concept_score_list[label[i]] + value_list_all[i]
        concept_score_idsum[label[i]] = concept_score_idsum[label[i]] + 1
    concept_score_list1 = [concept_score_list[k] / concept_score_idsum[k] for k in range(len(concept_score_list))]
    # concept_score_list1=concept_score_list
    concept_score_id1 = np.argsort(concept_score_list1)
    print(concept_score_id1)
    sort_concept_score_list1 = [concept_score_list1[i] for i in concept_score_id1]
    print(sort_concept_score_list1)

    folder_path = os.path.join(pathManager.dir_class_concept_value_save)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    save_path = os.path.join(folder_path, 'concept_id.csv')
    # save_path = os.path.join(folder_path, 'concept_id_nodiv.csv')
    np.savetxt(save_path, np.array([concept_score_id1]), delimiter=',')
    save_path = os.path.join(folder_path, 'concept_value.csv')
    # save_path = os.path.join(folder_path, 'concept_value_nodiv.csv')
    np.savetxt(save_path, np.array([sort_concept_score_list1]), delimiter=',')
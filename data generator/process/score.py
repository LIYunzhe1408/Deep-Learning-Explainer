import os
import time
from utils.data_operation import IMGDataset, read_csv_normal
from utils.hie_model import HREEM1_googlenet
import torch.nn.functional as F
from utils.shapley_value_hre import hre_shapley_value
import numpy as np


def get_result_score(explained_model, device, pathManager, config, class_name):
    """
    重要度计算模块 sh-tree，结果保存在
    ./result_save/class/version/model/...

    """
    print("概念重要度计算开始")
    print("----------------")
    print("Input is from one image.")
    print("Image_patch from //hre_ip_code_path// and patch_superpixels from //hre_ps_code_path//")
    print("----------------")
    image_id = config["img_num"]
    # 读取csv
    ip_tensor = read_csv_normal(os.path.join(pathManager.dir_data_cal_hre_ip_code_path, str(image_id) + '.csv')).to(
        device)
    ps_tensor_list = []
    for i in range(config["patch_num"]):
        file_path = os.path.join(pathManager.dir_data_cal_hre_ps_code_path, str(image_id) + '-' + str(i) + '.csv')
        if os.path.exists(file_path):
            ps_tensor_list.append(read_csv_normal(file_path))
        else:
            break

    # 局部model，结合了两个训练好模型的参数
    HREEM_model1 = HREEM1_googlenet(hre_model_path=pathManager.dir_model_save).to(device).eval()

    cal_out_dim = config["image chooser"][class_name]["class_dim"]  # 要解释的类的输出维度，即类，0-999  #logit是softmax之前那层的输出
    # 用shapley value计算重要度

    # ori image tensor
    # print(' ori image logit:')
    dataSet = IMGDataset(data_dir=os.path.join(pathManager.dir_source_folder))
    explained_model.eval()

    #
    image_out = F.softmax(explained_model(dataSet[image_id].view(1, 3, 224, 224).to(device)).detach(), dim=1)[:,
                cal_out_dim]
    print('origin explained_model image probability:', image_out.to("cpu"))
    # image and patch code result
    image_patch_value = F.softmax(HREEM_model1(ip_tensor).detach(), dim=1)[:, cal_out_dim].to("cpu")
    print('image and patch hidden-code decode probability value of HREEM_model1:', image_patch_value)

    # shapley with consistency
    print('shapley with consistency:')
    print('image shapley value:', float(image_patch_value[0]))
    # patch shapley value
    patch_value = hre_shapley_value(ip_tensor[1:].to(device), HREEM_model1, cal_out_dim, float(image_patch_value[0]))
    print('patch shapley value:', patch_value)
    print('sum=', sum(patch_value))
    superpixel_value_list_consist = []
    for i in range(len(ps_tensor_list)):
        print(ps_tensor_list[i].shape)
        superpixel_value = hre_shapley_value(ps_tensor_list[i][1:].to(device), HREEM_model1, cal_out_dim,
                                             patch_value[i])  # 上一步计算的值直接放入
        print('superpixel shapley value ' + str(i) + ':', superpixel_value)
        print('sum=', sum(superpixel_value))
        superpixel_value_list_consist.append(superpixel_value)

    # shapley value结果保存
    folder_path = os.path.join(pathManager.dir_score_save, str(image_id))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_name1 = 'image_value.csv'
    file_name2 = 'object_value.csv'
    file_name3 = 'component_value.csv'
    value_list_consist = [i for item in superpixel_value_list_consist for i in item]
    print(len(value_list_consist))

    # 存的不是归一化的
    np.savetxt(os.path.join(folder_path, file_name1), [image_patch_value[0].numpy()], delimiter=',')
    np.savetxt(os.path.join(folder_path, file_name2), [np.array(patch_value)], delimiter=',')
    np.savetxt(os.path.join(folder_path, file_name3), [np.array(value_list_consist)], delimiter=',')

    print("概念重要度计算结束")


def run_score(explained_model, device, pathManager, config, class_name):
    # 计算指定图片概念解释：50s
    start_time = time.time()
    get_result_score(explained_model, device, pathManager, config, class_name)
    end_time = time.time()
    execution_time = end_time - start_time
    print("函数执行时间为：", execution_time, "秒")






import os
from ..utils.data_operation import IMGDataset, load_csv_pair_tensor, load_csv_patches_tensor
import torch
import numpy as np
import time


def extract_img_ob_features(explained_model, device, pathManager, config):
    """
    特征提取模块1
    获得图片与对应的对象级概念在预训练模型特征提取结束后的输出并保存
    ./data_cal/class/version/image_patch_mid_pair_tensor/...
    """
    print("图片与对象级概念表达提取开始")

    folder_path = os.path.join(pathManager.dir_data_cal_image_patch_mid_pair_tensor_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    explained_model.eval()

    # 钩子
    def hook(module, input, output):
        # print(output.shape)
        output = output.view(output.shape[0], -1)
        output = output.to("cpu")
        # print(output.shape)  x-1024
        save_path = os.path.join(pathManager.dir_data_cal_image_patch_mid_pair_tensor_path, str(i) + '.csv')
        np.savetxt(save_path, output.detach().numpy(), delimiter=',')
        return None

    # 注册钩子,for average pooling
    handle = explained_model.avgpool.register_forward_hook(hook)
    # 数据集--某一类图片
    dataSet = IMGDataset(data_dir=os.path.join(pathManager.dir_source_folder))

    # 加载数据保存中间结果
    for i in range(len(dataSet)):
        patches_tensor = load_csv_patches_tensor(pathManager.dir_cal_patch_tensor_path, i, config["patch_num"])
        pair_tensor = torch.cat((dataSet[i].view(1, 3, 224, 224), patches_tensor), 0)
        pair_tensor = pair_tensor.to(device)
        explained_model(pair_tensor)
    handle.remove()  # hook删除
    print("图片与对象级概念表达提取结束")


def extract_ob_co_features(explained_model, device, pathManager, config):
    """
    特征提取模块2
    获得对象级概念与其对应的组件级概念在预训练模型提取结束后的的输出
    ./data_cal/class/version/patch_superpixel_mid_pair_tensor/...
    """
    print("对象级概念与组件级概念表达提取开始")

    folder_path = os.path.join(pathManager.dir_data_cal_patch_superpixel_mid_pair_tensor_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    explained_model.eval()
    length = 0
    def hook(module, input, output):
        # print(output.shape)  # a,b,1,1
        output = output.view(output.shape[0], -1)
        output = output.to("cpu")
        save_path = os.path.join(folder_path, file)
        np.savetxt(save_path, output.detach().numpy(), delimiter=',')
        # features.append(output)
        return None

    handle = explained_model.avgpool.register_forward_hook(hook)

    patch_tensor_folder = pathManager.dir_cal_patch_tensor_path
    # superpixel_tensor_folder=args.superpixel_tensor_path
    files = os.listdir(os.path.join(patch_tensor_folder))
    # for循环，一个patch一组
    for file in files:
        # 一个对象级概念和它下辖的组件级概念的组合tensor，第一条是对象级概念的tensor
        pairs_tensor = load_csv_pair_tensor(os.path.join(patch_tensor_folder, file), pathManager.dir_cal_superpixel_tensor_path,
                                            config["seg_num"])
        length += len(pairs_tensor)-1
        pairs_tensor = pairs_tensor.to(device)
        explained_model(pairs_tensor)
    print(length)
    handle.remove()  # hook删除
    print("对象级概念与组件级概念表达提取结束")


def ob_co_tensor_extraction(explained_model, device, pathManager, config):
    # 6.66s
    start_time = time.time()
    extract_img_ob_features(explained_model, device, pathManager, config)
    end_time = time.time()
    execution_time = end_time - start_time
    print("函数执行时间为：", execution_time, "秒")

    # 35s
    start_time = time.time()
    extract_ob_co_features(explained_model, device, pathManager, config)
    end_time = time.time()
    execution_time = end_time - start_time
    print("函数执行时间为：", execution_time, "秒")



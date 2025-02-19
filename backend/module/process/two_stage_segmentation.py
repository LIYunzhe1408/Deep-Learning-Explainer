import os
from ..utils.data_operation import IMGDataset, transform_convert_save
import torchvision.models as models
from torch.utils.data.dataloader import DataLoader
import torch
from ..utils.visualization import patches_vis, superpixel_vis
import numpy as np
import skimage.segmentation as segmentation
import time


def two_stage_image_segmentation(pathset, args, model_name):
    """
    图片预处理模块，预处理图片保存在
    ./visualization_result/class/version/handle_image/...
    图片两段式分割，保存分割后的图片块和对应的tensor
    ./data_cal/class/version/patch，superpixel，patch_tensor，superpixel_tensor/...  ,后两个太大了可删
    在图片上的分割结果可视化保存
    ./visualization_result/class/version/semantic_segmentation,superpixel_segmentation/...
    mask保存
    ./data_cal/class/version/image_co_mask_path，image_ob_mask_path/...
    """
    seg_num = args["seg_num"]
    seg_save_param = args["seg_save_param"]
    seg_batch_size = args["seg_batch_size"]

    print("图片分割开始")
    folder_path = os.path.join(pathset.dir_handle_image)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # 数据集--某一类图片
    dataSet = IMGDataset(data_dir=os.path.join(pathset.dir_source_folder))
    for ss in range(len(dataSet)):
        dataSet.img_save(ss, folder_path)
    # dataSet.img_show(0)
    # 加载数据集
    data_loader = DataLoader(dataset=dataSet, batch_size=seg_batch_size, shuffle=False)

    if model_name == "fcn":
        # 使用语义分割预训练模型 这是最差的那个  可替换
        seg_model = models.segmentation.fcn_resnet50(pretrained=True, progress=False).eval()
    elif model_name == "lraspp":
        seg_model = models.segmentation.lraspp_mobilenet_v3_large(pretrained=True, progress=False).eval()
    else:
        # 这是pytorch预训练模型里最好的的那个
        seg_model = models.segmentation.deeplabv3_resnet101(pretrained=True, progress=False).eval()

    image_num = 0
    image_cnt = 0

    for i, data in enumerate(data_loader):

        """
        语义分割
        对象级概念
        """
        # print(len(data),data.shape,i)   #n, 3, 224, 224
        output = seg_model(data)['out']
        # print(output.shape) # n-21-224-224
        mask_data = torch.argmax(output, dim=1)
        # print(mask_data,mask_data.shape) # n-224-224
        # print(np.unique(mask_data))  查看能分割出的类
        # 语义分割结果可视化+保存
        for it, img in enumerate(data):
            img = img.reshape((1, 3, 224, 224))
            patches_vis(img, output[it].reshape(1, 21, 224, 224).detach(), image_cnt, pathset.dir_patch_image)
            image_cnt += 1

        # binary mask制作与存储
        mask_data_np = mask_data.numpy()
        # print(mask_data_np[1])
        seg_masks_batch = []
        # num_non_zero=[]
        for j in range(len(mask_data_np)):
            seg_masks = []
            for s in range(mask_data_np[j].max() + 1):
                seg_mask = (mask_data_np[j] == s).astype(int)  # binary mask
                if np.mean(seg_mask) > seg_save_param:  # 当前：大于0个像素的mask保存
                    seg_masks.append(seg_mask)
                    # num_non_zero.append(np.count_nonzero(seg_mask))
            # print(len(seg_masks))
            seg_masks_batch.append(seg_masks)  # n-p-224*224

        # 根据mask获得分割图片的tensor
        patches = []  # patches.shape  #n-p-3*224*224
        for j in range(len(seg_masks_batch)):
            patch = []
            for k in range(len(seg_masks_batch[j])):
                patch.append(torch.from_numpy(seg_masks_batch[j][k]) * data[j])
            patches.append(patch)

        # 保存tensor，保存图片
        folder_path = os.path.join(pathset.dir_cal_patch_tensor_path)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        for j in range(len(patches)):
            for k in range(len(patches[j])):
                filename = str(image_num + j) + '-' + str(k)  # 第len(i)+j张图-第k个mask
                tmp = [patches[j][k].view(-1).numpy()]
                path = os.path.join(folder_path, filename + '.csv')
                np.savetxt(path, tmp, delimiter=',')
                transform_convert_save(patches[j][k], dataSet.return_transform_tensor(), pathset.dir_patches,
                                       filename + '.jpg')
        print("batch" + str(i) + "patches张量与图片保存结束")

        # 保存语义分割mask
        folder_path = os.path.join(pathset.dir_cal_image_ob_mask_path)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        for j in range(len(seg_masks_batch)):
            for k in range(len(seg_masks_batch[j])):
                filename = str(image_num + j) + '-' + str(k)  # 第len(i)+j张图-第k个语义
                tmp = [seg_masks_batch[j][k].reshape(-1)]
                path = os.path.join(folder_path, filename + '.csv')
                np.savetxt(path, tmp, delimiter=',')

        """
        超像素分割
        组件级概念

        """
        # 获取超像素mask,联合语义mask，得到超像素图片tensor
        superpixelj = []  # n-p-s-3*224*224  超像素tensor
        i_mask_j = []  # 单图片全部超像素的mask  全0，1  list-tensor
        for j in range(len(patches)):
            superpixelk = []  # p-s-3*224*224
            i_mask_k = []  # p-s-224*224
            for k in range(len(patches[j])):  # n-p-3*224*224
                segments = segmentation.slic(patches[j][k].numpy(), n_segments=seg_num, compactness=20,
                                             channel_axis=0)
                # print(type(segments))  #numpy.ndarray
                superpixels = []  # s-3*224*224
                i_mask_s = []  # s-224*224
                for s in range(segments.max() + 1):
                    mask = (segments == s).astype(int)
                    i_mask_s_f = torch.from_numpy(mask) * torch.from_numpy(seg_masks_batch[j][k])
                    i_mask_s_f_n = i_mask_s_f.numpy()
                    if np.mean(i_mask_s_f_n) > seg_save_param:
                        superpixels.append(i_mask_s_f * patches[j][k])
                        i_mask_s.append(i_mask_s_f)
                superpixelk.append(superpixels)
                i_mask_k.append(i_mask_s)
            superpixelj.append(superpixelk)
            i_mask_j.append(i_mask_k)

        # 保存tensor，保存图片
        folder_path = os.path.join(pathset.dir_cal_superpixel_tensor_path)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        for j in range(len(superpixelj)):
            for k in range(len(superpixelj[j])):
                for s in range(len(superpixelj[j][k])):
                    filename = str(image_num + j) + '-' + str(k) + '-' + str(s)  # 第len(i)+j张图-第k个语义-第s个段
                    tmp = [superpixelj[j][k][s].view(-1).numpy()]
                    path = os.path.join(folder_path, filename + '.csv')
                    np.savetxt(path, tmp, delimiter=',')
                    transform_convert_save(superpixelj[j][k][s], dataSet.return_transform_tensor(),
                                           pathset.dir_superpixels, filename + '.jpg')

        # 保存超像素mask
        folder_path = os.path.join(pathset.dir_cal_image_co_mask_path)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        for j in range(len(i_mask_j)):
            for k in range(len(i_mask_j[j])):
                for s in range(len(i_mask_j[j][k])):
                    filename = str(image_num + j) + '-' + str(k) + '-' + str(s)  # 第len(i)+j张图-第k个语义-第s个段
                    tmp = [i_mask_j[j][k][s].view(-1).numpy()]
                    path = os.path.join(folder_path, filename + '.csv')
                    np.savetxt(path, tmp, delimiter=',')

        #
        # 单图片两段分割结果可视化 + 保存
        add_param = 1
        for j in range(len(i_mask_j)):
            image_finally_mask = torch.zeros(224, 224)
            for k in range(len(i_mask_j[j])):
                for s in range(len(i_mask_j[j][k])):
                    image_finally_mask = image_finally_mask + i_mask_j[j][k][s] * add_param
                    add_param = add_param + 1
            superpixel_vis(data[j], image_finally_mask, str(image_num + j), pathset.dir_superpixel_image)

        print("batch" + str(i) + "superpixel张量、图片、mask保存结束")
        image_num += len(data)

    print("图片分割结束")


def two_stage_segmentation(pathset, args, model_name):
    start_time = time.time()
    # TODO 分割图片的数量原代码用的是文件夹里图片的length，不看yaml的....要改！！！
    two_stage_image_segmentation(pathset, args, model_name)
    end_time = time.time()
    execution_time = end_time - start_time
    print("函数执行时间为：", execution_time, "秒")



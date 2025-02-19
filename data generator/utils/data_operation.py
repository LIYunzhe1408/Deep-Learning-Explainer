import torch
import torchvision
from torch.utils.data.dataset import Dataset
from torchvision.transforms import transforms
from PIL import Image
import os
import numpy as np
import csv


class IMGDataset(Dataset):
    def __init__(self, data_dir):
        """
        某一类图片的Dataset
        :param data_dir: str, 数据集所在路径
        """

        self.data_info = self.get_img_info(data_dir)
        self.transform_tensor = transforms.Compose([
            transforms.Resize(224), # 224,224:缩放，长宽比不变 ;224:缩放图片(Image)，保持长宽比不变，最短边为224像素
            transforms.CenterCrop(224), # 从图片中间切出224*224的图片
            transforms.ToTensor(), # 将图片(Image)转成Tensor，归一化至[0, 1]（直接除以255）
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) # 常用标准化
        ])

    def __getitem__(self, index):
        img_path = self.data_info[index]
        img = Image.open(img_path).convert('RGB')     # 0~255
        img = self.transform_tensor(img)   # 在这里做transform，转为tensor等等
        return img

    def get_i_without_transform(self, index):
        img_path = self.data_info[index]
        img = Image.open(img_path).convert('RGB')     # 0~255
        return img

    def __len__(self):
        return len(self.data_info)

    @staticmethod
    def get_img_info(data_dir):
        data_info = list()
        img_names = os.listdir(data_dir)
        for i in range(len(img_names)):
            img_name = img_names[i]
            img_path = os.path.join(data_dir, img_name)
            data_info.append(img_path)
        return data_info

    def img_show(self,index):
        img=self.__getitem__(index)
        transform_convert(img).show()

    def img_save(self,index,folder_path):
        img=self.__getitem__(index)
        transform_convert_save(img,self.transform_tensor,folder_path,str(index)+'.jpg')

    def return_transform_tensor(self):
        return self.transform_tensor



def transform_convert(ori_img_tensor):
    """
    tensor2img
    param img_tensor: tensor
    param transforms: torchvision.transforms
    """

    img_tensor = ori_img_tensor.clone()
    transform= transforms.Compose([
            transforms.Resize(224), # 缩放图片(Image)，保持长宽比不变，最短边为224像素
            transforms.CenterCrop(224), # 从图片中间切出224*224的图片
            transforms.ToTensor(), # 将图片(Image)转成Tensor，归一化至[0, 1]（直接除以255）
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) # 常用标准化
        ])
    if 'Normalize' in str(transform):
        normal_transform = list(filter(lambda x: isinstance(x, transforms.Normalize), transform.transforms))
        mean = torch.tensor(normal_transform[0].mean, dtype=img_tensor.dtype, device=img_tensor.device)
        std = torch.tensor(normal_transform[0].std, dtype=img_tensor.dtype, device=img_tensor.device)
        img_tensor.mul_(std[:, None, None]).add_(mean[:, None, None])

    img_tensor = img_tensor.transpose(0, 2).transpose(0, 1)  # C x H x W  ---> H x W x C

    if 'ToTensor' in str(transform) or img_tensor.max() < 1:
        img_tensor = img_tensor.detach().numpy() * 255

    if isinstance(img_tensor, torch.Tensor):
        img_tensor = img_tensor.numpy()

    if img_tensor.shape[2] == 3:
        img = Image.fromarray(img_tensor.astype('uint8')).convert('RGB')
    elif img_tensor.shape[2] == 1:
        img = Image.fromarray(img_tensor.astype('uint8')).squeeze()
    else:
        raise Exception("Invalid img shape, expected 1 or 3 in axis 2, but got {}!".format(img_tensor.shape[2]))

    return img

def transform_convert_1(ori_img_tensor):
    """
    tensor2img
    param img_tensor: tensor
    param transforms: torchvision.transforms
    """

    img_tensor = ori_img_tensor.clone()
    transform= transforms.Compose([
            transforms.Resize(224), # 缩放图片(Image)，保持长宽比不变，最短边为224像素
            transforms.CenterCrop(224), # 从图片中间切出224*224的图片
            transforms.ToTensor(), # 将图片(Image)转成Tensor，归一化至[0, 1]（直接除以255）
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) # 常用标准化
        ])
    if 'Normalize' in str(transform):
        normal_transform = list(filter(lambda x: isinstance(x, transforms.Normalize), transform.transforms))
        mean = torch.tensor(normal_transform[0].mean, dtype=img_tensor.dtype, device=img_tensor.device)
        std = torch.tensor(normal_transform[0].std, dtype=img_tensor.dtype, device=img_tensor.device)
        img_tensor.mul_(std[:, None, None]).add_(mean[:, None, None])

    return img_tensor


def transform_convert_p_v(ori_img_transform_tensors):
    img_transform_tensors=ori_img_transform_tensors.clone()
    transform= transforms.Compose([
            transforms.Resize(224), # 缩放图片(Image)，保持长宽比不变，最短边为224像素
            transforms.CenterCrop(224), # 从图片中间切出224*224的图片
            transforms.ToTensor(), # 将图片(Image)转成Tensor，归一化至[0, 1]（直接除以255）
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) # 常用标准化
        ])
    for i in range(len(img_transform_tensors)):
        if 'Normalize' in str(transform):
            normal_transform = list(filter(lambda x: isinstance(x, transforms.Normalize), transform.transforms))
            mean = torch.tensor(normal_transform[0].mean, dtype=img_transform_tensors[i].dtype, device=img_transform_tensors[i].device)
            std = torch.tensor(normal_transform[0].std, dtype=img_transform_tensors[i].dtype, device=img_transform_tensors[i].device)
            img_transform_tensors[i].mul_(std[:, None, None]).add_(mean[:, None, None])

        img_transform_tensors[i] = img_transform_tensors[i] * 255
    img_transform_tensors=img_transform_tensors.byte()
    # print(img_transform_tensors)
    return img_transform_tensors


def transform_convert_s_v(ori_img_transform_tensors):
    img_transform_tensors=ori_img_transform_tensors.clone()
    transform= transforms.Compose([
            transforms.Resize(224), # 缩放图片(Image)，保持长宽比不变，最短边为224像素
            transforms.CenterCrop(224), # 从图片中间切出224*224的图片
            transforms.ToTensor(), # 将图片(Image)转成Tensor，归一化至[0, 1]（直接除以255）
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) # 常用标准化
        ])
    if 'Normalize' in str(transform):
        normal_transform = list(filter(lambda x: isinstance(x, transforms.Normalize), transform.transforms))
        mean = torch.tensor(normal_transform[0].mean, dtype=img_transform_tensors.dtype, device=img_transform_tensors.device)
        std = torch.tensor(normal_transform[0].std, dtype=img_transform_tensors.dtype, device=img_transform_tensors.device)
        img_transform_tensors.mul_(std[:, None, None]).add_(mean[:, None, None])

    img_tensor = img_transform_tensors.transpose(0, 2).transpose(0, 1)  # C x H x W  ---> H x W x C

    if isinstance(img_tensor, torch.Tensor):
        img_tensor = img_tensor.numpy()

    return img_tensor

def transform_convert_save(ori_img_tensor, transform,path,filename):
    """
    tensor2img--save
    param img_tensor: tensor
    param transforms: torchvision.transforms
    """

    img_tensor = ori_img_tensor.clone()
    if 'Normalize' in str(transform):
        normal_transform = list(filter(lambda x: isinstance(x, transforms.Normalize), transform.transforms))
        mean = torch.tensor(normal_transform[0].mean, dtype=img_tensor.dtype, device=img_tensor.device)
        std = torch.tensor(normal_transform[0].std, dtype=img_tensor.dtype, device=img_tensor.device)
        img_tensor.mul_(std[:, None, None]).add_(mean[:, None, None])


    save_path=os.path.join(path)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    torchvision.utils.save_image(img_tensor, os.path.join(save_path,filename))


def load_csv_patches_tensor(file_path,t,patch_num):
    result=[]
    for i in range(patch_num):
        patches_file_name=str(t)+'-'+str(i)+'.csv'
        patches_file_path= os.path.join(file_path,patches_file_name)
        if os.path.exists(patches_file_path):
            patch_file=open(patches_file_path, "r")
            reader = csv.reader(patch_file)
            for item in reader:
                temp = list(map(float, item))
                result.append(temp)
                break
            patch_file.close()
        else:
            break
    result = torch.tensor(result, dtype=torch.float)
    result=result.view(-1,3,224,224)

    return result

def load_csv_pair_tensor(file_path,superpixel_path,seg_num):
    file_name=os.path.splitext(os.path.basename(file_path))[0]
    # print(file_name)
    result = []
    file = open(file_path, "r")
    reader = csv.reader(file)
    for item in reader:
        temp = list(map(float, item))
        result.append(temp)
        break
    file.close()
    for i in range(seg_num):
        superpixel_file_name=file_name+'-'+str(i)+'.csv'
        superpixel_file_path= os.path.join(superpixel_path,superpixel_file_name)
        if os.path.exists(superpixel_file_path):
            superpixel_file=open(superpixel_file_path, "r")
            reader = csv.reader(superpixel_file)
            for item in reader:
                temp = list(map(float, item))
                result.append(temp)
                break
            superpixel_file.close()
        else:
            break
    result = torch.tensor(result, dtype=torch.float)
    result=result.view(-1,3,224,224)  #理论上还原形状没问题，做过小测试，正式数据没做过对比

    return result




class PSDataset(Dataset):
    def __init__(self, data_dir):
        """
        图片的patch和superpixel的Dataset
        :param data_dir: str, 数据集所在路径
        """
        self.data_info = self.get_ps_info(data_dir)

    def __getitem__(self, index):
        result = []
        ps_file_path = self.data_info[index]
        ps_file = open(ps_file_path, "r")
        reader = csv.reader(ps_file)
        for item in reader:
            temp = list(map(float, item))
            result.append(temp)
        ps_file.close()
        result=torch.tensor(result)
        return result

    def __len__(self):
        return len(self.data_info)

    @staticmethod
    def get_ps_info(data_dir):
        data_info = list()
        ps_names = os.listdir(data_dir)
        for ps_name in ps_names:
            ps_path = os.path.join(data_dir, ps_name)
            data_info.append(ps_path)
        return data_info






def read_csv_normal(path):
    result = []
    ps_file = open(path, "r")
    reader = csv.reader(ps_file)
    for item in reader:
        temp = list(map(float, item))
        result.append(temp)
    ps_file.close()
    result=torch.tensor(result)
    return result



def load_mask_component(file_path, image_id, patch_num, seg_num):
    result = []

    for i in range(patch_num):
        for j in range(seg_num):
            mask_file_name=str(image_id)+'-'+str(i)+'-'+str(j)+'.csv'
            mask_file_path= os.path.join(file_path,mask_file_name)
            if os.path.exists(mask_file_path):
                mask_file=open(mask_file_path, "r")
                reader = csv.reader(mask_file)
                for item in reader:
                    temp = list(map(float, item))
                    result.append(temp)
                    break
                mask_file.close()
            else:
                break
    result = torch.tensor(result, dtype=torch.float)
    result=result.view(-1,224,224)  #理论上还原形状没问题，做过小测试

    return result


def load_mask_object(file_path,image_id,patch_num):
    result = []
    for i in range(patch_num):
        mask_file_name=str(image_id)+'-'+str(i)+'.csv'
        mask_file_path= os.path.join(file_path,mask_file_name)
        if os.path.exists(mask_file_path):
            mask_file=open(mask_file_path, "r")
            reader = csv.reader(mask_file)
            for item in reader:
                temp = list(map(float, item))
                result.append(temp)
                break
            mask_file.close()
        else:
            break
    result = torch.tensor(result, dtype=torch.float)
    result=result.view(-1,224,224)  #理论上还原形状没问题，做过小测试

    return result


def read_csv_int(path):
    ps_file = open(path, "r")
    reader = csv.reader(ps_file)
    for item in reader:
        temp = list(map(float, item))
        temp = list(map(int, temp))
        return temp


def read_csv_np(path):
    result = []
    ps_file = open(path, "r")
    reader = csv.reader(ps_file)
    for item in reader:
        temp = list(map(float, item))
        result.append(temp)
        break
    ps_file.close()
    result=np.array(result)
    result=result.flatten()
    # print(result.shape)
    return result


def get_start_and_end(list_i,num):
    result=np.where(np.array(list_i)==num)
    return result[0][0],result[0][-1]

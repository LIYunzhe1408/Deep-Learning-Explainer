import torch
from torch import nn
import torch.nn.functional as F
import numpy as np
import os
import torchvision.models as models

class HRE(nn.Module):

    def __init__(self, dim_in, dim_mid):
        super(HRE, self).__init__()
        self.dim_in = dim_in
        # self.dim_out = dim_out
        self.dim_mid = dim_mid
        # 定义编码器
        self.Encoder = nn.Sequential(
            nn.Linear(self.dim_in, int(self.dim_in/2)),
            nn.Linear(int(self.dim_in/2), int(self.dim_in/4)),
            nn.Linear(int(self.dim_in/4), self.dim_mid),

        )
        # 定义解码器
        self.Decoder = nn.Sequential(
            nn.Linear(self.dim_mid, int(self.dim_in/4)),
            nn.Linear(int(self.dim_in / 4),int( self.dim_in / 2)),
            nn.Linear(int(self.dim_in/2), self.dim_in),
        )

    def forward(self, input):


        code =self.Encoder(input)

        # high_layer_code=code[0]
        low_layer_code_sum=code[1]
        for i in range(2,len(code)):
            low_layer_code_sum=low_layer_code_sum+code[i]

        output = self.Decoder(code)
        low_layer_code_sum_out= self.Decoder(low_layer_code_sum)


        return code, output,low_layer_code_sum_out

class HRE_DEEP(nn.Module):

    def __init__(self, dim_in, dim_mid):
        super(HRE_DEEP, self).__init__()
        self.dim_in = dim_in
        # self.dim_out = dim_out
        self.dim_mid = dim_mid
        # 定义编码器
        self.Encoder = nn.Sequential(
            nn.Linear(self.dim_in, int(self.dim_in / 2)),
            # nn.ReLU(),
            nn.Linear(int(self.dim_in / 2), int(self.dim_in / 4)),
            # nn.ReLU(),
            nn.Linear(int(self.dim_in / 4), int(self.dim_in / 8)),
            nn.Linear(int(self.dim_in / 8), self.dim_mid),


        )
        # 定义解码器
        self.Decoder = nn.Sequential(
            nn.Linear(self.dim_mid, int(self.dim_in / 8)),
            nn.Linear(int(self.dim_in / 8), int(self.dim_in / 4)),
            # nn.ReLU(),
            nn.Linear(int(self.dim_in / 4), int(self.dim_in / 2)),
            # nn.ReLU(),
            nn.Linear(int(self.dim_in / 2), self.dim_in),
        )

    def forward(self, input):
        code = self.Encoder(input)

        low_layer_code_sum = code[1]
        for i in range(2, len(code)):
            low_layer_code_sum = low_layer_code_sum + code[i]

        output = self.Decoder(code)
        low_layer_code_sum_out = self.Decoder(low_layer_code_sum)

        return code, output, low_layer_code_sum_out


# class HREEM0(nn.Module):
#
#     def __init__(self):
#         super(HREEM0, self).__init__()
#         googlenet = models.googlenet(pretrained=True)
#         HRE_model = torch.load(os.path.join('./model_save/HRE-ips.pth'))  # 加载模型
#         self.Decoder=HRE_model.Decoder
#         self.dropout=googlenet.dropout
#         self.fc=googlenet.fc
#
#
#     def forward(self, input):
#         code=self.Decoder(input)
#         code=self.dropout(code)
#         code=self.fc(code)
#         return code

class HREEM1_googlenet(nn.Module):

    def __init__(self,hre_model_path):
        super(HREEM1_googlenet, self).__init__()
        googlenet = models.googlenet(pretrained=True)
        HRE_model = torch.load(os.path.join(hre_model_path,'HRE-ips.pth'))  # 加载模型
        self.Decoder=HRE_model.Decoder
        self.dropout=googlenet.dropout
        self.fc=googlenet.fc


    def forward(self, input):
        code=self.Decoder(input)
        code=self.dropout(code)
        code=self.fc(code)
        return code

class HREEM1_resnet101(nn.Module):

    def __init__(self,hre_model_path):
        super(HREEM1_resnet101, self).__init__()
        resnet101 = models.resnet101(pretrained=True)
        HRE_model =  torch.load(os.path.join(hre_model_path,'HRE-ips.pth'))  # 加载模型
        self.Decoder=HRE_model.Decoder
        self.fc=resnet101.fc


    def forward(self, input):
        code=self.Decoder(input)
        code=self.fc(code)
        return code




class HREEM1_inception_v3(nn.Module):

    def __init__(self,hre_model_path):
        super(HREEM1_inception_v3, self).__init__()
        inception_v3 = models.inception_v3(pretrained=True)
        HRE_model =  torch.load(os.path.join(hre_model_path,'HRE-ips.pth'))  # 加载模型
        self.Decoder=HRE_model.Decoder
        self.dropout=inception_v3.dropout
        self.fc=inception_v3.fc


    def forward(self, input):
        code=self.Decoder(input)
        code=self.dropout(code)
        code=self.fc(code)
        return code

class HREEM1_alexnet(nn.Module):

    def __init__(self,hre_model_path):
        super(HREEM1_alexnet, self).__init__()
        alexnet = models.alexnet(pretrained=True)
        HRE_model =  torch.load(os.path.join(hre_model_path,'HRE-ips.pth'))  # 加载模型
        self.Decoder=HRE_model.Decoder
        self.classifier=alexnet.classifier


    def forward(self, input):
        code=self.Decoder(input)
        code=self.classifier(code)
        return code



class HREEM1_densenet121(nn.Module):

    def __init__(self,hre_model_path):
        super(HREEM1_densenet121, self).__init__()
        densenet121 = models.densenet121(pretrained=True)
        HRE_model = torch.load(os.path.join(hre_model_path,'HRE-ips.pth'))  # 加载模型
        self.Decoder=HRE_model.Decoder
        self.classifier=densenet121.classifier


    def forward(self, input):
        code=self.Decoder(input)
        code=self.classifier(code)
        return code

class HREEM1_efficientnet_b0(nn.Module):

    def __init__(self,hre_model_path):
        super(HREEM1_efficientnet_b0, self).__init__()
        efficientnet_b0 = models.efficientnet_b0(pretrained=True)
        HRE_model = torch.load(os.path.join(hre_model_path,'HRE-ips.pth'))  # 加载模型
        self.Decoder=HRE_model.Decoder
        self.classifier=efficientnet_b0.classifier

    def forward(self, input):
        code=self.Decoder(input)
        code=self.classifier(code)
        return code


class HREEM1_vit_b_16(nn.Module):

    def __init__(self,hre_model_path):
        super(HREEM1_vit_b_16, self).__init__()
        vit_b_16 = models.vit_b_16(pretrained=True)
        HRE_model = torch.load(os.path.join(hre_model_path,'HRE-ips.pth'))  # 加载模型
        self.Decoder=HRE_model.Decoder
        self.classifier=vit_b_16.heads

    def forward(self, input):
        code=self.Decoder(input)
        code=self.classifier(code)
        return code





def loss_function_old(input_raw, input_reconstruction, mid_code,dim,classify_model,code_sum_out):
    """
    重构损失、一致性损失
    层次关系包含损失
    """
    #
    # reconstruction loss:  value+direction
    rec_loss_1 = F.mse_loss(input_raw, input_reconstruction)
    # rec_loss_1 = F.pairwise_distance(input_raw, input_reconstruction,p=2)

    # print(rec_loss_1,rec_loss_2)
    # print(rec_loss_1.mean(),rec_loss_2.mean())
    # rec_loss=rec_loss_1.mean()-rec_loss_2.mean()
    # rec_loss_2_all  =F.cosine_similarity(input_raw, input_reconstruction)
    # rec_loss_2=(rec_loss_2_all.mean()-(-1))/2-1  # 从-1,1归一化到-1，0
    # rec_loss=rec_loss_1-rec_loss_2
    rec_loss =rec_loss_1*10  # mse已经足够好了，对于重构

    # consistency loss  #
    # input_raw_result=classify_model(input_raw)[:,dim]
    # input_reconstruction_result=classify_model(input_reconstruction)[:,dim]
    # consistency_loss1 = F.mse_loss(input_raw_result, input_reconstruction_result)  # 只用logit算mse从sscsdc结果看会使概念得到强化，背离了一致性
    input_raw_result=F.softmax(classify_model(input_raw),dim=1)
    input_reconstruction_result = classify_model(input_reconstruction)
    consistency_loss2=F.cross_entropy(input_reconstruction_result,input_raw_result)
    # input_raw_logit=classify_model(input_raw)
    # input_reconstruction_logit = classify_model(input_reconstruction)
    # consistency_loss3=F.mse_loss(input_raw_logit,input_reconstruction_logit)
    # # new
    # consistency_loss=consistency_loss2+consistency_loss3  # 保持模型性能不变，logit尽量不变
    consistency_loss=consistency_loss2

    # hierarchical relationship loss:
    mid_high=mid_code[0]
    mid_low_sum=mid_code[1]
    for i in range(2,len(mid_code)):
        mid_low_sum=mid_low_sum+mid_code[i]
    #
    # # mid_patch_k=mid_patch.unsqueeze(0)
    # # mid_superpixel_sum_k=mid_superpixel_sum.unsqueeze(0)
    # # hr_loss_0 = F.pairwise_distance(mid_patch_k, mid_superpixel_sum_k,p=2)
    # hr_loss_1=F.l1_loss(mid_high,mid_low_sum)
    hr_loss_1=F.mse_loss(mid_high,mid_low_sum)

    # # hr_loss_2=F.cosine_similarity(mid_patch, mid_superpixel_sum,dim=0)
    # # hr_loss_2=(hr_loss_2-(-1))/2-1
    # # hr_loss=hr_loss_0+hr_loss_1-hr_loss_2
    # high_reconstruction_result=classify_model(input_reconstruction[0])[dim]
    # code_reconstruction_result=classify_model(code_sum_out)[dim]
    # hr_loss_3 = F.l1_loss(high_reconstruction_result, code_reconstruction_result)  # Consistency loss

    # 不管残差，考虑加起来的相似性和一致性
    # hr_loss = hr_loss_1+hr_loss_3
    hr_loss=hr_loss_1*100  #

    # residual_loss
    # residual_loss_1=F.l1_loss(residual_code,torch.zeros(residual_code.shape))
    # residual_out_result=classify_model(residual_out)[dim]
    # residual_loss_2=F.l1_loss(residual_out_result,torch.zeros(residual_out_result.shape))
    # residual_loss=residual_loss_1+residual_loss_2
    # residual_loss=residual_loss_1


    # print(rec_loss + hr_loss)
    print(rec_loss,consistency_loss,hr_loss)
    #
    return rec_loss +consistency_loss+hr_loss
    # return rec_loss+ hr_loss


def loss_function(input_raw, input_reconstruction, mid_code,dim,classify_model,code_sum_out):
    """
    可加性损失
    重构损失
    等价性损失
    """

    # 可加性损失
    mid_high=mid_code[0]
    mid_low_sum=mid_code[1]
    for i in range(2,len(mid_code)):
        mid_low_sum=mid_low_sum+mid_code[i]
    additivity_loss=F.mse_loss(mid_high,mid_low_sum)

    # 重构损失
    input_raw_result=F.softmax(classify_model(input_raw),dim=1)
    input_reconstruction_result =F.log_softmax(classify_model(input_reconstruction),dim=1)
    recontrust_loss=F.kl_div(input_reconstruction_result,input_raw_result,reduction="batchmean")
    # recontrust_loss = F.kl_div(input_reconstruction_result, input_raw_result)

    # 等价性损失
    input_e=F.log_softmax(classify_model(code_sum_out),dim=0)
    target_e=F.softmax(classify_model(input_reconstruction[0]),dim=0)
    equivalence_loss= F.kl_div(input_e.unsqueeze(0), target_e.unsqueeze(0),reduction="batchmean")

    loss=additivity_loss+recontrust_loss+equivalence_loss
    return loss


def model_save(model,path):
    if not os.path.exists(path):
        os.makedirs(path)
    filename='HRE-ips.pth'
    pre_file = os.path.join(path,filename)
    if os.path.exists(pre_file):
        os.remove(pre_file)
    model=model.to("cpu")
    torch.save(model, os.path.join(path, filename))

def print_model_params(model):
    for k, v in model.named_parameters():
        print(k,v)



# def prepare_model_param(HREEM_model):
#     googlenet = models.googlenet(pretrained=True)
#     pretrained_dict1 = googlenet.state_dict()
#     HRE_model = torch.load(os.path.join('./model_save/HRE.pth'))  # 加载模型
#     pretrained_dict2 = HRE_model.state_dict()
#     model_dict = HREEM_model.state_dict()
#     pretrained_dict1 = {k: v for k, v in pretrained_dict1.items() if k in model_dict}
#     pretrained_dict2 = {k: v for k, v in pretrained_dict2.items() if k in model_dict}
#     pretrained_dict={}
#     pretrained_dict.update(pretrained_dict2)
#     pretrained_dict.update(pretrained_dict1)
#     return pretrained_dict


# test
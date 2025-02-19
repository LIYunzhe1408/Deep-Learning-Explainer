from torchvision.utils import draw_segmentation_masks
import torch
import numpy as np
import matplotlib.pyplot as plt
import torchvision.transforms.functional as F
import os
from skimage.segmentation import mark_boundaries
import shap
import torch.nn.functional as FF
import picture as dp
from utils.data_operation import transform_convert_p_v, transform_convert_s_v, transform_convert_1


def show(imgs):
    if not isinstance(imgs, list):
        imgs = [imgs]
    fix, axs = plt.subplots(ncols=len(imgs), squeeze=False)
    for i, img in enumerate(imgs):
        img = img.detach()
        img = F.to_pil_image(img)
        axs[0, i].imshow(np.asarray(img))
        axs[0, i].set(xticklabels=[], yticklabels=[], xticks=[], yticks=[])


def patches_vis(data,mask,i,path):
    plt.rcParams["savefig.bbox"] = 'tight'
    class_dim = 1
    num_classes=21  # 预训练模型固定参数
    all_classes_masks = mask.argmax(class_dim) == torch.arange(num_classes)[:, None, None, None]
    # The first dimension is the classes now, so we need to swap it
    all_classes_masks = all_classes_masks.swapaxes(0, 1)
    patches_with_masks = [
        draw_segmentation_masks(img, masks=mask, alpha=.6)
        for img, mask in zip(transform_convert_p_v(data), all_classes_masks)
    ]
    show(patches_with_masks)
    # plt.show()
    folder_path = os.path.join(path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    plt.savefig(os.path.join(folder_path,str(i)+'.jpg'),dpi = 1000, pad_inches=-0.1)
    plt.clf()
    plt.close()


def superpixel_vis(data,mask,order,path):
    plt.rcParams["savefig.bbox"] = 'tight'
    mask=mask.int().numpy()
    plt.imshow(mark_boundaries(transform_convert_s_v(data), mask))
    # plt.show()
    folder_path = os.path.join(path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    plt.axis('off')
    plt.savefig(os.path.join(folder_path,str(order)+'.jpg'),dpi = 1000, pad_inches=-0.1)
    plt.clf()  # 清除当前 figure 的所有axes，但是不关闭这个 window，所以能继续复用于其他的 plot。
    plt.close()  # 关闭 window，如果没有指定，则指当前 window。


def result_heatmap(masks, con_t, data,folder_path,filename):
    max_score=max(con_t)
    con_t=con_t/max_score
    a=torch.zeros(224,224)
    for i in range(len(masks)):
        a=a+masks[i]*con_t[i]
    a=a.view(1,224,224)
    # a = torch.cat((a, a, a), dim=0)
    a = a.numpy()
    a = np.transpose(a, (1, 2, 0))
    X=transform_convert_1(data.view(3,224,224))
    X = X.numpy()
    X=np.transpose(X,(1,2,0))
    # shap.image_plot(a, X)
    print(a.shape, X.shape)

    # 没法单拉一个函数，去掉a或者x，看报错点
    shap.image_plot(shap_values=a, pixel_values=X, hspace='auto', show=False)
    plt.savefig(os.path.join(folder_path,filename+'.jpg'), pad_inches=-0.1)
    plt.clf()
    plt.close()


def result_ssc(HREEM_model1,tensor_ssc_sdc,cal_out_dim,sort_list,image_tensor):
    out_image = FF.softmax(HREEM_model1(image_tensor).detach(),dim=0).numpy().tolist()
    out_image_prob=out_image[cal_out_dim]
    print(out_image_prob)
    # add--most-important
    add_list1=[]
    add_list1.append(0)
    j=-1
    ssc_most_important_add = torch.zeros(tensor_ssc_sdc[sort_list[j]].shape)
    for i in range(5):
        ssc_most_important_add = ssc_most_important_add + tensor_ssc_sdc[sort_list[j]]
        out=FF.softmax(HREEM_model1(ssc_most_important_add).detach(),dim=0)
        # print(out.shape)
        add_list1.append(out[cal_out_dim])
        j=j-1

    add_list1=torch.tensor(add_list1).view(-1).numpy()
    add_list1=add_list1/out_image_prob
    add_list1=add_list1.tolist()
    print('add--most-important:',add_list1)
    # add--least important
    add_list2=[]
    add_list2.append(0)
    j=0
    ssc_least_important_add = torch.zeros(tensor_ssc_sdc[sort_list[j]].shape)
    for i in range(5):
        ssc_least_important_add = ssc_least_important_add + tensor_ssc_sdc[sort_list[j]]
        out=FF.softmax(HREEM_model1(ssc_least_important_add).detach(),dim=0)
        add_list2.append(out[cal_out_dim])
        j=j+1
    add_list2=torch.tensor(add_list2).view(-1).numpy()
    add_list2=add_list2/out_image_prob
    add_list2=add_list2.tolist()
    print('add--least important:',add_list2)
    dp.drawPicture(len(add_list1),add_list1,add_list2)

def result_sdc(HREEM_model1,tensor_ssc_sdc,cal_out_dim,sort_list,image_tensor):
    out_image = FF.softmax(HREEM_model1(image_tensor).detach(),dim=0).numpy().tolist()
    out_image_prob = out_image[cal_out_dim]
    # sub--most-important
    sub_list1=[]
    sub_list1.append(out_image_prob)
    j=-1
    sdc_most_important_sub = image_tensor.clone()
    for i in range(5):
        sdc_most_important_sub=sdc_most_important_sub-tensor_ssc_sdc[sort_list[j]]
        out=FF.softmax(HREEM_model1(sdc_most_important_sub).detach(),dim=0)
        sub_list1.append(out[cal_out_dim])
        j=j-1
    sub_list1=torch.tensor(sub_list1).view(-1).numpy()
    sub_list1=sub_list1/out_image_prob
    sub_list1=sub_list1.tolist()
    print('sub--most-important:',sub_list1)
    # sub--least-important
    sub_list2=[]
    sub_list2.append(out_image_prob)
    j=0
    sdc_least_important_sub = image_tensor.clone()
    for i in range(5):
        sdc_least_important_sub=sdc_least_important_sub-tensor_ssc_sdc[sort_list[j]]
        out=FF.softmax(HREEM_model1(sdc_least_important_sub).detach(),dim=0)
        sub_list2.append(out[cal_out_dim])
        j=j+1
    sub_list2=torch.tensor(sub_list2).view(-1).numpy()
    sub_list2=sub_list2/out_image_prob
    sub_list2=sub_list2.tolist()
    print('sub--least-important:',sub_list2)
    dp.drawPicture(len(sub_list1),sub_list1,sub_list2)





def ssc_concept_consistency(HREEM_model1,tensor_ssc_sdc,image_tensor,class_dim,sort_concept_list,cluser_label,concept_num):
    out_image = FF.softmax(HREEM_model1(image_tensor).detach(),dim=0).numpy().tolist()
    out_image_prob=out_image[class_dim]
    print(out_image_prob)
    # add--most-important
    add_list1= [0]
    j=-1
    ssc_most_important_add = torch.zeros(tensor_ssc_sdc[0].shape)
    if len(sort_concept_list)<concept_num:
        concept_num=len(sort_concept_list)
    for i in range(concept_num):
        for k in range(len(cluser_label)):
            if cluser_label[k]==sort_concept_list[j]:
                ssc_most_important_add = ssc_most_important_add + tensor_ssc_sdc[k]
        out=FF.softmax(HREEM_model1(ssc_most_important_add).detach(),dim=0)
        # print(out.shape)
        add_list1.append(out[class_dim])
        j=j-1

    add_list1=torch.tensor(add_list1).view(-1).numpy()
    add_list1=add_list1/out_image_prob
    add_list1=add_list1.tolist()
    print('add--most-important:',add_list1)
    sscc=0
    sscc_list=[]
    for k in range(1,len(add_list1)):
        sscc_list.append(add_list1[k]-add_list1[k-1])
    for t in range(len(sscc_list)-1):
        if sscc_list[t]>sscc_list[t+1]:
            sscc=sscc+1
    sscc=sscc/(concept_num-1)
    print('sscc:',sscc)


    # # add--least important
    # add_list2= [0]
    # j=0
    # ssc_least_important_add = torch.zeros(tensor_ssc_sdc[0].shape)
    # for i in range(concept_num):
    #     for k in range(len(cluser_label)):
    #         if cluser_label[k]==sort_concept_list[j]:
    #             ssc_least_important_add = ssc_least_important_add + tensor_ssc_sdc[k]
    #     out=FF.softmax(HREEM_model1(ssc_least_important_add).detach(),dim=0)
    #     add_list2.append(out[class_dim])
    #     j=j+1
    # add_list2=torch.tensor(add_list2).view(-1).numpy()
    # add_list2=add_list2/out_image_prob
    # add_list2=add_list2.tolist()
    # print('add--least important:',add_list2)
    # dp.drawPicture(len(add_list1),add_list1,add_list2)

    return sscc


def sdc_concept_consistency(HREEM_model1,tensor_ssc_sdc,image_tensor,class_dim,sort_concept_list,cluser_label,concept_num):
    out_image = FF.softmax(HREEM_model1(image_tensor).detach(),dim=0).numpy().tolist()
    out_image_prob = out_image[class_dim]
    # sub--most-important
    sub_list1= [out_image_prob]
    j=-1
    sdc_most_important_sub = image_tensor.clone()
    if len(sort_concept_list)<concept_num:
        concept_num=len(sort_concept_list)
    for i in range(concept_num):
        for k in range(len(cluser_label)):
            if cluser_label[k]==sort_concept_list[j]:
                sdc_most_important_sub=sdc_most_important_sub-tensor_ssc_sdc[k]
        out=FF.softmax(HREEM_model1(sdc_most_important_sub).detach(),dim=0)
        sub_list1.append(out[class_dim])
        j=j-1
    sub_list1=torch.tensor(sub_list1).view(-1).numpy()
    sub_list1=sub_list1/out_image_prob
    sub_list1=sub_list1.tolist()
    print('sub--most-important:',sub_list1)
    sdcc=0
    sdcc_list=[]
    for k in range(1,len(sub_list1)):
        sdcc_list.append(sub_list1[k]-sub_list1[k-1])
    for t in range(len(sdcc_list)-1):
        if sdcc_list[t]<sdcc_list[t+1]:
            sdcc=sdcc+1
    sdcc = sdcc / (concept_num - 1)
    print('sdcc:',sdcc)



    # # sub--least-important
    # sub_list2= [out_image_prob]
    # j=0
    # sdc_least_important_sub = image_tensor.clone()
    # for i in range(concept_num):
    #     for k in range(len(cluser_label)):
    #         if cluser_label[k]==sort_concept_list[j]:
    #             sdc_least_important_sub=sdc_least_important_sub-tensor_ssc_sdc[k]
    #     out=FF.softmax(HREEM_model1(sdc_least_important_sub).detach(),dim=0)
    #     sub_list2.append(out[class_dim])
    #     j=j+1
    # sub_list2=torch.tensor(sub_list2).view(-1).numpy()
    # sub_list2=sub_list2/out_image_prob
    # sub_list2=sub_list2.tolist()
    # print('sub--least-important:',sub_list2)
    # dp.drawPicture(len(sub_list1),sub_list1,sub_list2)

    return sdcc


def ssc_concept_consistency_mask(model,masks,image_tensor,class_dim,sort_concept_list, cluser_label,concept_num):
    out_image =  FF.softmax(model(image_tensor)[0].detach(), dim=0)
    out_image_prob=out_image[class_dim].numpy()
    print(out_image_prob)
    # add--most-important
    add_list1= [0]
    j=-1
    most_important_mask = torch.zeros([224, 224])
    if len(sort_concept_list)<concept_num:
        concept_num=len(sort_concept_list)
    for i in range(concept_num):
        for k in range(len(cluser_label)):
            if cluser_label[k]==sort_concept_list[j]:
                most_important_mask = most_important_mask + masks[k]
        most_important_mask = (most_important_mask > 0).int()
        out = FF.softmax(model(most_important_mask * image_tensor).detach(), dim=1)[0]
        # print(out.shape)
        add_list1.append(out[class_dim])
        j=j-1
    add_list1=torch.tensor(add_list1).view(-1).numpy()
    add_list1=add_list1/out_image_prob
    add_list1=add_list1.tolist()
    print('add--most-important:',add_list1)
    sscc=0
    sscc_list=[]
    for k in range(1,len(add_list1)):
        sscc_list.append(add_list1[k]-add_list1[k-1])
    for t in range(len(sscc_list)-1):
        if sscc_list[t]>sscc_list[t+1]:
            sscc=sscc+1
    sscc=sscc/(concept_num-1)
    print('sscc:',sscc)

    return sscc


def sdc_concept_consistency_mask(model,masks,image_tensor,class_dim,sort_concept_list, cluser_label,concept_num):
    out_image =  FF.softmax(model(image_tensor)[0].detach(), dim=0)
    out_image_prob=out_image[class_dim]
    print(out_image_prob)
    # sub--most-important
    sub_list1= [out_image_prob]
    j=-1
    most_important_mask=torch.zeros([224, 224])
    if len(sort_concept_list)<concept_num:
        concept_num=len(sort_concept_list)
    for i in range(concept_num):
        for k in range(len(cluser_label)):
            if cluser_label[k]==sort_concept_list[j]:
                most_important_mask=most_important_mask+masks[k]
        most_important_mask_t = most_important_mask.clone()
        most_important_mask_t = (most_important_mask_t == 0).int()
        out = FF.softmax(model(most_important_mask_t * image_tensor).detach(), dim=1)[0]
        sub_list1.append(out[class_dim])
        j=j-1
    sub_list1=torch.tensor(sub_list1).view(-1).numpy()
    sub_list1=sub_list1/out_image_prob.numpy()
    sub_list1=sub_list1.tolist()
    print('sub--most-important:',sub_list1)
    sdcc=0
    sdcc_list=[]
    for k in range(1,len(sub_list1)):
        sdcc_list.append(sub_list1[k]-sub_list1[k-1])
    for t in range(len(sdcc_list)-1):
        if sdcc_list[t]<sdcc_list[t+1]:
            sdcc=sdcc+1
    sdcc = sdcc / (concept_num - 1)
    print('sdcc:',sdcc)

    return sdcc


def ssc_concept_prob(HREEM_model1,tensor_ssc_sdc,image_tensor,sort_concept_list,cluser_label,concept_num):
    out_image = FF.softmax(HREEM_model1(image_tensor).detach(),dim=0)
    out_image_class=out_image.argmax()
    print(out_image_class)
    # add--most-important
    add_list1= []
    j=-1
    ssc_most_important_add = torch.zeros(tensor_ssc_sdc[0].shape)
    concept_num_tmp=0
    if len(sort_concept_list)<concept_num:
        concept_num_tmp= len(sort_concept_list)
    else:
        concept_num_tmp=concept_num
    for i in range(concept_num_tmp):
        for k in range(len(cluser_label)):
            if cluser_label[k]==sort_concept_list[j]:
                ssc_most_important_add = ssc_most_important_add + tensor_ssc_sdc[k]
        out=FF.softmax(HREEM_model1(ssc_most_important_add).detach(),dim=0).argmax()
        if out==out_image_class:
            add_list1.append(1)
        else:
            add_list1.append(0)
        j=j-1
    tmp_a=add_list1[-1]
    if concept_num_tmp<concept_num:
        for i in range(concept_num-concept_num_tmp):
            add_list1.append(tmp_a)
    print('add--most-important:',add_list1)

    # add--least important
    add_list2= []
    j=0
    ssc_least_important_add = torch.zeros(tensor_ssc_sdc[0].shape)
    for i in range(concept_num_tmp):
        for k in range(len(cluser_label)):
            if cluser_label[k]==sort_concept_list[j]:
                ssc_least_important_add = ssc_least_important_add + tensor_ssc_sdc[k]
        out=FF.softmax(HREEM_model1(ssc_least_important_add).detach(),dim=0).argmax()
        if out==out_image_class:
            add_list2.append(1)
        else:
            add_list2.append(0)
        j=j+1

    tmp_a=add_list2[-1]
    if concept_num_tmp<concept_num:
        for i in range(concept_num-concept_num_tmp):
            add_list2.append(tmp_a)
    print('add--least important:',add_list2)

    return add_list1,add_list2


def sdc_concept_prob(HREEM_model1,tensor_ssc_sdc,image_tensor,sort_concept_list,cluser_label,concept_num):
    out_image = FF.softmax(HREEM_model1(image_tensor).detach(),dim=0)
    out_image_class=out_image.argmax()
    print(out_image_class)
    # sub--most-important
    sub_list1= []
    j=-1
    sdc_most_important_sub = image_tensor.clone()
    concept_num_tmp=0
    if len(sort_concept_list)<concept_num:
        concept_num_tmp= len(sort_concept_list)
    else:
        concept_num_tmp=concept_num
    for i in range(concept_num_tmp):
        for k in range(len(cluser_label)):
            if cluser_label[k]==sort_concept_list[j]:
                sdc_most_important_sub=sdc_most_important_sub-tensor_ssc_sdc[k]
        out=FF.softmax(HREEM_model1(sdc_most_important_sub).detach(),dim=0).argmax()
        if out==out_image_class:
            sub_list1.append(1)
        else:
            sub_list1.append(0)
        j=j-1
    tmp_a=sub_list1[-1]
    if concept_num_tmp<concept_num:
        for i in range(concept_num-concept_num_tmp):
            sub_list1.append(tmp_a)
    print('sub--most-important:',sub_list1)

    # sub--least-important
    sub_list2= []
    j=0
    sdc_least_important_sub = image_tensor.clone()
    for i in range(concept_num_tmp):
        for k in range(len(cluser_label)):
            if cluser_label[k]==sort_concept_list[j]:
                sdc_least_important_sub=sdc_least_important_sub-tensor_ssc_sdc[k]
        out=FF.softmax(HREEM_model1(sdc_least_important_sub).detach(),dim=0).argmax()
        if out==out_image_class:
            sub_list2.append(1)
        else:
            sub_list2.append(0)
        j=j+1
    tmp_a=sub_list2[-1]
    if concept_num_tmp<concept_num:
        for i in range(concept_num-concept_num_tmp):
            sub_list2.append(tmp_a)
    print('sub--least-important:',sub_list2)

    return sub_list1,sub_list2


def ssc_concept_prob_conpect_exist(HREEM_model1,tensor_ssc_sdc,image_tensor,sort_concept_list,cluser_label,concept_num):
    out_image = FF.softmax(HREEM_model1(image_tensor).detach(),dim=0)
    out_image_class=out_image.argmax()
    print(out_image_class)
    # add--most-important
    add_list1= []
    j=-1
    ssc_most_important_add = torch.zeros(tensor_ssc_sdc[0].shape)
    i=0
    while i<concept_num and j>=-len(sort_concept_list):
        tmpt=0
        for k in range(len(cluser_label)):
            if cluser_label[k]==sort_concept_list[j]:
                ssc_most_important_add = ssc_most_important_add + tensor_ssc_sdc[k]
                tmpt=1
        if tmpt == 1:
            out=FF.softmax(HREEM_model1(ssc_most_important_add).detach(),dim=0).argmax()
            if out==out_image_class:
                add_list1.append(1)
            else:
                add_list1.append(0)
        else:
            i=i-1
        j=j-1
        i=i+1
    tmp_a=add_list1[-1]
    l_a_i=len(add_list1)
    if l_a_i<concept_num:
        for i in range(concept_num-l_a_i):
            add_list1.append(tmp_a)
    print('add--most-important:',add_list1)

    # add--least important
    add_list2= []
    j=0
    ssc_least_important_add = torch.zeros(tensor_ssc_sdc[0].shape)
    i=0
    while i<concept_num and j<len(sort_concept_list):
        tmpt=0
        for k in range(len(cluser_label)):
            if cluser_label[k]==sort_concept_list[j]:
                ssc_least_important_add = ssc_least_important_add + tensor_ssc_sdc[k]
                tmpt = 1
        if tmpt == 1:
            out=FF.softmax(HREEM_model1(ssc_least_important_add).detach(),dim=0).argmax()
            if out==out_image_class:
                add_list2.append(1)
            else:
                add_list2.append(0)
        else:
            i=i-1
        j=j+1
        i=i+1
    tmp_a=add_list2[-1]
    l_a_l=len(add_list2)
    if l_a_l<concept_num:
        for i in range(concept_num-l_a_l):
            add_list2.append(tmp_a)
    print('add--least important:',add_list2)

    return add_list1,add_list2


def sdc_concept_prob_conpect_exist(HREEM_model1,tensor_ssc_sdc,image_tensor,sort_concept_list,cluser_label,concept_num):
    out_image = FF.softmax(HREEM_model1(image_tensor).detach(),dim=0)
    out_image_class=out_image.argmax()
    print(out_image_class)
    # sub--most-important
    sub_list1= []
    j=-1
    sdc_most_important_sub = image_tensor.clone()
    i=0
    while i<concept_num and j>=-len(sort_concept_list):
        tmpt=0
        for k in range(len(cluser_label)):
            if cluser_label[k]==sort_concept_list[j]:
                sdc_most_important_sub=sdc_most_important_sub-tensor_ssc_sdc[k]
                tmpt = 1
        if tmpt == 1:
            out=FF.softmax(HREEM_model1(sdc_most_important_sub).detach(),dim=0).argmax()
            if out==out_image_class:
                sub_list1.append(1)
            else:
                sub_list1.append(0)
        else:
            i=i-1
        j=j-1
        i=i+1
    tmp_a=sub_list1[-1]
    l_s_i=len(sub_list1)
    if l_s_i<concept_num:
        for i in range(concept_num-l_s_i):
            sub_list1.append(tmp_a)
    print('sub--most-important:',sub_list1)

    # sub--least-important
    sub_list2= []
    j=0
    sdc_least_important_sub = image_tensor.clone()
    i=0
    while i<concept_num and j<len(sort_concept_list):
        tmpt=0
        for k in range(len(cluser_label)):
            if cluser_label[k]==sort_concept_list[j]:
                sdc_least_important_sub=sdc_least_important_sub-tensor_ssc_sdc[k]
                tmpt = 1
        if tmpt == 1:
            out=FF.softmax(HREEM_model1(sdc_least_important_sub).detach(),dim=0).argmax()
            if out==out_image_class:
                sub_list2.append(1)
            else:
                sub_list2.append(0)
        else:
            i=i-1
        j=j+1
        i=i+1
    tmp_a=sub_list2[-1]
    l_s_l=len(sub_list2)
    if l_s_l<concept_num:
        for i in range(concept_num-l_s_l):
            sub_list2.append(tmp_a)
    print('sub--least-important:',sub_list2)

    return sub_list1,sub_list2


def ssc_concept_prob_mask(model,masks,image_tensor,sort_concept_id, cluser_label,concept_num):
    image_out=model(image_tensor)[0].detach()
    image_out =  FF.softmax(image_out, dim=0)
    baseline = image_out.argmax()

    j=-1
    add_list1=[]
    most_important_mask=torch.zeros([224, 224])
    for i in range(concept_num):
        for k in range(len(cluser_label)):
            if cluser_label[k]==sort_concept_id[j]:
                most_important_mask=most_important_mask+masks[k]
        most_important_mask=(most_important_mask>0).int()
        out=FF.softmax(model(most_important_mask*image_tensor).detach(),dim=1)[0]
        if out.argmax() == baseline:
            add_list1.append(1)
        else:
            add_list1.append(0)
        j=j-1

    j=0
    add_list2=[]
    least_important_mask = torch.zeros([224, 224])
    for i in range(concept_num):
        for k in range(len(cluser_label)):
            if cluser_label[k]==sort_concept_id[j]:
                least_important_mask=least_important_mask+masks[k]
        least_important_mask=(least_important_mask>0).int()
        out=FF.softmax(model(least_important_mask*image_tensor).detach(),dim=1)[0]
        if out.argmax() == baseline:
            add_list2.append(1)
        else:
            add_list2.append(0)
        j=j+1
    print(add_list1,add_list2)
    return add_list1,add_list2


def sdc_concept_prob_mask(model,masks,image_tensor,sort_concept_id, cluser_label,concept_num):
    image_out =  FF.softmax(model(image_tensor)[0].detach(), dim=0)
    baseline = image_out.argmax()

    j=-1
    sub_list1=[]
    most_important_mask=torch.zeros([224, 224])
    for i in range(concept_num):
        for k in range(len(cluser_label)):
            if cluser_label[k]==sort_concept_id[j]:
                most_important_mask=most_important_mask+masks[k]
        most_important_mask_t=most_important_mask.clone()
        most_important_mask_t=(most_important_mask_t==0).int()
        out=FF.softmax(model(most_important_mask_t*image_tensor).detach(),dim=1)[0]
        if out.argmax() == baseline:
            sub_list1.append(1)
        else:
            sub_list1.append(0)
        j=j-1

    sub_list2=[]
    j=0
    least_important_mask = torch.zeros([224, 224])
    for i in range(concept_num):
        for k in range(len(cluser_label)):
            if cluser_label[k]==sort_concept_id[j]:
                least_important_mask=least_important_mask+masks[k]
        least_important_mask_t=least_important_mask.clone()
        least_important_mask_t=(least_important_mask_t==0).int()
        out=FF.softmax(model(least_important_mask_t*image_tensor).detach(),dim=1)[0]
        if out.argmax() == baseline:
            sub_list2.append(1)
        else:
            sub_list2.append(0)
        j=j+1
    print(sub_list1, sub_list2)
    return sub_list1, sub_list2


def ssc_concept_prob_mask_conpect_exist(model,masks,image_tensor,sort_concept_id, cluser_label,concept_num):
    image_out=model(image_tensor)[0].detach()
    image_out =  FF.softmax(image_out, dim=0)
    baseline = image_out.argmax()

    j=-1
    add_list1=[]
    most_important_mask=torch.zeros([224, 224])
    i=0
    while i<concept_num and j>=-len(sort_concept_id):
        tmpt=0
        for k in range(len(cluser_label)):
            if cluser_label[k]==sort_concept_id[j]:
                most_important_mask=most_important_mask+masks[k]
                tmpt=1
        if tmpt == 1:
            most_important_mask=(most_important_mask>0).int()
            out=FF.softmax(model(most_important_mask*image_tensor).detach(),dim=1)[0]
            if out.argmax() == baseline:
                add_list1.append(1)
            else:
                add_list1.append(0)
        else:
            i=i-1
        j=j-1
        i=i+1
    tmp_a=add_list1[-1]
    l_a_i=len(add_list1)
    if l_a_i<concept_num:
        for i in range(concept_num-l_a_i):
            add_list1.append(tmp_a)
    j=0
    add_list2=[]
    least_important_mask = torch.zeros([224, 224])
    i=0
    while i<concept_num and j<len(sort_concept_id):
        tmpt=0
        for k in range(len(cluser_label)):
            if cluser_label[k]==sort_concept_id[j]:
                least_important_mask=least_important_mask+masks[k]
                tmpt = 1
        if tmpt == 1:
            least_important_mask=(least_important_mask>0).int()
            out=FF.softmax(model(least_important_mask*image_tensor).detach(),dim=1)[0]
            if out.argmax() == baseline:
                add_list2.append(1)
            else:
                add_list2.append(0)
        else:
            i=i-1
        j=j+1
        i=i+1
    tmp_a=add_list2[-1]
    l_a_l=len(add_list2)
    if l_a_l<concept_num:
        for i in range(concept_num-l_a_l):
            add_list2.append(tmp_a)
    print(add_list1,add_list2)
    return add_list1,add_list2


def sdc_concept_prob_mask_conpect_exist(model,masks,image_tensor,sort_concept_id, cluser_label,concept_num):
    image_out =  FF.softmax(model(image_tensor)[0].detach(), dim=0)
    baseline = image_out.argmax()

    j=-1
    sub_list1=[]
    most_important_mask=torch.zeros([224, 224])
    i=0
    while i<concept_num and j>=-len(sort_concept_id):
        tmpt=0
        for k in range(len(cluser_label)):
            if cluser_label[k]==sort_concept_id[j]:
                most_important_mask=most_important_mask+masks[k]
                tmpt = 1
        if tmpt == 1:
            most_important_mask_t=most_important_mask.clone()
            most_important_mask_t=(most_important_mask_t==0).int()
            out=FF.softmax(model(most_important_mask_t*image_tensor).detach(),dim=1)[0]
            if out.argmax() == baseline:
                sub_list1.append(1)
            else:
                sub_list1.append(0)
        else:
            i = i - 1
        j = j - 1
        i = i + 1
    tmp_a = sub_list1[-1]
    l_s_i = len(sub_list1)
    if l_s_i < concept_num:
        for i in range(concept_num - l_s_i):
            sub_list1.append(tmp_a)

    sub_list2=[]
    j=0
    least_important_mask = torch.zeros([224, 224])
    i=0
    while i<concept_num and j<len(sort_concept_id):
        tmpt=0
        for k in range(len(cluser_label)):
            if cluser_label[k]==sort_concept_id[j]:
                least_important_mask=least_important_mask+masks[k]
                tmpt = 1
        if tmpt == 1:
            least_important_mask_t=least_important_mask.clone()
            least_important_mask_t=(least_important_mask_t==0).int()
            out=FF.softmax(model(least_important_mask_t*image_tensor).detach(),dim=1)[0]
            if out.argmax() == baseline:
                sub_list2.append(1)
            else:
                sub_list2.append(0)
        else:
            i = i - 1
        j = j + 1
        i = i + 1
    tmp_a = sub_list2[-1]
    l_s_l = len(sub_list2)
    if l_s_l < concept_num:
        for i in range(concept_num - l_s_l):
            sub_list2.append(tmp_a)
    print(sub_list1, sub_list2)
    return sub_list1, sub_list2

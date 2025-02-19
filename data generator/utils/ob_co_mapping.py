import argparse
import os
import sys
from utils.data_operation import read_csv_int, get_start_and_end


def run_ob_co_mapping(pathManager, configuration):
    # ob------------------------------------------------------
    # 加载ob级别图片的所属概念信息
    label = read_csv_int(os.path.join(pathManager.dir_cal_cluster_path, 'cluster_ob.csv'))
    list_i = []
    ob_list=[]
    for i in range(50):
        for j in range(configuration["patch_num"]):
            fn=str(i)+'-'+str(j)+'.csv'
            if os.path.exists(os.path.join(pathManager.dir_cal_image_ob_mask_path,fn)):
                list_i.append(i)
                if i==configuration["img_num"]:
                    ob_list.append(str(i)+'-'+str(j))
            else:
                break


    # 获取序号图片的ob的序号
    start, end = get_start_and_end(list_i, configuration["img_num"])
    # 图片的ob的概念 #
    ob_cluser_label = label[start:end + 1]
    print('ob_cluser_label: ',ob_cluser_label)
    # 获取不重复概念编号
    ob_concept_list = list(set(label[start:end + 1]))
    print('不重复ob概念编号:', ob_concept_list)


    # co------------------------------------------------------

    # 加载co级别图片的所属概念信息
    label = read_csv_int(os.path.join(pathManager.dir_cal_cluster_path, 'cluster_co.csv'))
    list_i = read_csv_int(os.path.join(pathManager.dir_cal_cluster_path, 'image_id.csv'))
    # 获取序号图片的co的序号
    start, end = get_start_and_end(list_i, configuration["img_num"])
    # print(start, end)
    # 图片的co的概念 #
    co_cluser_label = label[start:end + 1]
    print('co_cluser_label: ',co_cluser_label)
    # # 获取不重复概念编号
    # co_concept_list = list(set(label[start:end + 1]))
    # print('不重复co概念编号:', co_concept_list)

    co_list=[]
    for i in range(configuration["patch_num"]):
        for j in range(configuration["seg_num"]):
            fn=str(configuration["img_num"])+'-'+str(i)+'-'+str(j)+'.csv'
            if os.path.exists(os.path.join(pathManager.dir_cal_image_co_mask_path,fn)):
                co_list.append(str(configuration["img_num"])+'-'+str(i)+'-'+str(j))
            else:
                break

    # mapping-------------------------------------------------
    ob_co_images = {}
    for i in range(len(ob_concept_list)):
        ob_i_colist=[]
        ob_i_list=[]
        for j in range(len(ob_cluser_label)):
            if ob_cluser_label[j]==ob_concept_list[i]:
                ob_i_list.append(ob_list[j])
        for j in range(len(ob_i_list)):
            for k in range(len(co_list)):
                if co_list[k].startswith(ob_i_list[j]+'-'):
                    ob_i_colist.append(co_cluser_label[k])
        ob_i_co=list(set(ob_i_colist))
        print('ob concept: ',ob_concept_list[i],' 下属 co concepts: ',ob_i_co)
        ob_co_images.update({ob_concept_list[i]: ob_i_co})


    local_explanation_path = os.path.join(pathManager.dir_ob_co_each_image, str(configuration["img_num"]), "localExplanation.txt")
    if isinstance(ob_co_images, str):
        ob_co_images = eval(ob_co_images)
    with open(local_explanation_path, 'w', encoding='utf-8') as f:
        f.write(str(ob_co_images))  # dict to str
    with open(local_explanation_path, 'r', encoding='utf-8') as f:
        dict_cluster = eval(f.read())  # eval
        print(dict_cluster == ob_co_images)
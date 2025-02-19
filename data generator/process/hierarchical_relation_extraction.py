from utils.data_operation import PSDataset
import numpy as np
import os
from utils.hie_model import loss_function, model_save, HRE_DEEP
import torch.optim as optim
import time
import copy
import torch


def hierarchical_relation_extraction(explained_model, device, pathManager, config, class_name):
    """
    HRM model训练过程
    概念实例层次关系建立模块
    在dnn特征提取层与分类器之间建立概念树，使用ip、ps的组合数据数据
    model保存在./model_save/class/version/model/HRE-ips.pth
    encode结果保存在./data_cal/class/version/hre_ip_code,hre_ps_code/model/...
    """

    print("空间概念树生成器训练开始")

    # def my_collate(batch):
    #     datax = [item for item in batch]
    #     return datax

    # dataset
    ip_dataSet = PSDataset(data_dir=os.path.join(pathManager.dir_data_cal_image_patch_mid_pair_tensor_path))
    ps_dataSet = PSDataset(data_dir=os.path.join(pathManager.dir_data_cal_patch_superpixel_mid_pair_tensor_path))

    ps_set = [ps_dataSet[x].to(device) for x in range(int(len(ps_dataSet)))]
    ip_set = [ip_dataSet[x].to(device) for x in range(int(len(ip_dataSet)))]

    dim_in_num = ps_dataSet[0].shape[1]
    print(dim_in_num)

    HRE_model = HRE_DEEP(dim_in=dim_in_num, dim_mid=config["model args"]["encode_dim"])
    optimizer = optim.Adam(HRE_model.parameters(), lr=config["model args"]["lr"], weight_decay=config["model args"]["weight_decay"])
    HRE_model = HRE_model.to(device)

    explained_model.eval()
    classify_model = explained_model.fc
    classify_model = classify_model.to(device).eval()

    best_epoch = 0
    min_loss = 1e10

    # train
    start = time.time()
    HRE_model.train()
    for epoch in range(config["model args"]["epochs"]):
        epoch_s_t = time.time()
        train_loss = 0.0
        for i in range(0, int(len(ps_set) / config["model args"]["ps_batch_size"])):
            batch_loss = 0.0
            optimizer.zero_grad()
            for t in range(0, config["model args"]["ps_batch_size"]):
                # print(i * args.ps_batch_size + t)
                code, output, code_sum_out = HRE_model(ps_set[i * config["model args"]["ps_batch_size"] + t])
                loss = loss_function(ps_set[i * config["model args"]["ps_batch_size"] + t], output, code, config["image chooser"][class_name]["class_dim"], classify_model,
                                     code_sum_out)
                batch_loss += loss
            train_loss += batch_loss.detach().to("cpu")
            batch_loss = batch_loss / config["model args"]["ps_batch_size"]
            # print(batch_loss)
            batch_loss.backward()
            optimizer.step()
        for i in range(0, int(len(ip_set) / config["model args"]["ps_batch_size"])):
            batch_loss = 0.0
            optimizer.zero_grad()
            for t in range(0, config["model args"]["ps_batch_size"]):
                # print(i * args.ps_batch_size + t)
                code, output, code_sum_out = HRE_model(ip_set[i * config["model args"]["ps_batch_size"] + t])
                loss = loss_function(ip_set[i * config["model args"]["ps_batch_size"] + t], output, code, config["image chooser"][class_name]["class_dim"], classify_model,
                                     code_sum_out)
                batch_loss += loss
            train_loss += batch_loss.detach().to("cpu")
            batch_loss = batch_loss / config["model args"]["ps_batch_size"]
            batch_loss.backward()
            optimizer.step()
        total_num = (len(ps_set) - (len(ps_set) % config["model args"]["ps_batch_size"])) + (
                    len(ip_set) - (len(ip_set) % config["model args"]["ps_batch_size"]))
        train_loss = train_loss / total_num
        print("epoch:", epoch, "training loss:", train_loss.numpy(), "time cost={}s".format(time.time() - epoch_s_t))

        if train_loss.numpy() < min_loss:
            min_loss = train_loss.numpy()
            best_epoch = epoch
            model_save(copy.deepcopy(HRE_model), os.path.join(pathManager.dir_model_save))

        print("best_epoch:", best_epoch, "    min_loss:", min_loss)
        if (epoch - best_epoch) > 50 and best_epoch > 50:
            break

    print("空间概念树生成器训练结束")
    end = time.time()
    print("training总时间为：{}s".format(end - start), "   loss最低epoch：", best_epoch, )

    print("概念树生成器结果保存开始")
    folder_path_ps = os.path.join(pathManager.dir_data_cal_hre_ps_code_path)
    if not os.path.exists(folder_path_ps):
        os.makedirs(folder_path_ps)
    folder_path_ip = os.path.join(pathManager.dir_data_cal_hre_ip_code_path)
    if not os.path.exists(folder_path_ip):
        os.makedirs(folder_path_ip)

    # test
    # loss = 0.0
    HRE_model = torch.load(os.path.join(pathManager.dir_model_save, 'HRE-ips.pth')).to(device).eval()  # 加载表现最好的模型
    with torch.no_grad():
        for i in range(0, len(ps_set)):
            code, output, code_sum_out = HRE_model(ps_set[i])
            # loss_s = loss_function(ps_test_set[i], output, code, args.class_dim, classify_model, code_sum_out)
            # loss += loss_s
            file_name = os.path.basename(ps_dataSet.data_info[i])
            save_path = os.path.join(folder_path_ps, file_name)
            np.savetxt(save_path, code.detach().to("cpu").numpy(), delimiter=',')
        for i in range(0, len(ip_set)):
            code, output, code_sum_out = HRE_model(ip_set[i])
            # loss_s = loss_function(ip_test_set[i], output, code, args.class_dim, classify_model, code_sum_out)
            # loss += loss_s
            file_name = os.path.basename(ip_dataSet.data_info[i])
            save_path = os.path.join(folder_path_ip, file_name)
            np.savetxt(save_path, code.detach().to("cpu").numpy(), delimiter=',')
        # print('predict loss:', loss.numpy() / (len(ps_test_set) + len(ip_test_set)))

    print("概念树生成器结果保存结束")


def run_relation_extraction(explained_model, device, pathManager, config, class_name):
    # 30s
    start_time = time.time()
    hierarchical_relation_extraction(explained_model, device, pathManager, config, class_name)
    end_time = time.time()
    execution_time = end_time - start_time
    print("函数执行时间为：", execution_time, "秒")

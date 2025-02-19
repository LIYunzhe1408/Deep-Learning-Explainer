
import copy
import torch
import math
import torch.nn.functional as F

def brgd(n):
    '''
    递归⽣成n位的⼆进制反格雷码
    :param n:
    :return:
    '''
    if n==1:
        return ["0","1"]
    L1 = brgd(n-1)
    L2 = copy.deepcopy(L1)
    L2.reverse()
    L1 = ["0" + l for l in L1]
    L2 = ["1" + l for l in L2]
    L = L1 + L2
    return L


def generate_sublist(n):
    conbine_list_str=brgd(n)
    conbine_list=[]
    for item in conbine_list_str:
        conbine_list.append(list(map(int,item)))
    return  conbine_list


def list_sum(item):
    total = 0
    for ele in range(len(item)):
        total = total + item[ele]
    return total

def weight_cal(item):
    factorial_F=math.factorial(len(item)+1)
    factorial_S=math.factorial(list_sum(item))
    factorial_F_S_1 = math.factorial(len(item)-list_sum(item))
    return factorial_S*factorial_F_S_1/factorial_F


def marginal_contribution_v(i,item,tensor_list,model,cal_out_dim,upper_tenosr):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # device=torch.device("cpu")
    i_tensor=tensor_list[i]
    if list_sum(item)==0:
        # 计算权重和v
        contribution_v=F.softmax(model(i_tensor).detach(),dim=0)[cal_out_dim]
        weight_v=weight_cal(item)
    else:
        s_tensor=torch.zeros(i_tensor.shape).to(device)
        for j in range(len(item)):
            if item[j]==1:
                if j<i:
                    s_tensor=s_tensor+tensor_list[j]
                else:
                    s_tensor=s_tensor+tensor_list[j+1]
        s_i_tensor=s_tensor+i_tensor
        # 计算权重和v
        if list_sum(item)==len(item):
            if isinstance(upper_tenosr, float):
                contribution_v=torch.tensor(upper_tenosr)-F.softmax(model(s_tensor).detach(),dim=0)[cal_out_dim].to("cpu")
            else:
                contribution_v=F.softmax(model(upper_tenosr).detach(),dim=0)[cal_out_dim]-F.softmax(model(s_tensor).detach(),dim=0)[cal_out_dim]
        else:
            contribution_v=F.softmax(model(s_i_tensor).detach(),dim=0)[cal_out_dim]-F.softmax(model(s_tensor).detach(),dim=0)[cal_out_dim]
        weight_v=weight_cal(item)


    return float(contribution_v.to("cpu"))*weight_v



def avg_contribution(i,tensor_list,model,cal_out_dim,upper_tenosr):
    if len(tensor_list)-1>0:
        conbine_list=generate_sublist(len(tensor_list)-1)
        v=0
        for item in conbine_list:
            v=v+marginal_contribution_v(i,item,tensor_list,model,cal_out_dim,upper_tenosr)
    else:
        if isinstance(upper_tenosr, float):
            v = upper_tenosr
        else:
            v = F.softmax(model(upper_tenosr).detach(),dim=0)[cal_out_dim].to("cpu")
    return float(v)


def hre_shapley_value(tensor_list,model,cal_out_dim,upper_tenosr):
    # 1、定义贡献函数，2、定义子集，3、计算，应该有同样得直接计算的
    result=[]
    for i in range(len(tensor_list)):
        result.append(avg_contribution(i,tensor_list,model,cal_out_dim,upper_tenosr))

    return result
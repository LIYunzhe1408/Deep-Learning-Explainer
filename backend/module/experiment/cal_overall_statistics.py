import csv
import os
import numpy as np

def read_csv_normal(path):
    result = []
    ps_file = open(path, "r")
    reader = csv.reader(ps_file)
    for item in reader:
        temp = list(map(float, item))
        result.append(temp)
    ps_file.close()
    return result



def sscc_sdcc_statistics(class_name, concept_num, model_name):
    result_save_path = './score_save'
    image_num = 14
    result_path = os.path.join(result_save_path, class_name, model_name)
    print(result_path)

    sscc_statistics_list = []
    sdcc_statistics_list = []

    for i in range(image_num):
        file_path = os.path.join(result_path, str(i), 'sscc_sdcc_re_' + str(concept_num) + '.csv')

        tmp = read_csv_normal(file_path)
        sscc_statistics_list.append(tmp[0][0])
        sdcc_statistics_list.append(tmp[0][1])

    sscc_statistics = sum(sscc_statistics_list)/len(sscc_statistics_list)
    sdcc_statistics = sum(sdcc_statistics_list)/len(sdcc_statistics_list)
    print('sscc_statistics,sdcc_statistics: ',sscc_statistics,sdcc_statistics)
    return sscc_statistics,sdcc_statistics



def ssc_sdc_statistics(class_name, concept_num, model_name):
    result_save_path = './score_save'
    image_num = 14
    result_path = os.path.join(result_save_path, class_name, model_name)
    print(result_path)

    #
    statistics_rate=np.zeros([4,concept_num],dtype=float)
    for i in range(image_num):
        file_path = os.path.join(result_path, str(i), 'ssc_sdc_re_ce_' + str(concept_num) + '.csv')
        tmp=read_csv_normal(file_path)
        tmp=np.array(tmp)
        statistics_rate=statistics_rate+tmp
    statistics_rate=statistics_rate/image_num

    print('statistics_rate:',statistics_rate)
    path = os.path.join(result_save_path, class_name, model_name)
    np.savetxt(os.path.join(path, 'sscsdc-re-ce-statistic.csv'), np.array(statistics_rate), delimiter=',')


def ssc_sdc_all(classlist, concept_num, model_name):
    result_save_path='./score_save'
    statistics=np.zeros([4,concept_num],dtype=float)
    for i in range(len(classlist)):
        class_name = classlist[i]
        result_path = os.path.join(result_save_path, class_name, model_name)
        path = os.path.join(result_path, 'sscsdc-re-ce-statistic.csv')
        tmp=read_csv_normal(path)
        tmp=np.array(tmp)
        statistics=statistics+tmp
    statistics=statistics/len(classlist)
    print('statistics:',statistics*0.8)

def rm_dir():
    classlist=['/tabby','/Blenheim spaniel','/sorrel','/junco','/bighorn',
               '/warplane','/pop bottle','/park bench','/motor scooter', '/ballplayer',
               '/Siamese cat','/Siberian husky','/timber wolf','/schooner', '/canoe',
               '/bulbul', '/black swan','/jeep','/police van' ,'/monitor',
               '/mountain bike', '/studio couch', '/zebra',
               '/speedboat','/groom','/albatross','/bison','/fire engine','/half track','/bullet train','/minivan']
    for i in range(len(classlist)):
        for j in range(50):
            # path=os.path.join('./result_save'+classlist[i]+'/official_version/googlenet',str(j), 'ssc_sdc_5.csv')
            # path = os.path.join('./result_save' + classlist[i] + '/official_version/googlenet', str(j), 'sscc_sdcc_5.csv')
            path = os.path.join('./result_save' + classlist[i] + '/official_version/googlenet','sscsdc-statistic.csv')
            if os.path.exists(path):
                os.remove(path)


def run_statistics(model_name, class_name):
    concept_num = 5
    sscc_sdcc_statistics(class_name, concept_num, model_name)
    ssc_sdc_statistics(class_name, concept_num, model_name)
    classlist2 =[class_name]
    ssc_sdc_all(classlist2, concept_num, model_name)
# classlist1 =['/tabby','/Blenheim spaniel','/sorrel','/junco','/bighorn',
#             '/warplane', '/pop bottle','/motor scooter', '/ballplayer','/Siamese cat',
#             '/Siberian husky','/timber wolf', '/schooner', '/canoe','/bulbul',
#             '/police van','/half track','/jeep','/park bench','/zebra',
#              '/black swan','/mountain bike','/bison','/fire engine']
#
# classlist2 =['/tabby','/Blenheim spaniel','/sorrel','/junco','/bighorn',
#             '/warplane', '/pop bottle','/motor scooter', '/ballplayer','/Siamese cat',
#             '/Siberian husky','/timber wolf', '/schooner', '/canoe','/bulbul',
#             '/police van','/half track','/jeep','/park bench','/zebra']
#
# s1=0
# s2=0
# for i in range(len(classlist1)):
#     sscc_statistics, sdcc_statistics=sscc_sdcc_statistics(classlist1[i], concept_num)
#     s1=s1+sscc_statistics
#     s2=s2+sdcc_statistics
#
# for i in range(len(classlist2)):
#     ssc_sdc_statistics(classlist2[i], concept_num)
#
# ssc_sdc_all(classlist2,concept_num)
# print(s1/len(classlist1),s2/len(classlist1))


# rm_dir()
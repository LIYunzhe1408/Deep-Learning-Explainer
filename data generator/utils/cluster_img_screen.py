import csv
import os


def generate_label_dict(csv_path, image_dir):
    csv_reader = csv.reader(open(csv_path))
    filenames = os.listdir(image_dir)
    label_dict = {}
    max_label = 0
    for row in csv_reader:
        for idx, item in enumerate(row):
            label = int(eval(item))
            filename = filenames[idx]
            label_dict.update({filename: label})
            max_label = label if label > max_label else max_label
    print(label_dict, max_label)
    return label_dict, max_label


csv_path = "../data_cal/tabby/deeplabv3/cluster_path/cluster_co.csv"
image_dir = r"../../vue/src/assets/image data/mainline/tabby/deeplabv3/superpixels"
co_dict, co_cluster_num = generate_label_dict(csv_path, image_dir)

csv_path = "../data_cal/tabby/deeplabv3/cluster_path/cluster_ob.csv"
image_dir = r"../../vue/src/assets/image data/mainline/tabby/deeplabv3/patches"
ob_dict, ob_cluster_num = generate_label_dict(csv_path, image_dir)

cluster_ob = {}
for i in range(ob_cluster_num+1):
    cluster_ob.update({i:[]})
    for key in ob_dict:
        if ob_dict[key] == i:
            cluster_ob[i].append(key)
print(cluster_ob)


cluster_co = {}
for i in range(co_cluster_num+1):
    cluster_co.update({i:[]})
    for key in co_dict:
        if co_dict[key] == i:
            cluster_co[i].append(key)
print(cluster_co)

import os
from ..utils.data_operation import IMGDataset, read_csv_normal, \
    load_mask_component, load_mask_object
from ..utils.visualization import result_heatmap
import time


def get_heatmap(pathManager, config):
    """
    图片可视化结果,保存在
    ./visualization_result/class/version/heatmap/model/...
    """

    folder_path = os.path.join(pathManager.dir_heatmap)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    dataSet = IMGDataset(data_dir=os.path.join(pathManager.dir_source_folder))
    image_id = config["img_num"]

    # component
    masks = load_mask_component(pathManager.dir_cal_image_co_mask_path, image_id, config["patch_num"], config["seg_num"])
    file_path = os.path.join(pathManager.dir_score_save, str(image_id), 'component_value.csv')
    con_t = read_csv_normal(file_path)
    con_t = con_t.view(-1)
    result_heatmap(masks, con_t, dataSet[image_id], folder_path, str(image_id) + '-c')

    # object
    masks = load_mask_object(pathManager.dir_cal_image_ob_mask_path, image_id, config["patch_num"])
    file_path = os.path.join(pathManager.dir_score_save, str(image_id), 'object_value.csv')
    con_t = read_csv_normal(file_path)
    con_t = con_t.view(-1)
    result_heatmap(masks, con_t, dataSet[image_id], folder_path, str(image_id) + '-o')


def run_heatmap(pathManager, config):
    # 1.16s
    start_time = time.time()
    get_heatmap(pathManager, config)
    end_time = time.time()
    execution_time = end_time - start_time
    print("函数执行时间为：", execution_time, "秒")


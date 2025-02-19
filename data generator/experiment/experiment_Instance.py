from process.score import run_score
from process.heatmap_generation import run_heatmap
import torch
import torchvision.models as models
import yaml
from utils.PathManager import Path
import os
import shutil
from experiment.sscc_sdcc_consistency import run_sscc_sdcc_consistency
from experiment.class_concept_score import run_class_concept_score
from experiment.ssc_sdc_probability import run_ssc_sdc_probability

def read_yaml_file(filepath):
    with open(filepath, 'r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def run_SSCC_SDCC(process_class, model_name):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    explained_model = models.googlenet(pretrained=True).to(device).eval()
    # 导入config
    configuration = read_yaml_file("./config_experiment.yaml")

    class_name, source_image_set = configuration["image chooser"][process_class]["class name"], \
                                   configuration["image chooser"][process_class]["identity"]
    pathManager = Path(class_name, model_name, source_image_set)

    for i in range(configuration["dataset_img_num"]):
        print("第" + str(i) + "张图片")
        test_img_id = i
        configuration["img_num"] = i
        run_score(explained_model, device, pathManager, configuration, class_name)
        run_heatmap(pathManager, configuration)
        run_sscc_sdcc_consistency(configuration, pathManager, test_img_id, class_name)
    # 全部图片归因完成后的类的概念重要度计算
    run_class_concept_score(configuration, pathManager)
    # 计算当前类图片的ssc和sdc
    for i in range(configuration["dataset_img_num"]):
        print("第" + str(i) + "张图片")
        test_img_id = i
        # 计算指定图片的ssc和sdc
        run_ssc_sdc_probability(configuration, pathManager, test_img_id)


    # path1 = os.path.join(pathManager.dir_cal_patch_tensor_path)
    # path2 = os.path.join(pathManager.dir_cal_superpixel_tensor_path)
    #
    # shutil.rmtree(path1)
    # shutil.rmtree(path2)
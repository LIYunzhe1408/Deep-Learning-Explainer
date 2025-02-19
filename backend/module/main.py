import shutil
import yaml
import torch
import torchvision.models as models
from .utils.PathManager import Path
from .process.two_stage_segmentation import two_stage_segmentation
from .process.concept_tensor_extraction import ob_co_tensor_extraction
from .process.hierarchical_relation_extraction import run_relation_extraction
from .process.score import run_score
from .process.heatmap_generation import run_heatmap
from .process.cluster_concept_tree import run_clustering
import os
# from experiment.experiment_Instance import run_SSCC_SDCC
# from experiment.cal_overall_statistics import run_statistics


def read_yaml_file(filepath):
    with open(filepath, 'r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def run_process(process_class, model_name, option=-1):
    # 被解释模型
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    explained_model = models.googlenet(pretrained=True).to(device).eval()

    # 导入config
    configuration = read_yaml_file("./module/config_mainline.yaml")

    class_name, source_image_set = configuration["image chooser"][process_class]["class name"], \
                                   configuration["image chooser"][process_class]["identity"]
    pathManager = Path(class_name, model_name, source_image_set)

    if option == 1:
        two_stage_segmentation(pathManager, configuration, model_name)
    elif option == 2:
        ob_co_tensor_extraction(explained_model, device, pathManager, configuration)
    # 很快~
    elif option == 3:
        run_clustering(pathManager, configuration)
    elif option == 4:
        run_relation_extraction(explained_model, device, pathManager, configuration, class_name)
    # 一张图片4分钟
    elif option == 5:
        run_score(explained_model, device, pathManager, configuration, class_name)
    elif option == 6:
        run_heatmap(pathManager, configuration)
    else:
        print("no option, please choose")

    if option == 0:
        path1 = os.path.join(pathManager.dir_cal_patch_tensor_path)
        path2 = os.path.join(pathManager.dir_cal_superpixel_tensor_path)

        shutil.rmtree(path1)
        shutil.rmtree(path2)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    process_class = "bison"

    # model_names = ["fcn", "lraspp"]
    model_name = "deeplabv3"
    run_process(process_class, model_name)


    # run_SSCC_SDCC(process_class, model_name)
    # TODO DO NOT RUN!!! 里面的path是写死的
    # run_statistics(model_name, process_class)

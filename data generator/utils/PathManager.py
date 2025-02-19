import os


# Paths
class Path:
    def __init__(self, class_name, model_name, source_image_set_id):
        self.dir_root = "../backend/data/image data/"
        self.dir_source_folder = "./dataset/" + source_image_set_id
        self.dir_model_save = "./model_save/" + class_name + "/" + model_name
        self.dir_score_save = "./score_save/" + class_name + "/" + model_name
        self.dir_class_concept_value_save = os.path.join(self.dir_score_save, "class_concept_value_path")

        self.dir_root_mainline = os.path.join(self.dir_root, "mainline", class_name, model_name)
        self.dir_handle_image = os.path.join(self.dir_root, "mainline", class_name, "handle image")
        self.dir_ob_co_each_image = os.path.join(self.dir_root, "mainline", class_name, model_name, "concept each image")
        self.dir_local_explanation = os.path.join(self.dir_root, "mainline", class_name, model_name, "localExplanation.txt")
        self.dir_cluster_image = os.path.join(self.dir_root, "mainline", class_name, model_name, "clusterImages.txt")
        self.dir_root_comparison = "../../vue/src/assets/image data/comparison"

        self.dir_patch_image, self.dir_superpixel_image, self.dir_patches, self.dir_superpixels, self.dir_heatmap = [
            os.path.join(self.dir_root_mainline, child_root) for child_root in
            ["patch-image", "superpixel-image", "patches", "superpixels", "heatmap"]]

        self.dir_data_cal_root = os.path.join("./data_cal", class_name, model_name)
        self.dir_cal_cluster_path =os.path.join(self.dir_data_cal_root, "cluster_path")
        self.dir_cal_image_ob_mask_path = os.path.join(self.dir_data_cal_root, "image_ob_mask_path")
        self.dir_cal_image_co_mask_path = os.path.join(self.dir_data_cal_root, "image_co_mask_path")
        self.dir_cal_patch_tensor_path = os.path.join(self.dir_data_cal_root, "patch_tensor")
        self.dir_cal_superpixel_tensor_path = os.path.join(self.dir_data_cal_root, "superpixel_tensor")
        self.dir_data_cal_image_patch_mid_pair_tensor_path = os.path.join(self.dir_data_cal_root, "image_patch_mid_pair_tensor")
        self.dir_data_cal_patch_superpixel_mid_pair_tensor_path = os.path.join(self.dir_data_cal_root, "patch_superpixel_mid_pair_tensor")
        self.dir_data_cal_hre_ps_code_path = os.path.join(self.dir_data_cal_root, "hre_ps_code")
        self.dir_data_cal_hre_ip_code_path = os.path.join(self.dir_data_cal_root, "hre_ip_code")


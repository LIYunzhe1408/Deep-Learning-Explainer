import os
# Paths
class Path:
    def __init__(self, class_name, model_name, source_image_set_id):
        self.dir_root = "../vue/src/assets/image data/"

        self.dir_root_mainline = os.path.join(self.dir_root, "mainline", class_name, model_name)
        self.dir_handle_image = os.path.join(self.dir_root, "mainline", class_name, "handle image")
        self.dir_root_comparison = "../vue/src/assets/image data/comparison"

        self.dir_patch_image, self.dir_superpixel_image, self.dir_patches, self.dir_superpixels = [
            os.path.join(self.dir_root_mainline, child_root) for child_root in
            ["patch-image", "superpixel-image", "patches", "superpixels"]]

        self.dir_source_folder = "./dataset/" + source_image_set_id
        self.dir_cal_image_ob_mask_path = os.path.join("./data_cal", class_name, model_name, "image_ob_mask_path")
        self.dir_cal_superpixel_tensor_path = os.path.join("./data_cal", class_name, model_name, "superpixel_tensor")
        self.dir_cal_image_co_mask_path = os.path.join("./data_cal", class_name, model_name, "image_co_mask_path")
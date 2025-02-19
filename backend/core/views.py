from django.http import JsonResponse
# from django.http import HttpResponse
import base64
import os
# import module.main as HCE
import yaml
from .models import User
from .models import Log
import time
import datetime


# Database
def addUser(request):
    """
    添加用户
    :param request:
    :return:
    """
    # 查询唯一数据
    users = User.objects.get(loggedIn='1')
    me = []
    me.append({
        "id": users.ID,
        "name": users.first_name,
        "email": users.email,
        "institution": users.institution,
        "permission": users.permission,
        "picture": encodeImage(os.path.join(os.getcwd(), users.picture if users.picture else "data/profile/logo.png"))})

    returnUsers = []

    if users.permission == "Admin":
        users = User.objects.all()
        for user in users:
            returnUsers.append({
                "id": user.ID,
                "name": user.first_name,
                "email": user.email,
                "institution": user.institution,
                "permission": user.permission})

    return JsonResponse({"admin":returnUsers, "user":me}, safe=False)


def clearLogIn(request):
    """
    重置当前登录的用户状态
    :param request:
    :return:
    """
    User.objects.filter(loggedIn='1').update(loggedIn='0')
    return JsonResponse("ok", safe=False)


def searchLog(request):
    """
    查询系统日志
    :param request:
    :return:
    """
    user_id, email = request.GET.get("user"), request.GET.get("email")
    permission = User.objects.get(id=user_id).permission
    if permission == "Admin":
        logs = Log.objects.all()
        returnLogs = []
        for log in logs:
            returnLogs.append({"id": log.ID,
                                "updateTime": log.update_time,
                                "user": log.user_name,
                                "changeLog": log.change_log})
    else:
        logs = Log.objects.filter(user_name=email)
        returnLogs = []
        for log in logs:
            returnLogs.append({"id": log.ID,
                                "updateTime": log.update_time,
                                "user": log.user_name,
                                "changeLog": log.change_log})
    print(returnLogs)
    return JsonResponse(returnLogs, safe=False)


def checkLoggedIn(request):
    """
    检查当前用户登录状态
    :param request:
    :return:
    """
    user_name, password = request.GET.get("user_name"), request.GET.get("password")

    user = User.objects.get(email=user_name)
    print(user.first_name, " ", user.password, " ", password == user.password)
    verified = user.password == password
    if verified:
        # new_user = User(first_name="Bill", last_name="Yuan", email="test", institution="UC San Diego", permission="User", password="1234", loggedIn=1)
        # new_user.save()
        User.objects.filter(email=user_name).update(loggedIn='1')
        update_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        name = user_name
        change_log = "Sign In"
        new_log = Log(update_time=update_time, user_name=name, change_log=change_log)
        new_log.save()

    time.sleep(0.5)
    return JsonResponse({"verification":verified}, safe=False)


def updateProfile(request):
    """
    更新用户个人信息
    :param request:
    :return:
    """
    user_name, email, ID = request.GET.get("name"), request.GET.get("email"), request.GET.get("id")
    User.objects.filter(id=ID).update(first_name=user_name)
    User.objects.filter(id=ID).update(email=email)
    return JsonResponse("ok", safe=False)


def deleteUser(request):
    """
    删除指定用户
    :param request:
    :return:
    """
    ID = request.GET.get("id")
    user = User.objects.get(ID=ID)
    user.delete()
    return JsonResponse("ok", safe=False)

def read_yaml_file(filepath):
    """
    Read yaml file.
    :param filepath: yaml file path
    :return: yaml object. Specifically, a dict
    """
    with open(filepath, 'r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def setLocalExplanationImagesLabel(class_name, model_name, localExplanationImages):
    """
    Mapping dict key to cluster name with concept_mapping.yaml
    :param class_name:
    :param model_name:
    :param localExplanationImages: {patch-x:
                                             {
                                               "src": '',
                                               "score": 00,
                                               "label": dict key,
                                               contributors:[{"src": '',
                                                              "score": 00,
                                                              "label": "xx"}]
                                            }
                                    }
    :return: localExplanationImages with correct label
    """
    yaml_path = os.path.join(os.getcwd(), "data/image data/concept_mapping.yaml")
    mapping = read_yaml_file(yaml_path)
    for key in localExplanationImages.keys():
        localExplanationImages[key]["label"] = mapping[class_name]["object"][model_name][int(localExplanationImages[key]["label"])]
        # 注释可以根据label看概念
        for component in localExplanationImages[key]["contributors"]:
            # print(mapping[class_name]["component"][model_name])
            if int(component["label"]) in mapping[class_name]["component"][model_name]:
                component["label"] = localExplanationImages[key]["label"] + "'s " + mapping[class_name]["component"][model_name][int(component["label"])]
            else:
                component["label"] = localExplanationImages[key]["label"] + "'s " + "other"
    return localExplanationImages


def encodeImage(sourceImagePath):
    """
    Encoded a path to a computer readable code, to be sent to front end.
    :param sourceImagePath:
    :return: encoded path
    """
    with open(sourceImagePath, 'rb') as f:
        sourceImagePath = base64.b64encode(f.read()).decode('utf-8')
    return sourceImagePath


def generateSubImages(segmented_image_path, image_num):
    """
    获取分割的子图片。Segmented images can be patches or superpixels
    :param segmented_image_path:
    :param image_num:
    :return:
    """
    segmented_images = os.listdir(segmented_image_path)
    segmented_images_list = []
    for segmented_image in segmented_images:
        if segmented_image.split('-')[0] == image_num:
            segmented_images_list.append(os.path.join(segmented_image_path, segmented_image))

    subPics = []
    for i in range(min(20, len(segmented_images_list))):
        segmented_images_list[i] = encodeImage(segmented_images_list[i])
        subPics.append({"src": segmented_images_list[i]})
    return subPics


def get_image(request):
    """
    获取默认选择图片
    :param request:
    :return:
    """
    root_path = 'E:/File/1_Graduation Thesis/5-code/HCE explainer/backend/data/image data/mainline'

    optionPics = [{"src": root_path+"/sorrel/handle image/6.jpg", "id": "n02389026",
                   "class": "sorrel"},
                  {"src": root_path+"/bulbul/handle image/6.jpg", "id": 'n01560419',
                   "class": "bulbul"},
                  {"src": root_path + "/tabby/handle image/6.jpg", "id": 'n02123045',
                   "class": "tabby"}]

    encoded_strings = []
    for i, pic in enumerate(optionPics):
        with open(pic["src"], 'rb') as f:
            encoded_string = base64.b64encode(f.read()).decode('utf-8')
            optionPics[i]["src"] = encoded_string
    # https://deepinout.com/django/django-questions/947_django_how_to_return_a_list_object_in_httpresponse_django.html
    # return JsonResponse({'image': encoded_string})
    return JsonResponse(optionPics, safe=False)
    # return HttpResponse([optionPic])


def explain_image(request):
    """
    获取主页面解释的热图
    :param request:{"model": xxx, "class":  xxx}
    :return: {"src": xxx, "contributors": {"high": "xxx", "medium": "xxxx", "low": "xxx"}
    """
    model_name = request.GET.get("model")
    class_name = request.GET.get("class")
    data = {}
    if model_name == "deeplabv3" and class_name == "tabby":
        data = {"src": None, "contributors": {"high": "Tabby's head", "medium": "Tabby's chest", "low": "Tabby's body"}}
    if model_name == "fcn" and class_name == "tabby":
        data = {"src": None, "contributors": {"high": "Head", "medium": "Breast", "low": "Lower Body"}}
    if model_name == "lraspp" and class_name == "tabby":
        data = {"src": None, "contributors": {"high": "Partial Head", "medium": "Partial Breast", "low": "Foot"}}
    if model_name == "deeplabv3" and class_name == "bulbul":
        data = {"src": None, "contributors": {"high": "Partial Head", "medium": "Partial Breast", "low": "Foot"}}
    if model_name == "deeplabv3" and class_name == "bulbul":
        data = {"src": None, "contributors": {"high": "Front Head", "medium": "Rear Head", "low": "Body"}}
    if model_name == "fcn" and class_name == "bulbul":
        data = {"src": None, "contributors": {"high": "Middle Head", "medium": "Else Head", "low": "Body"}}
    if model_name == "lraspp" and class_name == "bulbul":
        data = {"src": None, "contributors": {"high": "Partial Head", "medium": "Background", "low": "Else"}}
    if model_name == "deeplabv3" and class_name == "sorrel":
        data = {"src": None, "contributors": {"high": "Front Head", "medium": "Rear Head", "low": "Body"}}
    if model_name == "fcn" and class_name == "sorrel":
        data = {"src": None, "contributors": {"high": "Tail", "medium": "Body", "low": "Head"}}
    if model_name == "lraspp" and class_name == "sorrel":
        data = {"src": None, "contributors": {"high": "Breast", "medium": "Body", "low": "Else"}}
    print(class_name, model_name)
    root_path = 'E:/File/1_Graduation Thesis/5-code/HCE explainer/backend/data/image data/mainline'
    explained_image = os.path.join(root_path, class_name, model_name, "heatmap", "6-c.jpg")

    with open(explained_image, 'rb') as f:
        encoded_string = base64.b64encode(f.read()).decode('utf-8')
    data["src"] = encoded_string
    return JsonResponse(data, safe=False)


def getSegSample(request):
    """
    获取知识获取页面指标对比表格中的示例图片。Comparison Extraction
    """
    pics = {"class": "airplane",
            "src": { "deeplabv3": "E:/File/1_Graduation Thesis/5-code/HCE explainer/backend/data/image data/comparison/deeplabv3_resnet101.png",
                     "fcn": "E:/File/1_Graduation Thesis/5-code/HCE explainer/backend/data/image data/comparison/fcn_resnet50.png",
                     "lraspp": "E:/File/1_Graduation Thesis/5-code/HCE explainer/backend/data/image data/comparison/lraspp_mobilenet_v3_large.png"
                    }
            }
    for key in pics["src"].keys():
        with open(pics["src"][key], 'rb') as f:
            pics["src"][key] = base64.b64encode(f.read()).decode('utf-8')
    # print(pics)
    return JsonResponse(pics, safe=False)


def getSemanticSegmentationMetrics(request):
    """
    获取知识获取页面指标对比表格中数据。Comparison Extraction
    """
    modelData = [
        {"modelName": "deeplabv3", "PixelAccuracy": 0.9238, "MIoU": 0.7318, "id": '1'},
        {"modelName": "fcn", "PixelAccuracy": 0.9158, "MIoU": 0.6564, "id": '2'},
        {"modelName": "lraspp", "PixelAccuracy": 0.9055, "MIoU": 0.6624, "id": '3'}]

    return JsonResponse(modelData, safe=False)


def getOptionPics(request):
    """
    获取选项栏的选择图片。Extraction Option
    """
    root_path = 'E:/File/1_Graduation Thesis/5-code/HCE explainer/backend/data/image data/mainline'
    class_name = request.GET.get("class")
    optionPics = [
    {"src": os.path.join(root_path, class_name, "handle image", "4.jpg"), "id": '4',"class": class_name},
    {"src": os.path.join(root_path, class_name, "handle image", "5.jpg"), "id": '5',"class": class_name},
    {"src": os.path.join(root_path, class_name, "handle image", "6.jpg"), "id": '6',"class": class_name}]
    for optionPic in optionPics:
        with open(optionPic["src"], 'rb') as f:
            optionPic["src"] = base64.b64encode(f.read()).decode('utf-8')
    # print(optionPics)
    return JsonResponse(optionPics, safe=False)


def getExtractionImages(request):
    """
    获取知识获取主功能页面patch和超像素的大图和细分图
    :param request:
    :return:
    """
    root_path = 'E:/File/1_Graduation Thesis/5-code/HCE explainer/backend/data/image data/mainline'
    class_name, model_name, image_num = request.GET.get("class"), request.GET.get("model"), request.GET.get("imageNum")

    print(class_name, model_name, image_num)
    semanticPic = {"src": encodeImage(os.path.join(root_path, class_name, model_name, "patch-image", image_num+".jpg")),
                   "id": image_num,
                   "class": class_name}
    pixelPic = {"src": encodeImage(os.path.join(root_path, class_name, model_name, "superpixel-image", image_num+".jpg")),
                "id": image_num,
                "class": class_name}

    patches_path = os.path.join(root_path, class_name, model_name, "patches")
    subSSPics = generateSubImages(patches_path, image_num)

    superpixels_path = os.path.join(root_path, class_name, model_name, "superpixels")
    subPSPics = generateSubImages(superpixels_path, image_num)

    return JsonResponse({"SS": subSSPics, "PS": subPSPics, "semanticPic": semanticPic, "pixelPic": pixelPic}, safe=False)


def getTreeImages(request):
    """
    获取概念树的各层次图片
    :param request:
    :return:
    """
    max_patch_superpixel_images_limit, max_node_limit, max_handle_images_limit, max_patch_limit, max_superpixel_limit = 8, 24, 34, 15, 12
    root_path = 'E:/File/1_Graduation Thesis/5-code/HCE explainer/backend/data/image data/mainline'
    class_name, model_name = request.GET.get("class"), request.GET.get("model")

    print("Processing ", class_name, ", ", model_name)
    # Handle Image
    handleImage_root_path = os.path.join(root_path, class_name, "handle image")
    handleImage_paths = os.listdir(handleImage_root_path)
    handle_images = []
    for handleImage_path in handleImage_paths:
        if len(handle_images) < max_handle_images_limit:
            handle_images.append({"src": encodeImage(os.path.join(handleImage_root_path, handleImage_path))})

    # TODO 根据clusterImages提取图片
    with open(os.path.join(root_path, class_name, model_name, "clusterImages.txt"), 'r', encoding='utf-8') as f:
        dict_cluster = eval(f.read())  # eval
    # patches
    patches = {"class": class_name, "model": model_name, "clusters": []}
    patches_path = os.path.join(root_path, class_name, model_name, "patches")
    for key in dict_cluster.keys():
        for i in range(len(dict_cluster[key]["patch"])):
            encoded_path = encodeImage(os.path.join(patches_path, dict_cluster[key]["patch"][i]+".jpg"))
            dict_cluster[key]["patch"][i] = encoded_path
        patches["clusters"].append(dict_cluster[key]["patch"][:min(max_patch_limit, len(dict_cluster[key]["patch"]))])
    # print(len(patches["clusters"]))

    # superpixels
    superpixels = {"class": class_name,
                   "model": model_name,
                   "clusters": []
                   }
    superpixels_path = os.path.join(root_path, class_name, model_name, "superpixels")
    # key: patch_cluster i: superpixel_cluster j: superpixels
    for key in dict_cluster.keys():
        for i in range(len(dict_cluster[key]["superpixel"])):
            superpixel_cluster = {"belongToPatch": key,
                                  "images": []}
            for j in range(len(dict_cluster[key]["superpixel"][i])):
                encoded_path = encodeImage(os.path.join(superpixels_path, dict_cluster[key]["superpixel"][i][j]+".jpg"))
                dict_cluster[key]["superpixel"][i][j] = encoded_path
            superpixel_cluster["images"] = list(dict_cluster[key]["superpixel"][i])[:min(max_superpixel_limit, len(dict_cluster[key]["superpixel"][i]))]
            # 限制叶子节点数量
            if i < max_patch_superpixel_images_limit and len(superpixels["clusters"]) < max_node_limit:
                superpixels["clusters"].append(superpixel_cluster)

    # print(superpixels)
    return JsonResponse({"handleImages": handle_images, "patches": patches, "superpixels": superpixels}, safe=False)


def getLocalExplanationImages(request):
    """
    获取贡献度计算局部解释页面主功能栏所需图片
    :param request:
    :return:
    """
    localExplanationImages = {}
    class_name, model_name, img_num = request.GET.get("class"), request.GET.get("model"), request.GET.get("imageNum")
    print("Processing Local Explanation Images:")
    print(class_name, model_name, img_num)
    local_explanation_score_single_img_path = os.path.join(os.getcwd(), "data/image data/mainline", class_name,
                                                           model_name, "concept each image", img_num)
    with open(os.path.join(local_explanation_score_single_img_path, "score.txt"), 'r', encoding='utf-8') as f:
        contributors = eval(f.read())  # eval
        # print(contributors)

    with open(os.path.join(local_explanation_score_single_img_path, "localExplanation.txt"), 'r', encoding='utf-8') as f:
        patches = eval(f.read())  # eval
        # print(patches)

    for key in contributors["patch"].keys():
        localExplanationImages.update({"patch"+str(key): contributors["patch"][key]})
        img_path = os.path.join(local_explanation_score_single_img_path, "ob_concept_imgs",str(key) + '.jpg')
        localExplanationImages["patch"+str(key)]["src"] = encodeImage(img_path)
        localExplanationImages["patch" + str(key)]["score"] = format(localExplanationImages["patch" + str(key)]["score"], '.3f')
        localExplanationImages["patch" + str(key)]["label"] = str(key)
        # for debug
        # localExplanationImages["patch"+str(key)]["src"] = img_path

    for patch_id in patches.keys():
        temp_unsorted_list = {}
        for id in patches[patch_id]:
            temp_unsorted_list.update({id: contributors["contributors"][id]["score"]})
        # 只取前三个
        # patch_contributors = sorted(temp_unsorted_list.items(),key = lambda x:x[1], reverse=True)[:4]
        patch_contributors = sorted(temp_unsorted_list.items(),key = lambda x:x[1], reverse=True)
        # print(patch_contributors)
        for patch_contributor in patch_contributors:
            img_path = os.path.join(local_explanation_score_single_img_path, "co_concept_imgs", str(patch_contributor[0])+'.jpg')
            temp = {"src": encodeImage(img_path), "score": format(patch_contributor[1], '.3f'), "label": patch_contributor[0]}
            # for debug
            # temp = {"src": patch_contributor[0], "score": patch_contributor[1], "label": ''}
            localExplanationImages["patch" + str(patch_id)]["contributors"].append(temp)
            # print()

    localExplanationImages = setLocalExplanationImagesLabel(class_name, model_name, localExplanationImages)
    return JsonResponse(localExplanationImages, safe=False)


def getSegmentedResult(request):
    """
    获取贡献度计算局部解释页面各图片的概念标签
    :param request:
    :return:
    """
    class_name, model_name, img_num = request.GET.get("class"), request.GET.get("model"), request.GET.get("imageNum")
    root_path = os.path.join(os.getcwd(), "data/image data/mainline", class_name, model_name)
    segResult = {"heatmapObj":{"src": os.path.join(root_path, "heatmap", str(img_num)+'-o.jpg')},
                 "segImageObj": {"src": os.path.join(root_path, "patch-image", str(img_num)+'.jpg')},
                 "heatmapCom": {"src": os.path.join(root_path, "heatmap", str(img_num)+'-c.jpg')},
                 "segImageCom": {"src": os.path.join(root_path, "superpixel-image", str(img_num)+'.jpg')}}
    for key in segResult.keys():
        segResult[key]["src"] = encodeImage(segResult[key]["src"])
    return JsonResponse(segResult, safe=False)


def getExplanationComparisonImages(request):
    """
    Get 3 models images heatmap at object level and component level
    :return:
    """
    compareList = {
        "Obj": {
                    "deeplabv3":'',
                    "fcn": '',
                    "lraspp":''
               },
        "Compo": {
                    "deeplabv3": '',
                    "fcn": '',
                    "lraspp": ''
                 },
    }
    class_name, img_num = request.GET.get("class"), request.GET.get("imageNum")
    root_path = os.path.join(os.getcwd(), "data/image data/mainline/", class_name)
    for key in compareList.keys():
        for model in compareList[key].keys():
            path = os.path.join(root_path, model, "heatmap", img_num+"-o.jpg" if key == "Obj" else img_num+"-c.jpg")
            compareList[key][model] = encodeImage(path)
    return JsonResponse(compareList, safe=False)


def getExplanationMetrics(request):
    """
    获取对比解释中3个表格的指标数据
    :param request:
    :return:
    """
    ISSCISDCMetrics = []
    metric_yaml_path = os.path.join(os.getcwd(), "data/image data/comparison/explanation_metrics.yaml")
    metrics = read_yaml_file(metric_yaml_path)
    print(metrics["ISSCISDCMetrics"])
    for class_name in metrics["ISSCISDCMetrics"].keys():
        ISSCISDCMetrics.append({"class": class_name,
                                "ISSC": metrics["ISSCISDCMetrics"][class_name]["ISSC"],
                                "ISDC": metrics["ISSCISDCMetrics"][class_name]["ISDC"]})
    SSC, SDC = [], []
    for model in metrics["SSCMetrics"].keys():
        SSC.append({"model": model, "index": metrics["SSCMetrics"][model]["index"]})
    for model in metrics["SDCMetrics"].keys():
        SDC.append({"model": model, "index": metrics["SDCMetrics"][model]["index"]})

    return JsonResponse({"ISSCISDCMetrics": ISSCISDCMetrics, "SSCMetrics": SSC, "SDCMetrics": SDC}, safe=False)


def HCE_algorithm():
    # TODO 任务服务列表最后搞，先不耦合
    process_class = "bison"
    model_name = "deeplabv3"
    # HCE.run_process(process_class, model_name, option=0)
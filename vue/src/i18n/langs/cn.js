import zhLocale from 'element-ui/lib/locale/lang/zh-CN'
const cn = {
    option: {
        'model': 'Model',
        'SegHint': 'Used for semantic segmentation',
        'class': 'Class',
        'classHint': 'Input Category'
    },
    main: {
        'hello': 'Hello World',
        'MainPredict': 'Start Prediction',
        'MainInput': 'Input Image',
        'MainInputHint': 'Select an image, it will be intelligently processed by ',
        'MainInputHintHyper': 'Deep Neural Network',
        'MainOutput': 'Output',
        'MainOutputHint': 'The predicted class output from the neural network',
        'MainDNN': 'DNN Model',
        'MainDNNHint': 'Pre-trained classification model',
        'MainEX': 'Prediction Explanation',
        'MainEXHint': 'Determines the contribution of each concept in the image',
        'MainResults': 'Results',
        'MainResultsHint': 'Sorted in descending order'
    },
    extraction: {
        'topic': 'Semantic Segmentation Model Evaluation',
        'sentence-1': 'This module evaluates the segmentation performance of three semantic segmentation algorithms: deeplabv3, fcn, and lraspp on the PASCAL VOC 2012 dataset.',
        'sentence-2': 'Hierarchical knowledge acquisition is the basis for building concept trees and calculating contributions. It relies on semantic segmentation technology. Therefore, the performance of the semantic segmentation model will have a decisive impact on the hierarchical embedding explanation method (HCE).',
        'sentence-3': 'This module uses Pixel Accuracy and Mean Intersection over Union (MIoU) as evaluation metrics.',
        'sentence-4': 'Operation Instructions',
        'sentence-5': '1. Click on the "Image" column cell with the mouse to view the segmentation effect of the semantic segmentation model on the sample image. From left to right, the images are: original image - ground truth label - segmentation result - segmentation result overlaid on the original image.',
        'sentence-6': '2. View metric data and segmentation examples. Click the rightmost box in the table to select the model you want to analyze further in hierarchical knowledge acquisition.',
        'sentence-7': '3. Click "Confirm" to proceed to the next step.',
        'sentence-8': 'Supports uploading a personalized dataset to view evaluation results.',
        'modelName': 'Model Name',
        'PixelAccuracy': 'Pixel Accuracy',
        'MIoU': 'Mean IoU',
        'change': 'Change Image',
        'Image': "Image",
    },
    level: {
        'imageLevel': 'Image Level',
        'imageLevelHint': 'Original Image',
        'objectLevel': 'Object Level',
        'objectLevelHint': 'Concepts after semantic segmentation',
        'componentLevel': 'Component Level',
        'componentLevelHint': 'Concepts after superpixel segmentation',
    },
    explanation: {
        'compareButton': 'Compare',
        'sectionTitle': 'Contribution Heatmap',
        'sectionHint1': 'The local features of each object in an image are crucial for deep neural network recognition, and their contribution to decision results can be visualized using a heatmap.',
        'sectionHint2': 'Semantic segmentation models segment an image into local features, and differences in segmentation affect decision results differently.',
        'sectionHint3': 'This module compares segmentation results from different semantic segmentation models.',
        'objHeat': 'Object-Level Contribution Heatmap',
        'compoHeat': 'Component-Level Contribution Heatmap',
        'ExResults': 'Results',
        'ExResultsHint': 'Sorted in descending order of contribution'
    },
    utils: {
        'metrics': 'Performance Metrics',
        'confirm': 'Confirm',
        'return': 'Return'
    },
    sideMenu: {
        'home': 'Home',
        'extraction': 'Knowledge Extraction',
        'tree': 'Concept Tree',
        'localExplanation': 'Local Explanation',
        'explanation': 'Comparative Explanation',
        'sys': 'System'
    },
    logIn:{
        signInHint: 'Sign in to HCE Explainer',
        userHint: 'Username or email address',
        password: 'Password',
        passwordHint: 'Forgot password?',
        signIn: 'Sign in',
        signIning: 'Signing in...',
        newToHCE: 'New to HCE?',
        createAccount: 'Create an account'
    },
    sys:{
        profile: 'Profile',
        name: 'Nickname',
        email: 'Email',
        nameHint: 'Your nickname will be used by HCE platform administrators to contact you. You can modify it anytime.',
        emailHint: 'Your email can be used to log in to the HCE platform. Administrators may also contact you via email.',
        update: "Update Profile",
        profilePicture: 'Profile Picture',

        userM: 'User Management',
        nameT: 'Nickname',
        emailT: 'Email',
        instituionT: 'Institution',
        permissionT: 'Permissions',
        delete: 'Delete User',

        log: 'System Logs',
        logID: 'Log ID',
        time: 'Update Time',
        user: 'Username',
        changeLog: 'Change Details'
    },
    ...zhLocale
}
//
// const cn = {
//     option: {
//         'model': '模型',
//         'SegHint': '用于进行语义分割',
//         'class': '类别',
//         'classHint': '将被进行预测和解释'
//     },
//     main: {
//         'hello': '你好世界',
//         'MainPredict': '开始预测',
//         'MainInput': '输入图片',
//         'MainInputHint': '选择一张图片，它将被智能处理，处理模块为',
//         'MainInputHintHyper': '深度神经网络',
//         'MainOutput': '输出',
//         'MainOutputHint': '下方是深度神经网络输出的预测类别',
//         'MainDNN': 'DNN模型',
//         'MainDNNHint': '经过预训练的分类模型',
//         'MainEX': '预测结果解释',
//         'MainEXHint': '用于确定图片中各个概念对深度神经网络预测结果的贡献度',
//         'MainResults': '结果',
//         'MainResultsHint': '根据贡献度降序排列'
//     },
//     extraction: {
//         'topic': '语义分割模型评测',
//         'sentence-1': '本模块将对3种语义分割算法deeplabv3, fcn, lraspp，在PASCAL VOC 2012数据集上评测分割性能。',
//         'sentence-2': '层次知识的获取是构建概念树、计算贡献度的基础，层次知识的获取基于语义分割技术。因此，语义分割模型的性能将对层级嵌入解释方法HCE的解释结果有决定性影响。',
//         'sentence-3': '本模块将像素准确度（Pixel Accuracy）和平均交并比（MIoU）作为评测的指标。',
//         'sentence-4': '操作说明',
//         'sentence-5': '1. 鼠标点击“图片”列单元格，可查看该语义分割模型对示例图片的分割效果。图片中从左至右依次为：原图-真实标签-分割结果-分割结果融合原图。',
//         'sentence-6': '2. 查看指标数据和分割示例，点击表格最右侧方框，选择需要选取的模型以进一步查看层次知识获取结果。',
//         'sentence-7': '3. 点击“确认”进入下一步',
//         'sentence-8': '支持上传用户个性化的数据集用于查看评测效果；',
//         'modelName': '模型名称',
//         'PixelAccuracy': '像素准确度',
//         'MIoU': '平均交并比',
//         'change': '更换图片',
//         'Image': "图片",
//     },
//     level: {
//         'imageLevel': '图像层级',
//         'imageLevelHint': '原始图片',
//         'objectLevel': '对象层级',
//         'objectLevelHint': '语义分割后的概念',
//         'componentLevel': '组件层级',
//         'componentLevelHint': '超像素分割后的概念',
//     },
//     explanation: {
//         'compareButton': '对比',
//         'sectionTitle': '贡献度热力图',
//         'sectionHint1': '图像中每个物体的局部特征是深度神经网络识别的重要因素，它们对决策结果的贡献可以用热力图表',
//         'sectionHint2': '示。语义分割模型会对图片进行局部特征的分割，局部特征分割的不同，对决策结果的影响也不同，',
//         'sectionHint3': '本模块将对不同语义分割的分割结果进行对比。',
//         'objHeat': '对象级别贡献度热力图',
//         'compoHeat': '组件级别贡献度热力图',
//         'ExResults': '结果',
//         'ExResultsHint': '根据贡献度降序排列'
//     },
//     utils: {
//         'metrics': '性能指标',
//         'confirm': '确认',
//         'return': '返回'
//     },
//     sideMenu: {
//         'home': '主页',
//         'extraction': '知识获取',
//         'tree': '概念树',
//         'localExplanation': '局部解释',
//         'explanation': '对比解释',
//         'sys': '系统'
//     },
//     logIn:{
//         signInHint:'Sign in to HCE Explainer',
//         userHint: 'Username or email address',
//         password: 'Password',
//         passwordHint: 'Forgot password?',
//         signIn: 'Sign in',
//         signIning: 'Signing in...',
//         newToHCE: 'New to HCE?',
//         createAccount: 'Create an account'
//     },
//     // logIn:{
//     //     signInHint:'登录至 HCE 解释平台',
//     //     userHint: '用户名或电子邮箱',
//     //     password: '密码',
//     //     passwordHint: '忘记密码？',
//     //     signIn: '登录',
//     //     signIning: '登录中...',
//     //     newToHCE: '没有HCE平台账号？',
//     //     createAccount: '登录即创建账号'
//     // },
//     sys:{
//         profile: '个人信息',
//         name: '昵称',
//         email: '电子邮箱',
//         nameHint: '昵称将会HCE平台管理员联系您时对您的称呼，您可以随时进行修改',
//         emailHint: '电子邮箱可以用于登录HCE平台，HCE平台管理员也将通过电子邮箱与您联系',
//         update: "更新个人信息",
//         profilePicture: '个人头像',
//
//
//         userM: '用户管理',
//         nameT: '昵称',
//         emailT: '电子邮箱',
//         instituionT: '机构',
//         permissionT: '权限',
//         delete: '删除用户',
//
//         log: '系统日志',
//         logID: '编号',
//         time: '更新时间',
//         user: '用户名',
//         changeLog: '变更内容'
//     },
//     ...zhLocale
// }

export default cn
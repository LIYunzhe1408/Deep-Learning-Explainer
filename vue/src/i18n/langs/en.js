import enLocale from 'element-ui/lib/locale/lang/en'
const en = {
    option: {
      'model': 'Model',
      'SegHint': 'Semantic Segmentation',
      'class': 'Class',
      'classHint': 'To explain'
    },
    main: {
        'hello': 'hello world',
        'MainPredict': 'Predict',
        'MainInput': 'INPUT IMAGE',
        'MainInputHint': 'Choose one image to be predicted by ',
        'MainInputHintHyper': 'Deep Neural Network',
        'MainOutput': 'OUTPUT',
        'MainOutputHint': 'Classification result by the DNN below',
        'MainDNN': 'DNN Model',
        'MainDNNHint': 'Pretrained Classification Model',
        'MainEX': 'EXPLANATION',
        'MainEXHint': 'Determine which concept part contributes the most',
        'MainResults': 'Results',
        'MainResultsHint': 'Sorted By Contributions'
    },
    extraction: {
      'topic': 'Semantic Segmentation Evaluation',
        'sentence-1': 'In this section, we apply several state-of-the-art semantic segmentation models on PASCAL VOC 2012 to evaluate their performance. ',
        'sentence-2': 'This evaluation will have a determined effect on the performance of our Hierarchical Concept-Based Explanation method.',
        'sentence-3': 'Pixel Accuracy and MIoU are used as metrics for evaluation.',
        'sentence-4': 'Features in this version',
        'sentence-5': 'Select suitable model for following concept segmentation.',
        'sentence-6': 'Features to be updated in next version',
        'sentence-7': '`Change Image` button will be available to show various results.',
        'sentence-8': 'Uploaded datasets will be available to be processed by different semantic segmentation models.',
        'modelName': 'Model Name',
        'PixelAccuracy': 'Pixel Accuracy',
        'MIoU': 'MIoU',
        'change': 'Change Images',
        'Image': "Image",
    },
    level: {
        'imageLevel': 'IMAGE LEVEL',
        'imageLevelHint': 'Handle Image',
        'objectLevel': 'OBJECT LEVEL',
        'objectLevelHint': 'Concepts After Semantic Segmentation',
        'componentLevel': 'COMPONENT LEVEL',
        'componentLevelHint': 'Concepts After Superpixel Segmentation',
    },
    explanation: {
        'compareButton': 'Compare',
        'sectionTitle': 'Heatmap Contributions',
        'sectionHint1': 'Built like a spreadsheet, project tables give you a live canvas to filter,',
        'sectionHint2': 'sort, and group issues and pull requests. Tailor them to your needs with',
        'sectionHint3': 'custom fields and saved views.',
        'objHeat': 'Object Level Heatmap',
        'compoHeat': 'Component Level Heatmap',
        'ExResults': 'Results',
        'ExResultsHint': 'Sorted By Contributions'
    },
    utils: {
        'metrics': 'Metrics',
        'confirm': 'Confirm',
        'return': 'Return'
    },
    sideMenu: {
        'home': 'Home',
        'extraction': 'Concept Extraction',
        'tree': 'Concept Tree',
        'localExplanation': 'Local Explanation',
        'explanation': 'Explanation',
        'sys': 'System'
    },
    logIn:{
        signInHint:'Sign in to HCE Explainer',
        userHint: 'Username or email address',
        password: 'Password',
        passwordHint: 'Forgot password?',
        signIn: 'Sign in',
        signIning: 'Signing in...',
        newToHCE: 'New to HCE?',
        createAccount: 'Create an account'
    },
    profile:{
        profile: 'Profile',
        name: 'Name',
        email: 'Public email',
        nameHint: 'Your name will be regarded as how HCE admins call you when contacting you',
        emailHint: 'Your email can be used when signing in HCE EXPLAINER.',
        update: "Update Profile",
        profilePicture: 'Profile Picture',

        userM: 'User Management',
        nameT: 'Name',
        emailT: 'Email',
        instituionT: 'Institution',
        permissionT: 'Permission',
        delete: 'Delete user',

        log: 'System Log',
        logID: 'ID',
        time: 'Update Time',
        user: 'User Name',
        changeLog: 'Change Log'

    },
    ...enLocale
}

export default en;
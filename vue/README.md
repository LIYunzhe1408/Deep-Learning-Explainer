# 重要目录文件
```
E:.
├─.idea
├─node_modules      
├─public
│   └─index.html  // 最终编译为html
├─src
│   ├─main.js      // 全局文件，创建Vue实例，挂载到div对象，定义全局参数 
│   ├─App.vue      // 主页面
│   ├─assets       // 静态文件
│   ├─components   // 页面组件
        --ComparisonExtraction.vue      // 知识获取页面指标对比页面
        --Main.vue                      // 主页面
        --MainExplanation.vue           // 对比解释页面主功能栏
        --MainExtraction.vue            // 知识获取页面主功能栏
        --MainLocalExplanation.vue      // 贡献度计算局部解释主功能栏
        --MainTree.vue                  // 类概念书主功能栏
        --OptionExplanation.vue         // 对比解释页面选项栏
        --OptionExtraction.vue          // 知识获取页面选项栏
        --OptionLocalExplanation.vue    // 贡献度计算局部解释选项栏
        --OptionMain.vue                // 主页面选项栏
        --OptionTree.vue                // 概念树页面选项栏
        --SettingLog.vue                // 系统日志页面
│   ├─i18n          // 多语言配置-可以不使用，不影响功能
        --langs
            --cn.js // 中文配置
            --en.js // 英文配置
│   ├─router        // 路由配置, path+component定义子页面
│   ├─utils         // 公式渲染
        --MathJax.js
│   └─views                     // 页面
        --Explanation.vue       // 对比解释页面入口
        --Extraction.vue        // 知识获取页面入口
        --Header.vue            // 顶部header
        --Home.vue              // 主页面入口
        --HomeView.vue          // 全局路由入口
        --LocalExplanation.vue  // 贡献度计算局部解释页面入口
        --LogIn.vue             // 登录页面
        --Settings.vue          // 系统管理页面
        --SideMenu.vue          // 侧边栏菜单选项
        --TaskList.vue          // 任务列表
        --TaskSubmission.vue    // 新建任务页面
        --Tree.vue              // 概念树页面接口
├─package.json     // 所有的依赖配置
└─vue.config.js    // 配置工程参数
```


# vue
Try iconfont

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

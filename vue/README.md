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
│   ├─router       // 路由配置, path+component定义子页面
│   └─views        // 页面
├─package.json     // 所有的依赖配置
└─vue.config.js    // 配置工程参数
```


# vue

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

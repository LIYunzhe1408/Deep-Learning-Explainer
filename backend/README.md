# 运行环境
Django                      3.2.23
mysqlclient                 2.2.4
numpy                       1.21.5
pandas                      2.0.3
picture                     0.0.1
Pillow                      9.0.1
pip                         21.2.2
PyMySQL                     1.1.0
PyYAML                      6.0.1
requests                    2.31.0
scikit-image                0.19.3
scikit-learn                1.3.0
scipy                       1.10.1
segmentation-models-pytorch 0.3.3
shap                        0.42.1
torch                       1.11.0
torchaudio                  0.11.0
torchvision                 0.12.0

# 项目结构树
--backend
    --__init__.py   配置文件-未使用
    --asgi.py       配置文件-未使用
    --settings.py   第85行配置数据库
    --urls.py       配置路由
    --wsgi.py       配置文件-未使用
--core
    --migrations    数据库迁移文件，仅python连接数据库使用
    --__init__.py   配置文件-未使用
    --admin.py      配置文件-未使用
    --apps.py       配置文件-未使用
    --models.py     数据库模型
    --tests.py      配置文件-未使用
    --urls.py       子路由配置
    --views.py      接收前端请求，后端处理接口【主要文件】
--data
    --image data        
        --comparison    对比数据图片存储
        --mainline      主要数据图片存储
            -- 类别名称
                --语义分割模型-x
                    --heatmap               对象层级、组件层级解释热图
                    --patch-image           对象层级patch分割大图
                    --patches               对象层级patch细分图
                    --superpixel-image      组件层级超像素分割大图
                    --superpixels           组件层级超像素细分图
                --handle image  原始图片
        --concept_mapping.yaml  概念映射配置文件
    --profile           用户管理头像存储
    --test              测试用-不用管
--module        集成算法时使用，代码用途见data_generator项目readme.md
--templates     未使用
--db.sqlite3    默认数据库-未使用
--manage.py     启动文件

# 启动说明
* 命令行："项目路径/backend/manage.py" runserver 8000
* IDE：点击启动按钮即可
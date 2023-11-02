# 基于fastapi实现m3e embedding模型相关接口

本项目使用[`fastapi-start`](https://github.com/ibbd-dev/fastapi-start)工具进行初始化，该工具的帮助可以使用命令：`fas --help`。

用于快速将`m3e-base`（还没测试过）和`m3e-large`（已完成测试）的Embedding模型启动为http接口，基于流行的fastapi框架进行开发。

## 1. 功能介绍

## 2. 安装与部署

### 2.1 部署前需要先复制配置文件

```sh
cd app/
cp settings-example.py settings.py

# 根据实际情况修改配置文件
vim settings.py

# 启动
# FastAPI文档：https://fastapi.tiangolo.com/
uvicorn main:app --reload
```

### 2.2 使用docker-compose启动

```sh
# 如果需要可以修改该配置
# 特别是模型目录：/app/files/models/m3e-large/，需要将外部的模型目录挂载进来
# 如果需要改目录，也可以在配置文件settings.py中进行修改
cp docker-compose-example.yml docker-compose.yml

# 启动
docker-compose up -d
```

## 3. fas工具使用说明

```sh
# 添加一个模块
# test是模块名称，可以设定
fas module new --name=test

# 添加模块之后，要使模块生效，需要手动在app/main.py文件中注册该路由
# prefix: 该参数定义路由的前缀，每个模块的路由前缀必须是唯一的
from test_module.router import router as test_router
app.include_router(test_router, prefix="/test", tags=["测试模块"])

# 在当前目录增加一个test.py文件
# python是文件类型，test是文件名
fas file python test
```

fas也支持一些内置模块：

```sh
# 支持的内置模块列表
fas module list

# 查看某内置模块的帮助文档
fas module help captcha
```

## 4. 附录

## 5. 项目相关人员

- alex cai

# -*- coding: utf-8 -*-
#
# 基础配置文件，该文件应该只被settings.py引用
# Author: alex cai
# Email: caiyingyao@ibbd.net
# Created Time: 2023-11-01
from enum import Enum
from pathlib import Path

# 全局测试状态
DEBUG = False

# 版本号
VERSION = "v0.1.0"

# 系统异常状态码的基数
# 返回给前端的code会加上该值
SYSTEM_CODE_BASE = 10000

# 数据库连接
# 在database.py文件中使用
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/test"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# 配置日志目录
# 项目跟目录
ROOT_PATH = Path(__file__).absolute().parent

# 文件根目录
FILE_ROOT_PATH = ROOT_PATH.joinpath("files")

# 日志文件根目录
LOG_ROOT_PATH = FILE_ROOT_PATH.joinpath("logs")

# 日志文件根目录
MODEL_ROOT_PATH = FILE_ROOT_PATH.joinpath("models")

# 用于追踪的请求ID字段
REQUEST_ID_KEY = "x-request-id"


class ModelType(Enum):
    """模型类型"""
    large = 'large'

# 模型配置
MODEL_CONFIG = {
    ModelType.large: MODEL_ROOT_PATH.joinpath('m3e-large'),
}

# 默认模型
MODEL_DEFAULT = ModelType.large

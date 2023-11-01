# -*- coding: utf-8 -*-
#
# 模块路由配置文件
# Author: alex cai
# Email: caiyingyao@ibbd.net
# Created Time: 2023-11-01
from typing import List
from pydantic import BaseModel, Field
from settings import ModelType, MODEL_DEFAULT


class EmbeddingRequest(BaseModel):
    """Embedding请求参数 """
    texts: List[str] = Field(..., min_items=1, max_items=100,
                             title='需要进行Embedding的文本列表', description='注意文本的长度应该要符合模型的输入限制')
    model: ModelType = Field(MODEL_DEFAULT, title='Embedding模型')


class EmbeddingResponse(BaseModel):
    """Embedding响应参数 """
    embeddings: List[List[float]] = Field(..., min_items=1, max_items=100,
                                          title='Embedding列表', description='和输入参数中的texts对应')

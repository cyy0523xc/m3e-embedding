# -*- coding: utf-8 -*-
#
# 模块路由文件
# Author: alex cai
# Email: caiyingyao@ibbd.net
# Created Time: 2023-11-01
# from fastapi import Depends, HTTPException
from fastapi import APIRouter
import torch
import numpy as np
from typing import List
from scipy.interpolate import interp1d
from sklearn.preprocessing import PolynomialFeatures
from sentence_transformers import SentenceTransformer

from settings import MODEL_CONFIG, MODEL_DEFAULT
from .schema import EmbeddingRequest, EmbeddingResponse

router = APIRouter(
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)

# 检测是否有GPU可用，如果有则使用cuda设备，否则使用cpu设备
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
if torch.cuda.is_available():
    print('本次加载模型的设备为GPU: ', torch.cuda.get_device_name(0))
else:
    print('本次加载模型的设备为CPU.')

# 加载模型
models = {
    MODEL_DEFAULT: SentenceTransformer(MODEL_CONFIG[MODEL_DEFAULT].as_posix(), device=device)
}
print("加载默认模型成功.")


@router.post("/", summary='Embedding', response_model=EmbeddingResponse)
async def api_embedding(request: EmbeddingRequest):
    """批量文本Embedding接口"""
    # 转向量
    model = models[request.model]
    embeddings = [model.encode(text) for text in request.texts]

    # 如果嵌入向量的维度不为1536，则使用特征扩展法扩展至1536维度
    # # embeddings = [_interpolate_vector(embedding, 1536) if len(embedding) < 1536 else embedding for embedding in embeddings]
    embeddings = [_expand_features(embedding, 1536) if len(embedding) < 1536 else embedding for embedding in embeddings]

    # Min-Max normalization
    embeddings = [embedding / np.linalg.norm(embedding) for embedding in embeddings]

    # 将numpy数组转换为列表
    embeddings = [embedding.tolist() for embedding in embeddings]
    return {
        'embeddings': embeddings,
    }


def _interpolate_vector(vector: List[float], target_length: int) -> List[float]:
    """使用特征插值法扩展向量维度"""
    original_indices = np.arange(len(vector))
    target_indices = np.linspace(0, len(vector)-1, target_length)
    f = interp1d(original_indices, vector, kind='linear')
    return f(target_indices)


def _expand_features(embedding: List[float], target_length: int) -> List[float]:
    """使用特征扩展法扩展向量维度"""
    poly = PolynomialFeatures(degree=2)
    expanded_embedding = poly.fit_transform(embedding.reshape(1, -1))
    expanded_embedding = expanded_embedding.flatten()
    if len(expanded_embedding) > target_length:
        # 如果扩展后的特征超过目标长度，可以通过截断或其他方法来减少维度
        expanded_embedding = expanded_embedding[:target_length]
    elif len(expanded_embedding) < target_length:
        # 如果扩展后的特征少于目标长度，可以通过填充或其他方法来增加维度
        expanded_embedding = np.pad(expanded_embedding, (0, target_length - len(expanded_embedding)))

    return expanded_embedding

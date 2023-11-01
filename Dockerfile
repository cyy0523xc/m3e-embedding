FROM nvidia/cuda:10.2-cudnn7-devel-ubuntu18.04
LABEL maintainer "Alex Cai <cyy0523xc@qq.com>"

# -----------------------------------------------------------------
# ----------------------- install python及依赖 --------------------
# -----------------------------------------------------------------
# 安装Python3.8, pip, git等
# 参考：https://cloud.tencent.com/developer/article/1626765
# wget https://bootstrap.pypa.io/get-pip.py 直接下载经常超时
#   可以使用阿里的源替代：http://mirrors.aliyun.com/pypi/get-pip.py
# 可能会报错：GPG error: https://developer.download.nvidia.cn/..... NO_PUBKEY A4B469963BF863CC。
# 可以直接删除下面的文件：
#   rm /etc/apt/sources.list.d/cuda.list
#   rm /etc/apt/sources.list.d/nvidia-ml.list
# COPY get-pip.py /
RUN ls /etc/apt/sources.list.d/ \
    && rm -f /etc/apt/sources.list.d/cuda.list \
    && rm -f /etc/apt/sources.list.d/nvidia-ml.list \
    && apt update -y \
    && apt install -y --no-install-recommends software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa -y \
    && apt-get install -y --no-install-recommends \
        git \
        wget \
        python3.8 \
        python3.8-dev \
        python3.8-distutils \
        libglib2.0-0 libsm6 libxext-dev libxrender1 libgl1-mesa-glx \
    && ln -sf /usr/bin/python3.8 /usr/bin/python3 \
    && wget http://mirrors.aliyun.com/pypi/get-pip.py \
    && python3 get-pip.py \
    && rm get-pip.py \
    && rm -rf /var/lib/apt/lists/*\
    && alias cpip='pip install -i https://mirrors.aliyun.com/pypi/simple/' \
    && pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/

# ------------------------------------------------------------------
# ----------------------- install python包 -------------------------
# ------------------------------------------------------------------
COPY ./requirements.txt /
RUN pip3 --no-cache-dir install -r /requirements.txt \
    && rm -f /requirements.txt

# 终端设置
# 默认值是dumb，这时在终端操作时可能会出现：
# terminal is not fully functional
ENV LANG C.UTF-8
ENV TERM xterm
ENV PYTHONIOENCODING utf-8
ENV TZ "Asia/Shanghai"

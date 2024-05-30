FROM registry.cn-beijing.aliyuncs.com/serverless_devs/cuda:11.8.0-devel-ubuntu22.04

ARG FACEFUSION_VERSION=2.6.0
ENV GRADIO_SERVER_NAME=0.0.0.0

WORKDIR /facefusion

RUN apt-get update && \
    apt-get install -y python3.10 python-is-python3 pip curl ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . /facefusion

RUN python install.py --onnxruntime cuda-11.8 --skip-conda && \
    pip install -r requirements.txt && \
    pip cache purge

EXPOSE 7860

CMD ["python", "run.py", "--execution-providers", "cuda"]
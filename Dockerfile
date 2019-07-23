# base_python3镜像构建
#FROM alpine:latest
#RUN apk update && \
#    apk add curl python3 wget  --no-cache --update-cache  && \
#    pip3 install --upgrade pip



FROM registry.cn-beijing.aliyuncs.com/glodon-common/base_python3:latest
WORKDIR /webhook-wechat
COPY . /webhook-wechat/
#RUN echo "124.239.227.237 mirrors.aliyun.com" >> /etc/hosts
#RUN echo "http://mirrors.aliyun.com/alpine/v3.9/main/" > /etc/apk/repositories
#RUN echo "http://mirrors.aliyun.com/alpine/v3.9/community/" > /etc/apk/repositories
RUN apk update && \
    pip3 install flask itchat  -i http://pypi.douban.com/simple --trusted-host pypi.douban.com &&\
    mkdir -p /webhook-wechat/store
EXPOSE 8088
CMD ["python3", "-u","webhook-wechat.py"]


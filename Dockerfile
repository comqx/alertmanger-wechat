FROM alpine:latest
WORKDIR /webhook-wechat
COPY . /webhook-wechat/
#RUN echo "124.239.227.237 mirrors.aliyun.com" >> /etc/hosts
#RUN echo "http://mirrors.aliyun.com/alpine/v3.9/main/" > /etc/apk/repositories
#RUN echo "http://mirrors.aliyun.com/alpine/v3.9/community/" > /etc/apk/repositories
RUN apk update && \
    apk add curl python3 --no-cache --update-cache  && \
    pip3 install flask itchat  -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
EXPOSE 8088
CMD ["/bin/sh","run.sh"]


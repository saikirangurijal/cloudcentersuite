FROM alpine:latest as alpine

ENV PACKAGES="\
  bash \
  python2 \
  py-setuptools \
  build-base \
  linux-headers \
  python2-dev \
  py2-pip \
"


RUN echo \
# replacing default repositories with edge ones
&& echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" > /etc/apk/repositories \ 
&& echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories \
&& echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories \
&& apk add --no-cache $PACKAGES || (sed -i -e 's/dl-cdn/dl-4/g' /etc/apk/repositories && apk add --no-cache $PACKAGES)


ENTRYPOINT ["bash", "/ccsworker/serviceimport.sh"]

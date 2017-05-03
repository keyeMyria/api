FROM python:3.6-alpine
# FROM python:3.6-onbuild
# FROM ubuntu:latest

# add "tidyhtml" with alpine 3.5
RUN apk update && \
    apk add --no-cache postgresql-dev jpeg-dev zlib-dev libpq libxslt-dev libxslt python3-dev libc-dev linux-headers libxml2 libxml2-dev gcc musl-dev g++ libc6-compat libmagic
    # rm -rf /tmp/src && \
    # rm -rf /var/cache/apk/*

COPY requirements.txt /tmp/
RUN pip install pip -U
RUN pip install -r /tmp/requirements.txt --no-cache-dir && \
    rm -rf /tmp/src && \
    rm -rf /var/cache/apk/*

# RUN apt-get -y update && apt-get install -y \
# make \
# git \
# glusterfs-client \
# gettext \
# tidy \
# nodejs npm nodejs-legacy

RUN apk del postgresql-dev jpeg-dev zlib-dev libxslt-dev python3-dev libc-dev linux-headers libxml2-dev musl-dev && \
    rm -rf /tmp/src && \
    rm -rf /var/cache/apk/*


RUN mkdir /mnt/files
#CMD iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8000
WORKDIR /var/www/project/src
EXPOSE 8000
# CMD ls -la /var/www/pashinin.com/src
#CMD python3 ./manage.py runserver 0.0.0.0:8000 --settings=pashinin.settings
# CMD while :; do sleep 10; done

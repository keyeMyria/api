FROM python:3.6

# FROM python:3.6-alpine
#
# Why not Alpine:
# Alpine has error when compiling rust program and trying to run it
# inside Alpine (program uses glibc, Alpine - musl):
#
# __snprintf_chk: symbol not found

# Alpine:
# add "tidyhtml" with alpine 3.5
# RUN apk update && \
#     apk add --no-cache postgresql-dev jpeg-dev zlib-dev libpq libxslt-dev libxslt python3-dev libc-dev linux-headers libxml2 libxml2-dev gcc musl-dev g++ libc6-compat libmagic make libffi-dev

RUN apt-get update && \
    apt-get install -y libxslt-dev python3-dev libc-dev libxml2 libxml2-dev gcc musl-dev g++ make libffi-dev ruby && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/
RUN pip install pip -U
RUN pip install -r /tmp/requirements.txt --no-cache-dir && \
    rm -rf /tmp/src && \
    rm -rf /var/cache/apk/*

# Install ruby and ruby-bundler
# Alpine:
# RUN apk add --no-cache ruby

RUN gem install --no-document mustache

# RUN apt-get -y update && apt-get install -y \
# make \
# git \
# glusterfs-client \
# gettext \
# tidy \
# nodejs npm nodejs-legacy

# Alpine:
# RUN apk del postgresql-dev jpeg-dev zlib-dev libxslt-dev python3-dev libc-dev linux-headers libxml2-dev musl-dev && \
#     rm -rf /tmp/src && \
#     rm -rf /var/cache/apk/*


RUN mkdir /mnt/files
RUN chmod 777 /mnt/files
#CMD iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8000
WORKDIR /var/www/project/src
EXPOSE 8000
# CMD ls -la /var/www/pashinin.com/src
#CMD python3 ./manage.py runserver 0.0.0.0:8000 --settings=pashinin.settings
# CMD while :; do sleep 10; done

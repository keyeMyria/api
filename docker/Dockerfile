FROM python:3-onbuild
# FROM ubuntu:latest
COPY requirements.txt /tmp/

RUN apt-get -y update && apt-get install -y \
make \
git \
postgresql-server-dev-all
# redis-server \
# postgresql \

RUN pip3 install pip -U
RUN pip3 install -r /tmp/requirements.txt
#CMD iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8000
WORKDIR /var/www/pashinin.com/src
EXPOSE 8000
# CMD ls -la /var/www/pashinin.com/src
CMD python3 ./manage.py runserver 0.0.0.0:8000 --settings=pashinin.settings

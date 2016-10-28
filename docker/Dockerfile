FROM ubuntu:latest
COPY requirements.txt /tmp/

RUN apt-get -y update && apt-get install -y \
redis-server \
make \
python \
python3 \
python3-pip \
git \
postgresql \
postgresql-server-dev-all

RUN pip3 install pip -U
RUN pip3 install -r /tmp/requirements.txt
#CMD iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8000
WORKDIR /var/www/pashinin.com/src
CMD python3 ./manage.py runserver 0.0.0.0:8000 --settings=pashinin.settings

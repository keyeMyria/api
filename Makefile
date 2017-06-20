.PHONY: docker configs

python = `./configs/makeve.py`
vebin = `./configs/config.py -p vebin configs/secret-example.json configs/secret.json`
d = `pwd`
# vm = docker_web_1
# vm = pashinin.com:latest
vm = pashinin/pashinin.com:latest
container = pashinin/pashinin.com:latest
# container = pashinin.com
manage = $(python) src/manage.py
dockermanage.py = docker exec --user user -it $(container) python ./manage.py
# docker_run = docker-compose run --rm --env DJANGO_SETTINGS_MODULE='pashinin.settings' --env LD_LIBRARY_PATH='/var/www/pashinin.com/tmp/ve/lib' --volume `pwd`:/var/www/pashinin.com -w /var/www/pashinin.com/src -it $(container)
docker_run = docker-compose -f docker/docker-compose.yml run --rm django


all: install-docker-compose
	systemctl status docker | grep Active: | grep " active " -cq || systemctl start docker
	(cd docker;export UID; docker-compose up -d redis db django gulp)
# (cd docker;export UID; docker-compose up gulp)


install-docker-compose:
	which docker-compose || sudo pip install docker-compose

# docker run --name postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres


# docker run -ti -v `pwd`:/var/www/pashinin.com pashinin.com
# docker run -p 80:80 -d -v `pwd`:/var/www/pashinin.com pashinin.com
# All Docker VMs are described in docker/docker-compose.yml
docker: configs
	(cd docker; docker-compose up -d redis db)
	sleep 4
	(cd docker; docker-compose up dbinit)
	sleep 2
	(cd docker; docker-compose up migration)
	(cd docker; docker-compose up -d web)
	docker exec -it $(container) adduser user --uid `id -u` --quiet --disabled-password --gecos ""

docker-rebuild:
	docker build -t pashinin.com docker/

# Run "docker login" first
docker-push:
	docker tag pashinin.com pashinin/pashinin.com
	docker push pashinin/pashinin.com
	docker tag gulp pashinin/gulp
	docker push pashinin/gulp
	docker tag db pashinin/db
	docker push pashinin/db

configs:
	(cd configs; make templates)

dev: dev_pkgs

# $(manage) collectstatic --noinput -i *.scss -i *.sass -i *.less -i *.coffee -i *.map

start: docker

npm:
	npm install gulp gulp-sass gulp-livereload gulp-shell gulp-sourcemaps

bash:
	$(docker_run) sh

# --noworker - runserver will NOT start workers
django:
	docker exec --user www-data --env DJANGO_SETTINGS_MODULE='pashinin.settings' -it $(vm) ./manage.py runserver 0.0.0.0:8000
# docker run -it -v `pwd`:/var/www/pashinin.com pashinin.com ./manage.py runserver 0.0.0.0:8000 --settings=pashinin.settings

glusterfs:
	$(docker_run) mount.glusterfs 10.254.239.1:/v3 /mnt/files

gulp:
	docker exec $(vm) gulp

# For new app (no migrations, no changes detected) - create app with
# manage.py!
#
# docker exec --user user -it docker_web_1 ./manage.py startapp articles
#
# docker exec --user user -it $(vm) ./manage.py makemigrations your_app_label
# docker exec --user user -it docker_web_1 ./manage.py makemigrations articles
#
# ./manage.py migrate --fake default
migrate-docker:
	docker exec --user user -it $(vm) ./manage.py migrate --run-syncdb --settings=pashinin.settings
	docker exec --user user -it $(vm) ./manage.py makemigrations --settings=pashinin.settings
	docker exec --user user -it $(vm) ./manage.py migrate --settings=pashinin.settings

migrate:
	(cd docker;export UID;docker-compose run --rm django ./manage.py makemigrations --settings=pashinin.settings)
	(cd docker;export UID;docker-compose run --rm django ./manage.py migrate --settings=pashinin.settings)
# (cd docker;docker-compose run --rm django ./manage.py migrate --run-syncdb --settings=pashinin.settings)

loaddata:
	(cd docker;docker-compose run --rm django ./manage.py loaddata --settings=pashinin.settings initial_data.json articles_examples.json ege_subjects.json ege_exam.json ege_tasks.json categories.json tasks.json)
	# (cd docker;docker-compose run --rm django ./manage.py loaddata --settings=pashinin.settings )

vm:
	(cd docker; make vm)

psql:
	export UID; docker-compose -f docker/docker-compose.yml run --rm db psql -h db -U pashinin

stop:
	docker-compose -f docker/docker-compose.yml stop

recreate-db:
	docker container stop db
	docker container rm db
	(cd docker;export UID; docker-compose up -d redis db django gulp)

tmux:
	export LANG=en_US.UTF-8
	tmux new-session -s dev -d || echo "session created"
	tmux select-window -t runserver || tmux new-window -n runserver
	tmux send-keys -t runserver C-m 'make django' C-m
	tmux select-window -t gulp || tmux new-window -n gulp
	tmux send-keys -t gulp C-m 'gulp' C-m
	tmux select-window -t runserver
	tmux attach-session -t dev -d
# tmux select-window -t worker1 || tmux new-window -n worker1
# tmux send-keys -t worker1 C-m 'make worker1' C-m
# tmux select-window -t worker2 || tmux new-window -n worker2
# tmux send-keys -t worker2 C-m 'make worker2' C-m

worker1:
	docker exec --user www-data -it $(vm) ./manage.py runworker --exclude-channels=root.* --threads 4

worker2:
	docker exec -it $(vm) ./manage.py runworker --only-channels=root.*

ve:
	./configs/makeve.py
# TODO: upgrade pip

link_debug_parser:
	ln -sf /var/www/parser/build/lib/rparser /usr/local/lib/python3.6/rparser
# docker exec -it $(vm)

rparser:
	ln -sf ../rparser/rparser src/rparser
	(cd ../rparser/rparser; ln -sf ../build/lib/rparser/librparser.so librparser.so)
	(cd docker;export UID; docker-compose restart django)
# (cd docker;export UID; docker-compose run --rm django ls)
# (cd docker;export UID; docker-compose run --rm django ln -sf ../../rparser/build/lib/rparser/librparser.so ../../rparser/rparser/librparser.so)
	# (cd docker;export UID; docker-compose up -d django)
# (cd docker;export UID; docker-compose run --rm django python manage.py shell)

pip:
	$(vebin)/pip3 install -r docker/requirements.txt

pip-docker:
	$(docker_run) pip install -r ../docker/requirements.txt
# docker exec -it $(vm) pip3 install -r ../docker/requirements.txt

pull:
	sudo -H -u www-data git pull


update:
	sudo -H -u www-data git pull
	make pip
	sudo -H -u www-data make configs
	sudo -H -u www-data make css
	sudo -H -u www-data make collectstatic
	(cd configs; make ln_nginx)
	(cd src; `python ../configs/makeve.py` manage.py migrate)
	sudo supervisorctl restart worker-pashinin.com
	sudo service nginx reload

# TODO: edit pg_hba.conf - put 127.0.0.1 trust
prod: pull
	sudo -H -u www-data make configs
	(cd configs; make ln_nginx)
	mkdir -p /mnt/files
	mount.glusterfs 10.254.239.1:/v3 /mnt/files
	psql -a -f configs/tmp/dbinit.sql -U postgres -p 5434 -h localhost
	(cd src; ./manage.py makemigrations; ./manage.py migrate)
	sudo service nginx reload

# (cd src; ../configs/migrations.sh)

# mkdir -p /var/www/pashinin.com
# cd /var/www/pashinin.com
# sudo -H -u www-data git clone https://github.com/pashinin-com/pashinin.com.git initial
# # sudo -H -u www-data git pull
# cd initial
# sudo -H -u www-data make prod

dbinit-docker:
	docker exec -it $(container) psql -a -f ../configs/tmp/dbinit.sql -U postgres -p 5432 -h db

collectstatic:
	tmp/ve/bin/python src/manage.py collectstatic --noinput -i *.scss -i *.sass -i *.less -i *.coffee -i *.map -i *.md

collectstatic-dev:
	docker exec --user user -it $(container) ./manage.py collectstatic --noinput -i *.scss -i *.sass -i *.less -i *.coffee -i *.map -i *.md

# sudo -H -u www-data tmp/ve/bin/python src/manage.py collectstatic

# Look for all .scss files not starting with "_"
# Exclude folders: ./node_modules, ./static
# TODO: install apt: parallel
#
# sass --help
# --sourcemap=TYPE   [auto(default),none]
css: sass
	find . -type f -name "*.scss" -not -name "_*" -not -path "./node_modules/*" -not -path "./static/*" \
-print | parallel --no-notice sass --cache-location /tmp/sass --style compressed --sourcemap=none {} {.}.css

sass:
	sass -v > /dev/null || sudo su -c "gem install sass"

shell:
	(cd docker;export UID; docker-compose run --rm django python manage.py shell_plus)
# sudo -H -u www-data tmp/ve/bin/python ./src/manage.py shell

shell-docker:
	docker run --env DJANGO_SETTINGS_MODULE='pashinin.settings' --volume `pwd`:/var/www/pashinin.com -w /var/www/pashinin.com/src -it $(container) ./manage.py shell
# docker exec --user user -it $(vm) ./manage.py shell

python-docker:
	$(docker_run) ipython

ege:
	docker exec --user www-data --env DJANGO_SETTINGS_MODULE='ege.settings_ege' -it $(vm) ./manage.py runserver 0.0.0.0:8001

locale-docker:
	$(dockermanage.py) makemessages -l ru --no-obsolete --no-wrap --traceback --ignore=katex* -e jinja,py

localecompile-docker:
	$(dockermanage.py) compilemessages

localecompile:
	sudo -H -u www-data tmp/ve/bin/python ./src/manage.py compilemessages

py:
	$(python)

# testcmd = /bin/sh -c "cd ..;pytest -vv --durations=3"
testcmd = /bin/sh -c "pytest -vv --durations=3"
# test: flake8 install_docker
# install_docker
test:
	(cd docker; $(docker_run) $(testcmd))
# docker exec --user user --env DJANGO_SETTINGS_MODULE='pashinin.settings' -it $(testcmd)
# docker exec --user user --env DJANGO_SETTINGS_MODULE='ege.settings_ege' -it $(testcmd)
# docker exec --user user --env DJANGO_SETTINGS_MODULE='pashinin.settings' -it $(vm) /bin/sh -c "cd ..;pytest -vv -n3 --durations=3 --cov src --cov-report term-missing"

flake8: install_flake8
	flake8 src --exclude=*/migrations/*,__pycache__,settings*.py

install_flake8:
	(cd src; python3 -c 'from core.tasks import install;install("flake8")')
# sudo apt-get install python-flake8

install_docker:
	(cd src; python3 -c 'from core.tasks import install;install("docker")')

tidy:
	curl https://pashinin.com | tidy -config configs/tidy.conf

render:
	mkdir -p configs/tmp
	(cd configs;./config.py secret-example.json secret.json)
	(cd configs/; ./render.py)
	(cd src; python3 -c 'from core.tasks import generate_settings;generate_settings()')

# docker kill $(docker ps -q)
clean:
	docker rm `docker ps --no-trunc -aq`


hosts:
	(cd configs; sudo python hosts.py)

files:
	ag -o --nofilename --nogroup "{{\s*file\(.+}}"

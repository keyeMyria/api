.PHONY: docker configs

python = `./configs/makeve.py`
vebin = `./configs/config.py -p vebin configs/secret-example.json configs/secret.json`
d = `pwd`
vm = docker_web_1
manage = $(python) src/manage.py
dockermanage.py = docker exec --user user -it $(vm) python ./manage.py

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
	docker exec -it $(vm) adduser user --uid `id -u` --quiet --disabled-password --gecos ""
# docker exec -it $(vm) ln -sf /var/www/parser/build/lib/rparser /usr/local/lib/python3.6/rparser

# docker exec -it docker_web_1 userdel user
	# (cd docker; docker-compose up -d db redis)
# docker-compose up --force-recreate
# --no-deps db redis

dev: dev_pkgs

# $(manage) collectstatic --noinput -i *.scss -i *.sass -i *.less -i *.coffee -i *.map

start: docker

dev_pkgs:
	npm install gulp gulp-sass gulp-livereload gulp-shell gulp-sourcemaps

bash:
	docker exec -it $(vm) bash

# --noworker - runserver will NOT start workers
django:
	docker exec --user www-data --env DJANGO_SETTINGS_MODULE='pashinin.settings' -it $(vm) ./manage.py runserver 0.0.0.0:8000
# docker run -it -v `pwd`:/var/www/pashinin.com pashinin.com ./manage.py runserver 0.0.0.0:8000 --settings=pashinin.settings

glusterfs:
	docker exec $(vm) mount.glusterfs 10.254.239.1:/v3 /mnt/files

gulp:
	docker exec $(vm) gulp

configs:
	(cd configs; make templates)

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

vm:
	(cd docker; make vm)

psql:
	docker exec -it --user postgres docker_db_1 psql

recreate: stop
	# sudo find -type d -name migrations -exec rm -rf {} \;
	(cd docker; docker rm docker_db_1; docker rm docker_web_1;)
	make docker

stop:
	docker stop $(vm)
	docker stop docker_db_1
	docker stop docker_redis_1

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
	ln -sf /var/www/parser/build/lib/rparser/ /usr/local/lib/python3.6/rparser/
# docker exec -it $(vm)

pip:
	$(vebin)/pip3 install -r docker/requirements.txt

pip-docker:
	docker exec -it $(vm) pip3 install -r ../docker/requirements.txt

pull:
	sudo -H -u www-data git pull


update:
	sudo -H -u www-data git pull
	make pip
	sudo -H -u www-data make configs
	(cd configs; make ln_nginx)
	(cd src; ./manage.py migrate)
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
	docker exec -it $(vm) psql -a -f ../configs/tmp/dbinit.sql -U postgres -p 5432 -h db

collectstatic:
	sudo -H -u www-data tmp/ve/bin/python ./src/manage.py collectstatic --noinput -i *.scss -i *.sass -i *.less -i *.coffee -i *.map -i *.md

collectstatic-dev:
	docker exec --user user -it $(vm) ./manage.py collectstatic --noinput -i *.scss -i *.sass -i *.less -i *.coffee -i *.map -i *.md

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
	sudo -H -u www-data tmp/ve/bin/python ./src/manage.py shell

# python setup.py install develop
# pip uninstall your-local-repo-egg
# docker exec -it $(vm) pip3 install rparser -vvvv --no-index --find-links file:///var/www/parser
# --upgrade --force-reinstall
# build_rust
# docker exec -it $(vm) /bin/sh -c 'cd /var/www/parser;python3 setup.py install --force'
parser:
	docker exec -it $(vm) /bin/sh -c 'cd /var/www/parser;python3 setup.py build_rust'

# docker exec -it $(vm) /bin/sh -c 'cd /var/www/parser;python3 setup.py bdist_wheel'
# docker exec -it $(vm) python3 -m pip wheel /var/www/parser/ -w /wheelhouse/
wheel:
	python3 -m pip wheel . -w /wheelhouse/

parsertest:
	docker exec -it $(vm) python3 -c 'from rparser import article_render'

ege:
	docker exec --user www-data --env DJANGO_SETTINGS_MODULE='ege.settings_ege' -it $(vm) ./manage.py runserver 0.0.0.0:8001
# docker exec --user www-data $(vm) export DJANGO_SETTINGS_MODULE="ege.settings";
# --settings=ege.settings

locale-docker:
	$(dockermanage.py) makemessages -l ru --no-obsolete --no-wrap --traceback --ignore=katex* -e jinja,py

localecompile-docker:
	$(dockermanage.py) compilemessages

localecompile:
	sudo -H -u www-data tmp/ve/bin/python ./src/manage.py compilemessages

py:
	$(python)

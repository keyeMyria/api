.PHONY: docker configs

SHELL := /bin/bash
python = `./configs/makeve.py`
vebin = `./configs/config.py -p vebin configs/secret-example.json configs/secret.json`
d = `pwd`
# vm = docker_web_1
# vm = pashinin.com:latest
vm = pashinin/pashinin.com:latest
container = pashinin/pashinin.com:latest
# container = pashinin.com
manage = $(python) src/manage.py
# docker_run = docker-compose run --rm --env DJANGO_SETTINGS_MODULE='pashinin.settings' --env LD_LIBRARY_PATH='/var/www/pashinin.com/tmp/ve/lib' --volume `pwd`:/var/www/pashinin.com -w /var/www/pashinin.com/src -it $(container)

os = `lsb_release -i | cut -zb 17-`
codename = `lsb_release -cs`
settings=pashinin.settings
# docker-compose=cd docker;export UID; docker-compose
docker-compose=export UID; docker-compose -f docker/docker-compose.yml
# dockermanage.py = docker exec --user user -it $(container) python ./manage.py
dockermanage.py = $(docker-compose) run --rm django python ./manage.py
docker_run = $(docker-compose) run --rm django
uglifyjs = ./node_modules/uglify-es/bin/uglifyjs
sass = ./node_modules/node-sass/bin/node-sass --include-path node_modules


# Errors that can happen:
# ERROR: for db  Cannot start service db: oci runtime error: container_linux.go:265: starting container process caused "process_linux.go:284: applying cgroup configuration for process caused \"failed to write 15422 to cgroup.procs: write /sys/fs/cgroup/cpu,cpuacct/docker/eae4198a69bfa819781cc2e833a3f91a63097dce833e6240c9911df28ee83f0f/cgroup.procs: invalid argument\""

all: install-docker-compose install-docker
	systemctl status docker | grep Active: | grep " active " -cq || systemctl start docker
	$(docker-compose) up -d redis db django vnu || printf "* * * * *\n* %s\n* * * * *\n" "Have you logged out and back in after you were added to docker group?"
	[ ! -f tmp/run-migrations ] || (make migrate && make loaddata && rm -f tmp/run-migrations)
#	gulp
# (cd docker;export UID; docker-compose up gulp)


install-docker-compose:
	which docker-compose || sudo -H pip install docker-compose

install-docker:
	which docker || \
	if [[ "$(os)" == "Ubuntu" ]] ; then make install-docker-ubuntu; fi;

install-docker-ubuntu:
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
	sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
$(codename) \
stable"
	sudo apt-get update
	sudo apt-get -y install docker-ce
	sudo gpasswd -a `whoami` docker
	echo "You were added to the docker group. Log out and log in again!!!"
	sudo systemctl restart docker

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

bash:
	$(docker_run) bash

test-livereload:
	$(docker_run) curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" -H "Host: example.org" -H "Origin: http://example.org" http://example.org

# --noworker - runserver will NOT start workers
django:
	docker exec --user www-data --env DJANGO_SETTINGS_MODULE='$(settings)' -it $(vm) ./manage.py runserver 0.0.0.0:8000
# docker run -it -v `pwd`:/var/www/pashinin.com pashinin.com ./manage.py runserver 0.0.0.0:8000 --settings=pashinin.settings

glusterfs:
	$(docker_run) mount.glusterfs 10.254.239.1:/v3 /mnt/files

npm:
	npm install gulp gulp-sass gulp-livereload gulp-shell gulp-sourcemaps \
					 gulp-typescript typescript gulp-buffer

gulp:
	./node_modules/gulp/bin/gulp.js
#$(docker-compose) run gulp


# For new app (no migrations, no changes detected) - create app with
# manage.py!
#
# docker exec --user user -it docker_web_1 ./manage.py startapp articles
#
# docker exec --user user -it $(vm) ./manage.py makemigrations your_app_label
# docker exec --user user -it docker_web_1 ./manage.py makemigrations articles
#
# ./manage.py migrate --fake default
# migrate-docker:
# 	docker exec --user user -it $(vm) ./manage.py migrate --run-syncdb --settings=$(settings)
# 	docker exec --user user -it $(vm) ./manage.py makemigrations --settings=$(settings)
# 	docker exec --user user -it $(vm) ./manage.py migrate --settings=$(settings)

migrate:
	$(docker-compose) run --rm django ./manage.py makemigrations --settings=$(settings)
	$(docker-compose) run --rm django ./manage.py migrate --settings=$(settings)
# (cd docker;docker-compose run --rm django ./manage.py migrate --run-syncdb --settings=$(settings))

loaddata:
	$(docker-compose) run --rm django ./manage.py loaddata --settings=$(settings) \
initial_data.json
# initial_data.json articles_examples.json ege_subjects.json ege_exam.json ege_tasks.json categories.json tasks.json
#	(cd docker;docker-compose run --rm django ./manage.py loaddata --settings=pashinin.settings )

vm:
	(cd docker; make vm)

psql:
	$(docker-compose) run --rm db psql -h db -U pashinin  # need user here (or will be "root")

stop:
	$(docker-compose) stop

removedb:
	docker stop db || true && docker rm db || true
#	[ "$(docker ps -a | grep db)" ] && docker container stop db
#	[ "$(docker ps -a | grep db)" ] && docker container rm db

recreate-db: removedb
	chmod 777 tmp
	$(docker-compose) up db  # running NOT as daemon to see log and errors

db-up:
	$(docker-compose) up db

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

# Create a virtualenv if it doesn't exist
# Do not do it if we are in Travis build
ve:
	./configs/makeve.py  # always prints a path to python executable
# TODO: upgrade pip

link_debug_parser:
	ln -sf /var/www/parser/build/lib/rparser /usr/local/lib/python3.6/rparser
# docker exec -it $(vm)

rparser:
	ln -sf ../rparser/rparser src/rparser
	(cd ../rparser/rparser; ln -sf ../build/lib/rparser/librparser.so librparser.so)
	$(docker-compose) restart django

requirements:
	$(vebin)/pip install -r docker/requirements.txt
	if [[ "$(TRAVIS)" == "true" ]] && [[ "$(TRAVIS_PYTHON_VERSION)" == "pypy3" ]] ; then pip install psycopg2cffi; fi;
	if [[ "$(TRAVIS)" == "true" ]] && [[ "$(TRAVIS_PYTHON_VERSION)" != "pypy3" ]] ; then pip install psycopg2; fi;

pip:
	$(vebin)/pip3 install -r docker/requirements.txt

pip-docker:
	$(docker_run) pip install -r ../docker/requirements.txt
# docker exec -it $(vm) pip3 install -r ../docker/requirements.txt

pull:
	sudo -H -u www-data git pull

# Rebuild and prepare all configs locally (inside current folder)
# Also update npm packages, css and js files
# Must run as www-data user (sudo -H -u www-data make prepare)
prepare:
	make ve
	make requirements
	yarn install
	make configs
	make css

update:
	sudo -H -u www-data git pull
	make pip
	sudo -H -u www-data yarn install
	sudo -H -u www-data make configs
	sudo -H -u www-data make css
	sudo -H -u www-data make links
	sudo -H -u www-data make js
	sudo -H -u www-data make collectstatic
	(cd configs; make ln_nginx)
	(cd src; `python ../configs/makeve.py` manage.py migrate)
	sudo supervisorctl restart worker-pashinin.com
	sudo service nginx reload
	sudo service bind9 reload
# TODO: check bind config before restart. How? Do it in Travis?
# named-checkconf

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

#  Static files
#
# --noinput     Do NOT prompt the user for input of any kind
#
# -i            ignore some files
# The default ignored pattern list, ['CVS', '.*', '*~']
#
#
# --dry-run, -n¶
#     Do everything except modify the filesystem.

createinitialrevisions-dev:
	$(docker_run) sh -c "./manage.py createinitialrevisions"

createinitialrevisions:
	tmp/ve/bin/python src/manage.py createinitialrevisions

static_files = -i *.scss -i *.sass -i *.less -i *.coffee -i "*.md"
collectstatic:
	tmp/ve/bin/python src/manage.py collectstatic --noinput $(static_files)

collectstatic-dev:
	$(docker_run) ./manage.py collectstatic --noinput $(static_files)

# sudo -H -u www-data tmp/ve/bin/python src/manage.py collectstatic

# Look for all .scss files not starting with "_"
# Exclude folders: ./node_modules, ./static
# TODO: install apt: parallel
#
# sass --help
# --sourcemap=TYPE   [auto(default),none]
# ./node_modules/node-sass/bin/node-sass
css:
	find . -type f -name "*.scss" -not -name "_*" -not -path "*/js/libs/*" -not -path "./node_modules/*" -not -path "./static/*" \
-print | parallel --no-notice $(sass) -q --cache-location /tmp/sass --output-style compressed --sourcemap=none {} {.}.css

typescript:
	find ./src -type f -name "*.ts" -not -name "_*" -not -path "./node_modules/*" -not -path "./static/*" \
-print | parallel --no-notice tsc --lib es6,dom {}

shell:
	if [[ "$(DISPLAY)" == "" ]] ; then sudo -H -u www-data tmp/ve/bin/python ./src/manage.py shell; fi;
	if [[ "$(DISPLAY)" != "" ]] ; then $(dockermanage.py) shell_plus; fi;

locale-docker:
	$(dockermanage.py) makemessages -l ru --no-obsolete --no-wrap --traceback --ignore=katex* -e jinja,py

localecompile-docker:
	$(dockermanage.py) compilemessages

localecompile:
	sudo -H -u www-data tmp/ve/bin/python ./src/manage.py compilemessages

flake8: install_flake8
	flake8 src --exclude=*/migrations/*,__pycache__,settings*.py

install_flake8:
	(cd src; python3 -c 'from core.tasks import install;install("flake8")')
# sudo apt-get install python-flake8

install_docker:
	(cd src; python3 -c 'from core.tasks import install;install("docker")')

render:
	mkdir -p configs/tmp
	(cd configs;./config.py secret-example.json secret.json)  # generate configs/tmp/conf.json
	$(python) configs/render.py
	(cd src; python3 -c 'from core.tasks import generate_settings;generate_settings()')

# docker kill $(docker ps -q)
clean:
	docker rm `docker ps --no-trunc -aq`

hosts:
	(cd configs; sudo python hosts.py)

files:
	ag -o --nofilename --nogroup "{{\s*file\(.+}}"


# Javascript
js_files = find ./src -type f -name "*.js" -not -name "*.min.js" -not -path "*/js/libs/*" -not -name "*.mini.js" -print | parallel --no-notice

# 2 step. Will fix require is not defined
browserify-js:
	$(js_files) ./node_modules/browserify/bin/cmd.js {.}.min.js -o {.}.min.js

# For ES5 (2009): sudo npm install -g uglify-js
# For ES6 (2015): sudo npm install -g uglify-es
#
# $ uglifyjs -V
# uglify-js 3.0.28
minify-js:
	$(js_files) ./node_modules/uglify-es/bin/uglifyjs {.}.min.js -m -o {.}.min.js

# 1 step. ES6 -> ES5 (imports -> require)
# --minified --no-comments
babel-js:
	$(js_files) ./node_modules/babel-cli/bin/babel.js {} -o {.}.min.js

js:
	make babel-js       # ES6 -> ES5
	make browserify-js  # require is not defined
	make minify-js

js-print:
	$(js_files) echo {}

js-dev:
	gulp js


# Tests

test-js-style:
	./node_modules/eslint/bin/eslint.js ./src

test-python-style:
	flake8 src --exclude=*/migrations/*,__pycache__,settings*.py

testcmd = pytest -vv --durations=3
test:
	mkdir -p tmp/files
	if [[ "$(TRAVIS)" == "true" ]] ; then $(testcmd) --cov-config .coveragerc --cov src --cov-report term-missing; fi;
	if [[ "$(TRAVIS)" != "true" ]] ; then $(docker_run) $(testcmd); fi;

api:
	./node_modules/browserify/bin/cmd.js src/core/static/js/api.min.js -t --outfile  src/core/static/js/api.min.js

links:
	cp -f node_modules/moment/min/moment.min.js src/core/static/js/libs/
	cp -f node_modules/moment/locale/ru.js src/core/static/js/libs/moment.ru.min.js
	cp -f node_modules/moment-timezone/builds/moment-timezone-with-data.min.js src/core/static/js/libs/
	cp -f node_modules/raven-js/dist/raven.js src/core/static/js/libs/
	cp -f node_modules/raven-js/dist/raven.min.js src/core/static/js/libs/
	cp -f node_modules/raven-js/dist/raven.min.js.map src/core/static/js/libs/

	$(uglifyjs) node_modules/dropzone/dist/dropzone.js -m -o src/core/static/js/libs/dropzone.min.js
	$(uglifyjs) node_modules/whatwg-fetch/fetch.js -m -o src/core/static/js/libs/fetch.min.js

	cp -rf node_modules/photoswipe/dist src/core/static/js/libs/photoswipe
	cp -f node_modules/raven-js/dist/raven.min.js src/core/static/js/libs/


# get IP of a container
# docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name_or_id

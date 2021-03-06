.PHONY: docker configs

SHELL := /bin/bash
python = `./configs/makeve.py`
vebin = `./configs/config.py -p vebin configs/secret-example.json configs/secret.json`
d = `pwd`
vm = pashinin/pashinin.com:latest
container = pashinin/pashinin.com:latest
manage = $(python) src/manage.py
os = `lsb_release -i | cut -zb 17-`
codename = `lsb_release -cs`
# settings=pashinin.settings
settings=`cat src/current_app.txt`.settings
# docker-compose=export UID; docker-compose -f docker/docker-compose.yml
docker-compose=export UID; docker-compose
dockermanage.py = $(docker-compose) run --rm django python ./manage.py
docker_run = $(docker-compose) run --rm django
uglifyjs = ./node_modules/uglify-es/bin/uglifyjs
sass = ./node_modules/node-sass/bin/node-sass --include-path node_modules


# Errors that can happen:
# ERROR: for db  Cannot start service db: oci runtime error: container_linux.go:265: starting container process caused "process_linux.go:284: applying cgroup configuration for process caused \"failed to write 15422 to cgroup.procs: write /sys/fs/cgroup/cpu,cpuacct/docker/eae4198a69bfa819781cc2e833a3f91a63097dce833e6240c9911df28ee83f0f/cgroup.procs: invalid argument\""

all: install-docker-compose install-docker
	systemctl status docker | grep Active: | grep " active " -cq || systemctl start docker
	$(docker-compose) up -d db django vnu celery || printf "* * * * *\n* %s\n* * * * *\n" "Have you logged out and back in after you were added to docker group?"
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

docker-rebuild:
	docker build -t pashinin.com docker/

local-restart:
	sudo systemctl restart daphne
	sudo systemctl restart worker
#	sudo systemctl stop worker-root
#	sudo systemctl restart worker-root
	sudo systemctl restart nginx
	sudo systemctl restart celery-root
	sudo systemctl restart celery


local-stop:
	sudo systemctl stop daphne
	sudo systemctl stop worker
	sudo systemctl stop worker-root



# Run "docker login" first
docker-push:
	docker tag pashinin.com pashinin/pashinin.com
	docker push pashinin/pashinin.com

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
# $(docker-compose) run --rm django ./manage.py migrate --settings=$(settings)
# django_celery_results
# (cd docker;docker-compose run --rm django ./manage.py migrate --run-syncdb --settings=$(settings))

celery:
	$(docker-compose) run --rm django celery -A pashinin worker -l info

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
	$(docker-compose) stop || docker stop $(docker ps -a -q)
#	docker update --restart=no 0fed1e862c2c

stop-redis-1:
	$(docker-compose) stop redis_1

removedb:
	docker stop db || true && docker rm db || true

recreate-db: removedb
	chmod 777 tmp
	$(docker-compose) up db  # running NOT as daemon to see log and errors

db-up:
	$(docker-compose) up db

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
	(cd src; ../tmp/ve/bin/python -c 'from core.install import requirements;requirements()')
#	$(vebin)/pip install -r docker/requirements.txt
	if [[ "$(TRAVIS)" == "true" ]] && [[ "$(TRAVIS_PYTHON_VERSION)" == "pypy3" ]] ; then pip install psycopg2cffi; fi;
	if [[ "$(TRAVIS)" == "true" ]] && [[ "$(TRAVIS_PYTHON_VERSION)" != "pypy3" ]] ; then pip install psycopg2; fi;
	if [[ "$(TRAVIS)" == "" ]] ; then $(vebin)/pip install psycopg2; fi;

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
	make jslibs
	make js
	make collectstatic

config-links:
	(cd configs; sudo make somelinks)

update:
	sudo -H -u www-data git pull
	make pip
	sudo -H -u www-data yarn install
	sudo -H -u www-data make configs
	sudo -H -u www-data make css
	sudo -H -u www-data make jslibs
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

shell-prod:
	sudo -H -u www-data tmp/ve/bin/python ./src/manage.py shell

locale-docker:
	$(dockermanage.py) makemessages -l ru --no-obsolete --no-wrap --traceback --ignore=katex* -e jinja,py

localecompile-docker:
	$(dockermanage.py) compilemessages

localecompile:
	sudo -H -u www-data tmp/ve/bin/python ./src/manage.py compilemessages

flake8: install_flake8
	flake8 src --exclude=*/migrations/*,__pycache__,settings*.py

install_flake8:
	$(python) -c 'import flake8' || $(vebin)/pip install flake8
#	which flake8 || sudo -H pip install flake8
#	(cd src; $(python) -c 'from core.tasks import install;install("flake8")')
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
	docker system prune
#	docker rm `docker ps --no-trunc -aq`

hosts:
	(cd configs; sudo python hosts.py)

files:
	ag -o --nofilename --nogroup "{{\s*file\(.+}}"


# Javascript
js_files = find ./src -type f -name "*.js" -not -name "*.min.js" -not -path "*/js/libs/*" -not -name "*.mini.js" -print | parallel --no-notice

# 2 step. Will fix "require is not defined"
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

test-python-style: install_flake8
	$(python) -m flake8 src --exclude=*/migrations/*,__pycache__,settings*.py

testcmd = pytest -vv --durations=3
test:
	mkdir -p tmp/files
	if [[ "$(TRAVIS)" == "true" ]] ; then $(testcmd) --cov-config .coveragerc --cov src --cov-report term-missing; fi;
	if [[ "$(TRAVIS)" != "true" ]] ; then $(docker_run) $(testcmd); fi;

api:
	./node_modules/browserify/bin/cmd.js src/core/static/js/api.min.js -t --outfile  src/core/static/js/api.min.js

jslibs:
	cp -f node_modules/moment/min/moment.min.js src/core/static/js/libs/
	cp -f node_modules/moment/locale/ru.js src/core/static/js/libs/moment.ru.min.js
	cp -f node_modules/moment-timezone/builds/moment-timezone-with-data.min.js src/core/static/js/libs/
	cp -f node_modules/raven-js/dist/raven.js src/core/static/js/libs/
	cp -f node_modules/raven-js/dist/raven.min.js src/core/static/js/libs/
	cp -f node_modules/raven-js/dist/raven.min.js.map src/core/static/js/libs/

	cp -f node_modules/livereload-js/dist/livereload.js src/core/static/js/libs/livereload.min.js

	$(uglifyjs) node_modules/dropzone/dist/dropzone.js -m -o src/core/static/js/libs/dropzone.min.js
	$(uglifyjs) node_modules/whatwg-fetch/fetch.js -m -o src/core/static/js/libs/fetch.min.js

	cp -rf node_modules/photoswipe/dist src/core/static/js/libs/photoswipe
	cp -f node_modules/raven-js/dist/raven.min.js src/core/static/js/libs/

# systemd:
#	sudo ln -sf $(d)/configs/tmp/systemd-daphne.service /etc/systemd/system/daphne.service

install:
	make prepare
	make config-links
	(cd src; `python ../configs/makeve.py` manage.py migrate)
#	TODO: Install Sentry (make it highly available too)
#	(cd src; ../tmp/ve/bin/python -c 'from core.install import install_project_locally;install_project_locally()')
#	(cd src; ../tmp/ve/bin/python -c 'from core.install import install_vault;install_vault()')
#	(cd src; ../tmp/ve/bin/python -c 'from core.install import stolon;stolon.install()')
	sudo systemctl daemon-reload

	sudo systemctl enable worker.service
	sudo systemctl stop worker.service
	sudo systemctl start worker.service

	sudo systemctl enable daphne.service
	sudo systemctl stop daphne.service
	sudo systemctl start daphne.service
	sudo service nginx reload

docs:
	echo 1

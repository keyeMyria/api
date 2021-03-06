# -*- Makefile -*-

# really need this - back and forward to 'configs' folder
# (we may be inside 'src' dir, not 'configs')
python = `python ../configs/makeve.py`
# python = ../tmp/ve/python
S = tmp/conf.json
supervisor_confd = /etc/supervisor/conf.d
# supervisor_confd = .
output = tmp
dir = `realpath $(output)`
domain = `python config.py -p domain secret-example.json secret.json`
mustache = ../node_modules/mustache/bin/mustache $(S)

templates:
	mkdir -p $(output)

# create conf.json
	python config.py secret-example.json secret.json

# $(mustache) daphne.conf.mustache > $(output)/daphne.conf
	$(mustache) worker.conf.mustache > $(output)/worker.conf
	$(mustache) supervisor/celery.conf.mustache > $(output)/celery.conf
	$(mustache) supervisor/celerybeat.conf.mustache > $(output)/celerybeat.conf
	$(mustache) supervisor/celery_flower.conf.mustache > $(output)/celery_flower.conf
	(cd ../src; $(python) -c 'from core.tasks.update import generate_settings;generate_settings()')
	(cd ../src; $(python) -c 'from core.tasks.update import render_configs;render_configs()')
	$(mustache) nginx.conf.mustache > $(output)/nginx.conf

	$(mustache) bind.zone.mustache > $(output)/$(domain).zone

	$(mustache) phpfpm_params.mustache > $(output)/phpfpm_params
	$(mustache) nginx-site.conf.mustache > $(output)/$(domain).conf
	$(mustache) dbinit.sql.template > $(output)/dbinit.sql

# Must run as root (sudo make somelinks)
somelinks:
# Nginx config (current domain):
	ln -sf $(dir)/$(domain).conf /etc/nginx/sites-enabled/$(domain).conf
# Worker:
#	ln -sf $(dir)/systemd-daphne.service /etc/systemd/system/daphne.service
	rm /etc/systemd/system/daphne.service || true
	cp -f $(dir)/systemd-daphne.service /etc/systemd/system/daphne.service

	rm /etc/systemd/system/celery.service || true
	cp -f $(dir)/systemd-celery.service /etc/systemd/system/celery.service

	rm /etc/systemd/system/celery-root.service || true
	cp -f $(dir)/systemd-celery-root.service /etc/systemd/system/celery-root.service

# Workers:
	rm /etc/systemd/system/worker-root.service || true
#	cp -f $(dir)/systemd-worker-root.service /etc/systemd/system/worker-root.service

	rm /etc/systemd/system/worker.service || true
	cp -f $(dir)/systemd-worker.service /etc/systemd/system/worker.service

	systemctl daemon-reload

ln_nginx:
	sudo ln -sf $(dir)/$(domain).conf /etc/nginx/sites-enabled/$(domain).conf

# Realy need to copy! No symlinks! Bind does not read symlinks
	sudo cp -f $(dir)/$(domain).zone /etc/bind/$(domain).zone
	sudo chown bind /etc/bind/$(domain).zone

# Link Celery beat
	sudo ln -sf $(dir)/celerybeat.conf $(supervisor_confd)/celerybeat-$(domain).conf

ln_nginxmain:
	sudo ln -sf $(dir)/nginx.conf /etc/nginx/nginx.conf

links: ln_nginx ln_nginxmain
	sudo ln -sf $(dir)/daphne.conf $(supervisor_confd)/daphne-$(domain).conf
	sudo ln -sf $(dir)/worker.conf $(supervisor_confd)/worker-$(domain).conf
	sudo ln -sf $(dir)/celery.conf $(supervisor_confd)/celery-$(domain).conf
	sudo ln -sf $(dir)/celerybeat.conf $(supervisor_confd)/celerybeat-$(domain).conf
	sudo ln -sf $(dir)/celery_flower.conf $(supervisor_confd)/celery_flower-$(domain).conf
	sudo ln -sf $(dir)/phpfpm_params /etc/nginx/phpfpm_params

removelinks:
	sudo rm /etc/nginx/sites-enabled/$(domain).conf
	sudo rm $(supervisor_confd)/daphne-$(domain).conf

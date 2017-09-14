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

templates:
	mkdir -p $(output)
	python3.6 config.py secret-example.json secret.json
	# mustache $(S) daphne.conf.mustache > $(output)/daphne.conf
	mustache $(S) worker.conf.mustache > $(output)/worker.conf
	mustache $(S) supervisor/celery.conf.mustache > $(output)/celery.conf
	mustache $(S) supervisor/celery_flower.conf.mustache > $(output)/celery_flower.conf
	(cd ../src; $(python) -c 'from core.tasks.update import generate_settings;generate_settings()')
	mustache $(S) nginx.conf.mustache > $(output)/nginx.conf

	sudo chown www-data $(dir)/$(domain).zone
	mustache $(S) bind.zone.mustache > $(output)/$(domain).zone

	mustache $(S) phpfpm_params.mustache > $(output)/phpfpm_params
	mustache $(S) nginx-site.conf.mustache > $(output)/$(domain).conf
	mustache $(S) dbinit.sql.template > $(output)/dbinit.sql

ln_nginx:
	sudo ln -sf $(dir)/$(domain).conf /etc/nginx/sites-enabled/$(domain).conf
	sudo ln -sf $(dir)/$(domain).zone /etc/bind/$(domain).zone
	sudo chown bind $(dir)/$(domain).zone

ln_nginxmain:
	sudo ln -sf $(dir)/nginx.conf /etc/nginx/nginx.conf

links: ln_nginx ln_nginxmain
	sudo ln -sf $(dir)/daphne.conf $(supervisor_confd)/daphne-$(domain).conf
	sudo ln -sf $(dir)/worker.conf $(supervisor_confd)/worker-$(domain).conf
	sudo ln -sf $(dir)/celery.conf $(supervisor_confd)/celery-$(domain).conf
	sudo ln -sf $(dir)/celery_flower.conf $(supervisor_confd)/celery_flower-$(domain).conf
	sudo ln -sf $(dir)/phpfpm_params /etc/nginx/phpfpm_params

removelinks:
	sudo rm /etc/nginx/sites-enabled/$(domain).conf
	sudo rm $(supervisor_confd)/daphne-$(domain).conf

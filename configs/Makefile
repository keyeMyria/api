# -*- Makefile -*-

S = /tmp/conf.json
supervisor_confd = /etc/supervisor/conf.d
# supervisor_confd = .
output = tmp

domain = `./config.py -p domain secret-example.json secret.json`

templates:
	mkdir -p $(output)
	./config.py secret-example.json secret.json
	mustache $(S) daphne.conf.mustache > $(output)/daphne.conf
	mustache $(S) worker.conf.mustache > $(output)/worker.conf
	mustache $(S) settings.py.mustache > ../src/pashinin/settings.py
	mustache $(S) nginx.conf.mustache > $(output)/nginx.conf
	mustache $(S) phpfpm_params.mustache > $(output)/phpfpm_params
	mustache $(S) nginx-site.conf.mustache > $(output)/$(domain).conf
	mustache $(S) dbinit.sql.template > $(output)/dbinit.sql

ln_nginx:
	sudo ln -sf `realpath $(output)/$(domain).conf` /etc/nginx/sites-enabled/$(domain).conf

ln_nginxmain:
	sudo ln -sf `realpath $(output)/nginx.conf` /etc/nginx/nginx.conf

links: ln_nginx ln_nginxmain
	sudo ln -sf `realpath $(output)/daphne.conf` $(supervisor_confd)/daphne-$(domain).conf
	sudo ln -sf `realpath $(output)/worker.conf` $(supervisor_confd)/worker-$(domain).conf
	sudo ln -sf `realpath $(output)/phpfpm_params` /etc/nginx/phpfpm_params

removelinks:
	sudo rm /etc/nginx/sites-enabled/$(domain).conf
	sudo rm $(supervisor_confd)/daphne-$(domain).conf

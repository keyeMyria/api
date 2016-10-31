# -*- Makefile -*-

S = /tmp/conf.json
supervisor_confd = /etc/supervisor/conf.d
# supervisor_confd = .
output = tmp

templates:
	mkdir -p $(output)
	./config.py secret-example.json
	mustache $(S) daphne.conf.mustache > $(output)/daphne.conf
	mustache $(S) worker.conf.mustache > $(output)/worker.conf
	mustache $(S) settings.py.mustache > ../src/pashinin/settings.py
	mustache $(S) nginx.conf.mustache > $(output)/nginx.conf
	mustache $(S) phpfpm_params.mustache > $(output)/phpfpm_params
	mustache $(S) nginx-site.conf.mustache > $(output)/pashinin.com.conf
	mustache $(S) dbinit.sql.template > $(output)/dbinit.sql


links:
	sudo ln -sf `realpath $(output)/pashinin.com.conf` /etc/nginx/sites-enabled/pashinin.com.conf
	sudo ln -sf `realpath $(output)/nginx.conf` /etc/nginx/nginx.conf
	sudo ln -sf `realpath $(output)/daphne.conf` $(supervisor_confd)/daphne.conf
	sudo ln -sf `realpath $(output)/worker.conf` $(supervisor_confd)/worker.conf
	sudo ln -sf `realpath $(output)/phpfpm_params` /etc/nginx/phpfpm_params

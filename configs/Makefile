# -*- Makefile -*-

S = secret-example.json
supervisor_confd = /etc/supervisor/conf.d
# supervisor_confd = .
output = tmp

templates:
	mkdir $(output)
	mustache $(S) daphne.conf.mustache > $(output)/daphne.conf
	mustache $(S) settings.py.mustache > ../src/pashinin/settings.py
	mustache $(S) nginx.conf.mustache > $(output)/nginx.conf
	mustache $(S) nginx-site.conf.mustache > $(output)/pashinin.com.conf

links:
	sudo ln -sf `realpath $(output)/pashinin.com.conf` /etc/nginx/sites-enabled/pashinin.com.conf
	sudo ln -sf `realpath $(output)/nginx.conf` /etc/nginx/nginx.conf
	sudo ln -sf `realpath $(output)/daphne.conf` $(supervisor_confd)/daphne.conf

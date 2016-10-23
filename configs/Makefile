# -*- Makefile -*-

S = secret-example.json
supervisor_confd = /etc/supervisor/conf.d
# supervisor_confd = .
output = tmp

templates:
	mkdir $(output)
	sudo sh -c 'mustache $(S) daphne.conf.mustache > $(output)/daphne.conf'
	sudo sh -c 'mustache $(S) settings.py.mustache > ../src/pashinin/settings.py'
	sudo sh -c 'mustache $(S) nginx-site.conf.mustache > $(output)/nginx-site.conf'

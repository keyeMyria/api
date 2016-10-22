# -*- Makefile -*-

S = secret-example.json
supervisor_confd = /etc/supervisor/conf.d
# supervisor_confd = .

templates:
	sudo sh -c 'mustache $(S) daphne.conf > $(supervisor_confd)/daphne.conf'
	sudo sh -c 'mustache $(S) settings.py > ../src/pashinin/settings.py'
	# sudo chown www-data:www-data $(settings_file)

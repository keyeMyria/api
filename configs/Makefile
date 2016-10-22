# -*- Makefile -*-

S = secret-example.json
supervisor_confd = /etc/supervisor/conf.d
# supervisor_confd = .

templates:
	mustache $(S) daphne.conf.template > $(supervisor_confd)/daphne.conf
	# sudo chown www-data:www-data $(settings_file)

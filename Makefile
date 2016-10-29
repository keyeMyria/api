.PHONY: docker configs

d = `pwd`

# docker run -ti -v `pwd`:/var/www/pashinin.com pashinin.com
#docker run -p 80:80 -d -v `pwd`:/var/www/pashinin.com pashinin.com
docker: configs
	(cd docker; docker-compose up)


configs:
	(cd configs; make templates)

vm:
	(cd docker; make vm)

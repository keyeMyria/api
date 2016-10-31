.PHONY: docker configs

d = `pwd`

# docker run -ti -v `pwd`:/var/www/pashinin.com pashinin.com
#docker run -p 80:80 -d -v `pwd`:/var/www/pashinin.com pashinin.com
docker: configs
	(cd docker; docker-compose up -d redis db)
	sleep 4
	(cd docker; docker-compose up dbinit)
	sleep 2
	(cd docker; docker-compose up migration)
	(cd docker; docker-compose up web)
	# (cd docker; docker-compose up -d db redis)
# docker-compose up --force-recreate
# --no-deps db redis

configs:
	(cd configs; make templates)

vm:
	(cd docker; make vm)

psql:
	docker exec -it --user postgres docker_db_1 psql
# -ti --name docker_db_1 postgres psql

recreatedb: stop
	# sudo find -type d -name migrations -exec rm -rf {} \;
	(cd docker; docker rm docker_db_1)
	make docker


stop:
	docker stop docker_db_1
	docker stop docker_redis_1

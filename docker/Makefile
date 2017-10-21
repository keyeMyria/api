vm:
	docker build -t docker_web .

# docker build --build-arg user=`whoami` Dockerfile


rebuild-main:
	docker build -t pashinin.com -f Dockerfile .

rebuild-vnu:
	docker build -t vnu -f Dockerfile-vnu .

rebuild-db:
	docker build -t db -f Dockerfile-postgres .

rebuild-gulp:
	docker build -t gulp -f Dockerfile-gulp .

# Run "docker login" first
push-main:
	docker tag pashinin.com pashinin/pashinin.com
	docker push pashinin/pashinin.com

push-gulp:
	docker tag gulp pashinin/gulp
	docker push pashinin/gulp

push-vnu:
	docker tag vnu pashinin/vnu
	docker push pashinin/vnu

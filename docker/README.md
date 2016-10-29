https://hub.docker.com

```bash
# Configure Docker to start on boot
sudo systemctl enable docker

# show all containers on the system
docker ps -a

docker images
```




# Docker help

Container vs image. Container is a running image.

## Create your own image

```bash
touch Dockerfile
```

```
FROM docker/ubuntu:latest
RUN apt-get -y update && apt-get install -y redis-server
CMD echo "asd"
```

Then `Dockerfile` is used to build an image:

```
docker build -t pashinin.com .
```

`pashinin.com` is a name. `.` is a directory (current dir) with a Dockerfile.

After `build` finishes you can see your image in `docker images`.

```
REPOSITORY              TAG                 IMAGE ID
pashinin.com            latest              7a09c1c661c4
```

Tag image before pushing:

```
docker tag 7a09c1c661c4 <yourlogin>/pashinin.com:latest
```


Last thing to do is to login to docker hub and push an image there.

```bash
docker login

docker push pashinin/pashinin.com
```

Your authentication credentials will be stored in the .dockercfg authentication file in your home directory.

## docker-compose

For managing multiple containers.

Install:

```bash
curl -L "https://github.com/docker/compose/releases/download/1.8.1/docker-compose-$(uname -s)-$(uname -m)" > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

docker-compose --version
# docker-compose version: 1.8.1
```

Create docker-compose.yml:

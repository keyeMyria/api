import os
import shutil
import subprocess
from ..tasks import generate_settings

# Install Docker
if shutil.which("docker-compose") is None:
    print('Installing Docker...')
    raise
docker_compose = shutil.which("docker-compose")

# Install Yarn
if shutil.which("yarn") is None:
    print('Installing Yarn...')
    p = subprocess.Popen([
        'choco',
        'install',
        '-y',
        'yarn',
    ])
    p.wait()
    if shutil.which("yarn") is None:
        raise
yarn = shutil.which("yarn")

# yarn install
try:
    subprocess.Popen([yarn, 'install']).wait()
except Exception as e:
    print(e)


#
try:
    subprocess.Popen([shutil.which("pip"), 'install', 'celery']).wait()
except Exception as e:
    print(e)

# generate conf file
try:
    subprocess.Popen(
        [
            'python', 'config.py',
            'secret-example.json', 'secret.json'
        ],
        cwd='configs'
    ).wait()
except Exception as e:
    print(e)


# python3 -c 'from core.tasks import generate_settings;generate_settings()'
# subprocess.Popen([docker_compose, '-f',
# 'docker/docker-compose.yml', 'pull']).wait()

# os.execute("docker-compose -f docker/docker-compose.yml
# run --rm --workdir=/var/www/project/configs django make templates")
# os.execute("docker-compose -f docker/docker-compose.yml up")
# p = subprocess.Popen([docker_compose, '-f',
# 'docker/docker-compose.yml', 'up']).wait()

if __name__ == '__main__':
    print('Generating settings.py...', end='')
    try:
        # os.chdir('src')
        print(os.getcwd())
        generate_settings()
        # p = subprocess.Popen(
        #     ['python', '-c', "'from core.tasks import
        # generate_settings;generate_settings()'"],
        #     cwd='src',
        #     stdout=subprocess.PIPE, stderr=subprocess.PIPE
        # )
        # p.wait()
        # res = p.communicate()  # получить tuple('stdout', 'stderr')
        # if p.returncode:
        #     print(res[1])
        # print('result:', res[0])
        print('OK')
    except Exception as e:
        print('FAIL')
        print(e)

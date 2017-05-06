-- https://nodejs.org/dist/v7.10.0/node-v7.10.0-x64.msi

--os.execute("notepad.exe")
--os.execute("docker container ls")

--(cd configs; make templates)
os.execute("docker-compose -f docker/docker-compose.yml run --rm --workdir=/var/www/project/configs django make templates")
os.execute("docker-compose -f docker/docker-compose.yml up")


print("OK.DONE.")
print("")
print("Now go to http://example.org")
a = io.read("*n")

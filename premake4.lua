-- https://nodejs.org/dist/v7.10.0/node-v7.10.0-x64.msi

e = os.execute("python -V")
if e == 0 then
  print("Python already installed. OK")
else
  print("Installing Python...")
end

e = os.execute("python -m src.core.win.setup")
--os.execute("docker-compose -f docker/docker-compose.yml run --rm --workdir=/var/www/project/configs django make templates")
--os.execute("docker-compose -f docker/docker-compose.yml up")


print("OK.DONE.")
print("")
print("Now go to http://example.org")
a = io.read("*n")

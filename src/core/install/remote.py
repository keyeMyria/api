import os
import paramiko
from os.path import expanduser


def create_connection(host):
    home = expanduser("~")
    k = paramiko.RSAKey.from_private_key_file(os.path.join(
        home,
        '.ssh',
        'id_rsa'
    ))
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(hostname=host, username="root", pkey=k)
    return c


def add_user_to_group(user, group, host=None, c=None):
    if c is None:
        c = create_connection(host)

    raise NotImplementedError('implement add user to group')


def get_output(cmd, host=None, c=None):
    if c is None:
        c = create_connection(host)
    stdin, stdout, stderr = c.exec_command(cmd)
    return {
        'out': stdout.read().decode('utf-8').strip(),
        'err': stderr.read().decode('utf-8').strip(),
        'code': stdout.channel.recv_exit_status(),
    }


def file_exists(filename, host, c=None):
    # locally = host in (None, 'localhost', '127.0.0.1')
    # if locally:
    #     return os.path.isfile(filename)
    # else:
    if c is None:
        c = create_connection(host)

    stdin, stdout, stderr = c.exec_command(
        f"test -f {filename}"
    )
    return stdout.channel.recv_exit_status() == 0


def isdir(directory, host, c=None):
    # locally = host in (None, 'localhost', '127.0.0.1')
    # if locally:
    #     return os.path.isfile(filename)
    # else:
    if c is None:
        c = create_connection(host)

    stdin, stdout, stderr = c.exec_command(
        f"test -d {directory}"
    )
    return stdout.channel.recv_exit_status() == 0


def download(url, host, c=None):
    """Downloads {url} and puts it in /tmp/ on {host}"""
    basename = os.path.basename(url)
    filename = os.path.join('/tmp', basename)
    if c is None:
        c = create_connection(host)

    # cmd = f"wget -P /tmp -O {basename} {url}"
    cmd = f"wget -O {filename} {url}"
    print(f'{host}: {cmd}')
    stdin, stdout, stderr = c.exec_command(
        cmd
    )

    if stdout.channel.recv_exit_status() != 0:
        print('Error downloading a file on {host}')
        raise ValueError(stderr.read())

    return filename

    #     f = '/tmp/es.deb'
    #     if not os.path.isfile(f):
    #         urllib.request.urlretrieve(url, f)
    #     else:
    #         file_size = os.path.getsize(f)
    #         print(f'{f} exists ({file_size})')
    #         # TODO: install deb file

    #         # cache = apt.Cache()
    #         # if cache['package-name'].is_installed:
    #         if apt.installed('elasticsearch'):
    #             print("YES it's installed")
    #         else:
    #             print("NO it's NOT installed")
    #             apt.install(f)


def extract_zip(filename, dest, host, c=None):
    return get_output(
        f'unzip {filename} -d {dest}',
        host=host,
        c=c
    )


def untar(filename, host, c=None):
    """tar -xvzf community_images.tar.gz"""
    return get_output(
        f'tar -xvzf {filename}',
        host=host,
        c=c
    )


def mkdirs(d, host, c=None, **kwargs):
    r = get_output(
        f'mkdir -p {d}',
        host=host,
        c=c
    )
    if 'owner' in kwargs:
        get_output(
            f'chown postgres {d}',
            host=host,
            c=c
        )
    return r


def write(filename, contents, host, c=None):
    """Write contents (str) to filename (str) on a remote host (str)."""
    ftp = c.open_sftp()
    file = ftp.file(filename, "w")
    file.write(contents)
    file.flush()
    ftp.close()

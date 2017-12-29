import os
import subprocess
# import paramiko
from . import remote
import logging
log = logging.getLogger(__name__)


def sh(cmd):
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = p.communicate()
    return {
        'err': err,
        'out': out,
        'code': p.returncode,
    }


def get_deb_pkg_name(filename, host=None, c=None):
    if host:
        if c is None:
            c = remote.create_connection(host)
        stdin, stdout, stderr = c.exec_command(
            f"dpkg --info {filename} | grep Package: | sed 's/^.*: //'"
        )
        return stdout.read().decode('utf-8').strip()
    else:
        from deb_pkg_tools.package import inspect_package_fields
        meta_info = inspect_package_fields(filename)
        pkg_name = meta_info.get('Package')
        return pkg_name


def installed(pkg, host=None):
    """Return True if pkg is installed.

    "dpkg -s <pkg>" returns 0 if package is installed >0 otherwise.

    """
    if host is None:
        return sh(["dpkg", "-s", pkg])['code'] == 0
    else:
        res = remote.get_output(
            f"apt-cache search --names-only '^{pkg}$'",
            host=host
        )
        # stdin, stdout, stderr = c.exec_command(f"dpkg -s {pkg}")
        # out = stdout.read()
        # err = stderr.read()
        # print(out.decode('utf-8'))
        # print(err.decode('utf-8'))
        # raise NotImplementedError(stdout.read())
        res = remote.get_output(
            f"dpkg -s {pkg}",
            host=host
        )
        if "Status: deinstall" in res['out']:
            return False
        if 'is not installed' in res['err']:
            return False
        return True


def pkg_in_repos(pkg, host=None, c=None):
    if host:
        if c is None:
            c = remote.create_connection(host)
        res = remote.get_output(
            f"apt-cache search --names-only '^{pkg}$'",
            host=host,
            c=c
        )
        return res['out'] != ''
    else:
        p = subprocess.Popen(
            ["apt-cache", "search", "--names-only", f'^{pkg}$'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, err = p.communicate()
        return out.decode('utf-8') != ''


def install(pkg, interactive=False, host=None, c=None):
    """Install pkg package.

    pkg can be:

    1. package name (like "vim", "emacs")
    2. file name (like "/tmp/pkg.deb")

    """
    if host is None:
        print(f'APT: Installing {pkg} locally...')
        if os.path.isfile(pkg):
            # get info from .deb file
            pkg_name = get_deb_pkg_name(pkg, host, c=c)
            # print(repr())
            if installed(pkg_name, host=host):
                print(f'{pkg_name} is already installed')
                return

            p = subprocess.Popen(
                ["sudo", "dpkg", "-i", pkg] if interactive else
                ["sudo", "-n", "dpkg", "-i", pkg],
                # ["dpkg", "-i", pkg],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            out, err = p.communicate()
            if b'requires superuser privilege' in err:  # without sudo
                print(out, err)
            elif b'password is required' in err:
                if c is None:
                    c = remote.create_connection(host)
                stdin, stdout, stderr = c.exec_command(
                    # "ls"
                    f"sudo -n dpkg -i {pkg}"
                )
                print(stdout.read().decode('utf-8'))

        else:
            raise NotImplementedError(
                f"How to install a package {pkg}? No such file")
            # code = p.returncode
    else:
        print(f'{host}: Installing {pkg}...')
        if c is None:
            c = remote.create_connection(host)

        if remote.file_exists(pkg, host, c):
            pkg_name = get_deb_pkg_name(pkg, host, c=c)
            if installed(pkg_name, host):
                print(f'{host}: {pkg_name} is already installed')
            else:
                stdin, stdout, stderr = c.exec_command(
                    f"sudo -n dpkg -i {pkg}"
                )
                print(stdout.read().decode('utf-8'))
        else:
            if not pkg_in_repos(pkg, host=host, c=c):
                # apt update
                print(f'{host}: apt update...')
                res = remote.get_output(
                    "apt update",
                    host=host,
                    c=c
                )
            if not pkg_in_repos(pkg, host=host, c=c):
                raise ValueError(
                    f'Updated repos but still no "{pkg}"')

            res = remote.get_output(
                f"apt-get -y install {pkg}",
                host=host,
                c=c
            )

            e = 'dpkg was interrupted, you must manually run'
            if e in res['err']:
                # dpkg --configure -a
                raise NotImplementedError(
                    f"Need reconfigure dpkg on {host}")
            # raise NotImplementedError(
            #     f"How to install a package {pkg}?")
    return


def install_from_url(url, host=None, c=None):
    basename = os.path.basename(url)
    filename = os.path.join('/tmp', basename)
    if host:  # download url on "host"
        if c is None:
            c = remote.create_connection(host)

        if remote.file_exists(filename, host, c=c):
            print(f'{filename} exists on {host}')
        else:
            print(f'Going to download {basename} on {host}...')
            filename = remote.download(url, host, c=c)

        install(filename, host=host, c=c)
        # print(stdout.read())

    pass
    # if installed('elasticsearch', host=host):
    #     if host:
    #         print(f'APT: ElasticSearch is already installed on {host}.')
    #     else:
    #         print(f'ElasticSearch is already installed on this machine.')
    # elif not tty or confirm(f'Install ElasticSearch on {host}?'):


def ppa(name, host=None, c=None):
    # ppa:webupd8team/java
    # sudo add-apt-repository -y ppa:webupd8team/java
    if host:
        if c is None:
            c = remote.create_connection(host)

        res = remote.get_output(
            f'grep -q "^deb .*{name}" '
            '/etc/apt/sources.list /etc/apt/sources.list.d/*',
            host=host,
            c=c
        )
        ppa_already_added = res['code'] == 0
        if ppa_already_added:
            print(f'{host}: ppa:{name} already added')
            return

        res = remote.get_output(
            f'sudo add-apt-repository -y ppa:{name}',
            host=host,
            c=c
        )
        # print(out)
        # print(err)
    else:
        pass

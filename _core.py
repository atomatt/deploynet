import os
import os.path
import subprocess


def makedirs(path):
    if os.path.exists(path):
        return
    os.makedirs(path)


def shell(command):
    p = subprocess.Popen(command, shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return {'returncode': p.returncode, 'stdout': stdout,
            'stderr': stderr}


def sudo(command, password=None):
    if password:
        sudo = 'sudo -k -S -p "" '
        stdin = subprocess.PIPE
    else:
        sudo = 'sudo '
        stdin = None
    p = subprocess.Popen(sudo + command, shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         stdin=stdin)
    stdout, stderr = p.communicate(password)
    return {'returncode': p.returncode, 'stdout': stdout,
            'stderr': stderr}


if __name__ == '__channelexec__':
    import sys
    m = sys.modules['__deploynet__']
    m['cd'] = os.chdir
    m['shell'] = shell
    m['sudo'] = sudo
    m['fs.makedirs'] = makedirs
    channel.send(dir(m))

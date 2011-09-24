import os
import os.path


def install(path):
    if os.path.exists(path):
        return
    os.system('wget -q -O - http://bitbucket.org/ianb/virtualenv/raw/8dd7663d9811/virtualenv.py | python - --distribute %s' % path)


if __name__ == '__channelexec__':
    import sys
    m = sys.modules['__deploynet__']
    m['venv.install'] = install
    channel.send(dir(m))

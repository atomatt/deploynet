import os
import os.path


def install(path):
    if os.path.exists(path):
        return
    os.system('wget --quiet --no-check-certificate -O - https://github.com/pypa/virtualenv/raw/master/virtualenv.py | python - --distribute %s' % path)


if __name__ == '__channelexec__':
    import sys
    m = sys.modules['__deploynet__']
    m['venv.install'] = install
    channel.send(dir(m))

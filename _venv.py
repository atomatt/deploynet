import os
import os.path


def install(path):
    if os.path.exists(path):
        return
    os.system('wget --quiet --no-check-certificate -O - https://github.com/pypa/virtualenv/raw/master/virtualenv.py | python - --distribute %s' % path)


__exports__ = {
    "venv.install": install
}

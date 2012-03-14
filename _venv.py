import os
import os.path
import sys


VIRTUALENV_URL = "https://github.com/pypa/virtualenv/raw/master/virtualenv.py"


def install(path):
    if os.path.exists(path):
        return
    cmd = ["wget --quiet --no-check-certificate -O -", VIRTUALENV_URL, "|",
           sys.executable, "- --distribute", path]
    os.system(" ".join(cmd))


__exports__ = {
    "venv.install": install
}

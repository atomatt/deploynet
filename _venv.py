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


def install_requirements(venv, requirements_txt):
    cmd = ["./", venv, "/bin/pip install -r ", requirements_txt]
    return os.system("".join(cmd))


__exports__ = {
    "venv.install": install,
    "venv.install_requirements": install_requirements,
}

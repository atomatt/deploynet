import execnet


class Gateway(object):

    def __init__(self, spec=None):
        self._gw = execnet.makegateway(spec)
        self._gw.remote_exec(_remote_init).waitclose()
        self._ch = None

    def close(self):
        """
        Close the gateway.
        """
        self._gw.exit()

    def require(self, modulename):
        """
        Install source module in remote Python process.
        """
        with open(modulename+".py") as f:
            module = f.read()
        ch = self._gw.remote_exec(_require, modulename=modulename,
                                  module=module)
        ch.receive()
        ch.waitclose()

    def remote(self, name, *args, **kwargs):
        """
        Execute a named remote function.
        """
        self._open()
        self._ch.send({'name': name, 'args': args, 'kwargs': kwargs})
        return self._ch.receive()

    def rsync(self, sourcedir, destdir):
        """
        Copy directory to gateway's file system.
        """
        rsync = execnet.RSync(sourcedir)
        rsync.add_target(self._gw, destdir)
        rsync.send()

    def _open(self):
        """
        Ensure gateway is open and initialised and that the remote
        command loop is running.
        """
        if self._ch:
            return
        self.require("_core")
        self._ch = self._gw.remote_exec(_remote_command_loop)


def _require(channel, modulename, module):

    import sys

    # Compile the module.
    l = {}
    code = compile(module, modulename, "exec")
    eval(code, l)

    # Merge the module's exports into the magic module.
    m = sys.modules.setdefault('__deploynet__', {})
    m.update(l["__exports__"])
    channel.send(0)


def _remote_init(channel):
    """
    Initialise the dummy __deploynet__ module in the remote Python
    process.
    """
    import sys
    sys.modules.setdefault('__deploynet__', {})


def _remote_command_loop(channel):
    """
    Run a command loop in the remote process.
    """
    import sys
    m = sys.modules['__deploynet__']
    for item in channel:
        func = m[item['name']]
        args = item.get('args')
        kwargs = item.get('kwargs')
        channel.send(func(*args, **kwargs))


if __name__ == '__main__':

    import sys

    gw = Gateway(sys.argv[1])
    gw.require("_venv")
    gw.remote("venv.install", "vpy")
    gw.close()

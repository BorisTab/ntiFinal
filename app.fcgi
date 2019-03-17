#!/usr/bin/env python
from os import name
from os import getcwd

from autoapp import app

from pathlib import Path
from flup.server.fcgi import WSGIServer
from werkzeug.contrib.fixers import LighttpdCGIRootFix


class ScriptNameStripper(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ['SCRIPT_NAME'] = ''
        return self.app(environ, start_response)


app.debug = True
app.threaded = True
app = ScriptNameStripper(app)


if __name__ == '__main__':
    try:
        if name == 'nt':
            activate_this = Path(getcwd() + '/venv/bin/activate_this.py').as_posix()
            execfile(activate_this, dict(__file__=activate_this))
        else:
            activate_this = Path(getcwd() + '/venv/Scripts/activate_this.py').as_posix()
            execfile(activate_this, dict(__file__=activate_this))
    except NameError as e:
        print('Start failed')

    print('Starting up')
    WSGIServer(LighttpdCGIRootFix(app)).run()

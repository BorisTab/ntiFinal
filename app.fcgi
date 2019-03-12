#!/usr/bin/env python
import sys
import logging

from autoapp import app
from flup.server.fcgi import WSGIServer
from werkzeug.contrib.fixers import LighttpdCGIRootFix


class ScriptNameStripper(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ['SCRIPT_NAME'] = ''
        return self.app(environ, start_response)


app.debug = True
app = ScriptNameStripper(app)


if __name__ == '__main__':
    activate_this = '/var/apps/xnoobs/venv/bin/activate_this.py'
    execfile(activate_this, dict(__file__=activate_this))

    print('Starting up')
    WSGIServer(LighttpdCGIRootFix(app)).run()

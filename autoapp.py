from app import run

from base64 import b64encode
from flask.helpers import get_debug_flag

from settings import DevConfig
from settings import ProductionConfig


CONFIG = DevConfig if get_debug_flag() else ProductionConfig

app = run.create_app(CONFIG)
app.jinja_env.filters['b64d'] = lambda u: b64encode(u).decode()

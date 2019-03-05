from flask.helpers import get_debug_flag

from app import run

from settings import DevConfig
from settings import ProductionConfig


CONFIG = DevConfig if get_debug_flag() else ProductionConfig

app = run.create_app(CONFIG)

from flask.helpers import get_debug_flag

from app.app import create_app

from settings import DevConfig
from settings import ProductionConfig


CONFIG = DevConfig if get_debug_flag() else ProductionConfig

site = create_app(CONFIG)

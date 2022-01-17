from typing import Callable

from flask import Flask, Blueprint

from . import commands
from . import views
from .config import config
from .db import db, migrate
from .login_manager import login_manager
from .utils import register_utilities_to_app


def create_app(config_name: str = 'default') -> Flask:
    app = Flask(__name__)
    app.config.from_object(config.get(config_name) or config.get('default'))
    data_to_registered = [
        (app.register_blueprint, views, Blueprint),
        (app.cli.add_command, commands, Callable)
    ]

    for values in data_to_registered:
        register_utilities_to_app(*values)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    return app

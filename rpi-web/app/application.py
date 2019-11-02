import logging
import os

from flask import Flask
from werkzeug.utils import import_string
from . import config, db, io

logger = logging.getLogger(__name__)

app = Flask(__name__, static_url_path='')


def create_app(environment):

    config_map = {
        'development': config.Development(),
        'testing': config.Testing(),
        'production': config.Production(),
    }

    config_obj = config_map[environment.lower()]

    app.config.from_object(config_obj)
    app.url_map.strict_slashes = False
    app.add_url_rule('/', 'home', home)

    register_blueprints(app)

    db.init_app(app)
    io.init_app(app)

    return app


def home():
    return app.send_static_file('index.html')


def register_blueprints(app):
    root_folder = 'app'

    for dir_name in os.listdir(root_folder):
        module_name = root_folder + '.' + dir_name + '.views'
        module_path = os.path.join(root_folder, dir_name, 'views.py')

        if os.path.exists(module_path):
            module = import_string(module_name)
            obj = getattr(module, 'app', None)
            if obj:
                app.register_blueprint(obj)

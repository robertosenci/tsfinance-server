# -*- encoding: utf-8 -*-

# Python modules
import os
from importlib import import_module

# Flask modules
from flask import Flask
from flask_sockets import Sockets
from flask_apscheduler import APScheduler

# funcoes do projeto
from .utils import get_ip, get_name

# App modules
scheduler = APScheduler()
sockets = Sockets()

basedir = os.path.abspath(os.path.dirname(__file__))
app_src = basedir.split('\\')[-1]


def register_extensions(app):
    sockets.init_app(app)

    app.config['BLUEPRINTS'] = []
    app.config['CONNECTIONS'] = {}
    app.config['NICK_NAMES'] = {}


def register_blueprints(app):
    def find_modules():
        for item in os.listdir(basedir):
            if os.path.isdir(os.path.join(os.path.abspath(basedir), item)):
                file = os.path.join(os.path.abspath(basedir), item, 'routes.py')
                try:
                    isFile = os.path.isfile(file)
                except Exception as e:
                    isFile = False

                if isFile:
                    yield item

    for i, module_name in enumerate(find_modules()):
        try:
            module = import_module('{}.{}.routes'.format(app_src, module_name))
            app.config['BLUEPRINTS'].append({"name": module.blueprint.name, "url_prefix": module.blueprint.url_prefix})
            app.register_blueprint(module.blueprint)
        except Exception as e:
            print(e)
            ...


def configure_scheduler(app):
    scheduler.init_app(app)
    with app.app_context():
        scheduler.start()


def create_app():
    app = Flask(__name__)

    app.config['APPNAME'] = 'TSFINANCE'
    app.config['COMPUTER_NAME'] = get_name()
    app.config['COMPUTER_IP'] = get_ip()

    app_name = app.config['APPNAME'].upper()

    ambient = 'DevelopmentConfig' if os.environ.get(f'{app_name}_PRODUCTION') is None else 'ProductionConfig'
    app.config.from_object("{}.configuration.{}".format(app_src, ambient))

    register_extensions(app)
    configure_scheduler(app)

    with app.app_context():
        register_blueprints(app)

        # se tiver autenticacao o redirecionamento inicial
        # @app.route('/', methods=['GET'])
        # def index():
        #     return redirect(url_for(f'{app_name}_auth.login'))

        return app

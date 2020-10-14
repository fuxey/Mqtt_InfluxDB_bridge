from flask import Flask
from importlib import import_module


def register_blueprints(app):
    module = import_module(str('app.base.routes'))
    app.register_blueprint(module.blueprint)


def create_app(config, mqttInfluxDBBridge):
    app = Flask(__name__, static_folder='base/static')
    app.config['MQTTINFLUXDBBRIDGE'] = mqttInfluxDBBridge
    app.config.from_object(config)
    register_blueprints(app)
    return app

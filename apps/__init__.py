from flask import Flask

from apps.config import DeveloperConfig, ProductConfig, environment
from apps.urls import init_api

"""
app.config[]

"""


def create_app(env_name):
    app = Flask(__name__)
    app.config.from_object(environment.get(env_name))
    init_api(app)
    return app

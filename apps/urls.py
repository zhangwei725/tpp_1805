from flask_restful import Api

api = Api()


def init_api(app):
    api.init_app(app)




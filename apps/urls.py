from flask_restful import Api

from apps.main.apis import IndexResource

api = Api()


def init_api(app):
    api.init_app(app)


api.add_resource(IndexResource, '/')

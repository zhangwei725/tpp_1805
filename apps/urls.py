from flask_restful import Api

from apps.main.apis import IndexResource, HotRankingResource

# Resource注册
api = Api()


def init_api(app):
    api.init_app(app)


api.add_resource(IndexResource, '/')
api.add_resource(HotRankingResource, '/score/')

from flask_restful import Api

from apps.cinemas.apis import CinemasResource, CinemasDistrictResource
from apps.main.apis import IndexResource, HotRankingResource

# Resource注册
from apps.movie.apis import MoviesPageResource

api = Api()


def init_api(app):
    api.init_app(app)


api.add_resource(IndexResource, '/')
api.add_resource(HotRankingResource, '/score/')
api.add_resource(MoviesPageResource, '/movies/')
api.add_resource(CinemasResource, '/cinemas/')
api.add_resource(CinemasDistrictResource, '/cinemas/district/')

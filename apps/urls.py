from flask_restful import Api

from apps.cinemas.apis import CinemasResource, CinemasDistrictResource, UpdateResource, CinemaDetail
from apps.main.apis import IndexResource, HotRankingResource

# Resource注册
from apps.movie.apis import MoviesPageResource
from apps.order.apis import SeatOrderResource, OrderResource

api = Api()


def init_api(app):
    api.init_app(app)


api.add_resource(IndexResource, '/')
api.add_resource(HotRankingResource, '/score/')
api.add_resource(MoviesPageResource, '/movies/')
api.add_resource(CinemasResource, '/cinemas/')
# 影院区县的地址
api.add_resource(CinemasDistrictResource, '/cinemas/district/')
api.add_resource(UpdateResource, '/update/')
# 影院详情
api.add_resource(CinemaDetail, '/cinemas/detail/')
# 选座
api.add_resource(SeatOrderResource, '/seats/')
api.add_resource(OrderResource, '/order/')

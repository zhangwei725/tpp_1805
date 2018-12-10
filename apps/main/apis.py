from flask_restful import Resource, fields, marshal_with

from apps.main.models import Banner, Movie

"""

"""
banner_fields = {
    'bid': fields.Integer,
    'title': fields.String,
    'image': fields.String,
    'detail_url': fields.String,
}

movie_fields = {
    'id': fields.Integer,
    'show_name': fields.String,
    'show_name_en': fields.String,
    'director': fields.String,
    'leading_role': fields.String,
    'type': fields.String,
    'country': fields.String,
    'language': fields.String,
    'duration': fields.Integer,
    'screening_model': fields.String,
}

data_fields = {
    'banners': fields.List(fields.Nested(banner_fields)),
    'hot_movies': fields.List(fields.Nested(movie_fields)),
    'ready_movies': fields.List(fields.Nested(movie_fields)),
    'hot_count': fields.Integer,
    'ready_count': fields.Integer
}

result = {
    'status': fields.Integer(default=200),
    'msg': fields.String(default='success'),
    'data': fields.Nested(data_fields)
}


# limit  offset

class IndexResource(Resource):
    @marshal_with(result)
    def get(self):
        # 查询轮播的相关信息
        #
        # SELECT  *  FROM MOVIE LIMIT 0,5

        # SELECT  * FROM   LIMIT 10  OFFSET 1
        # (page-1)*size
        banners = Banner.query.filter(Banner.is_delete is False).order_by(Banner.order.desc()).all()
        movies = Movie.query.filter(Movie.flag == 1).order_by(Movie.open_day).limit(5).offset(0).all()

        return ''

from flask_restful import fields

# 分页数据
#  list
from apps.main.field import IndexFields

page_fields = {
    'pages': fields.Integer,
    'total': fields.Integer,
}

data_fields = {
    'pagination': fields.Nested(page_fields),
    'movies': fields.List(fields.Nested(IndexFields.movie_fields))
}


class MoviesFields:
    result_fields = {
        'status': fields.Integer,
        'msg': fields.String,
        'data': fields.Nested(data_fields)
    }

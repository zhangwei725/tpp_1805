from flask_restful import fields

from apps.main.field import IndexFields


class CinemasFields:
    cinemas_fields = {
        'cid': fields.Integer(),
        'name': fields.String(),
        'address': fields.String(),
        'phone': fields.String(),
        'score': fields.Float(),

    }

    result_fields = {
        'status': fields.Integer(default=200),
        'msg': fields.String(default='success'),
        'data': fields.List(fields.Nested(cinemas_fields))
    }


class AreaFields:
    district_fields = {
        'name': fields.String,
        'aid': fields.Integer
    }

    result_fields = {
        'status': fields.Integer(default=200),
        'msg': fields.String(default='success'),
        'data': fields.List(fields.Nested(district_fields))
    }


class CinemaDetailFields:
    hall_fields = {
        'hid': fields.Integer,
        'name': fields.String,
        'screen_type': fields.Integer,
        'seat_num': fields.Integer,
    }
    hs_fields = {
        'hsid': fields.Integer,
        'start': fields.DateTime(dt_format='iso8601'),
        'end': fields.DateTime(dt_format='iso8601'),
        'origin_price': fields.Float,
        'current_price': fields.Float,
        'hall': fields.Nested(hall_fields),
    }
    data_fields = {
        'cinema': fields.Nested(CinemasFields.cinemas_fields),
        'movies': fields.List(fields.Nested(IndexFields.movie_fields)),
        'movie': fields.Nested(IndexFields.movie_fields),
        'hs_list': fields.List(fields.Nested(hs_fields)),
    }

    result_fields = {
        'status': fields.Integer(default=200),
        'msg': fields.String(default='success'),
        'data': fields.Nested(data_fields)
    }

from flask_restful import fields


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

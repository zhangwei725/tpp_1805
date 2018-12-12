from flask_restful import Resource, reqparse

from apps.cinemas.helper import AreaFields, CinemasFields
from apps.cinemas.models import Cinema
from apps.main.models import Area
from apps.utils.resp_reslut import to_response_error, to_response_success


class CinemasResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('city', type=str, default='北京')
        self.parser.add_argument('district', type=str)

    """
    区域信息
    影院的信息
    """

    def get(self):
        try:
            args = self.parser.parse_args()
            city = args.get('city')
            district = args.get('district')
            query = Cinema.query.fliter(Cinema.city == city)
            if district:
                query = query.filter(Cinema.district == district)
            cinemas = query.all()
            return to_response_success(cinemas, fields=CinemasFields.result_fields)
        except:
            return to_response_error()


class CinemasDistrictResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('city', type=str, default='北京')

    def get(self):
        try:
            city = self.parser.parse_args().get('city')
            city = Area.query.filter(Area.short_name == city, Area.level == 2).first()
            districts = Area.query.filter(Area.parent_id == city.aid, Area.level == 3).all()
            return to_response_success(districts, fields=AreaFields.result_fields)
        except:
            return to_response_error()

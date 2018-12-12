from flask_restful import Resource, reqparse

from apps.cinemas.helper import AreaFields, CinemasFields
from apps.cinemas.models import Cinema, HallScheduling
from apps.ext import db
from apps.main.models import Area
from apps.utils.resp_reslut import to_response_error, to_response_success


class CinemasResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('city', type=str, default='北京')
        self.parser.add_argument('district', type=str)
        self.parser.add_argument('sort', type=int)
        self.parser.add_argument('keyword', type=str)

    """
    区域信息
    影院的信息
    """

    def get(self):
        try:
            args = self.parser.parse_args()
            city = args.get('city')
            # 获取区域信息
            district = args.get('district')
            sort = args.get('sort')
            query = Cinema.query.filter(Cinema.city == city)
            if district:
                # 如果有选中区域   where  city=1988 and district= 989
                query = query.filter(Cinema.district == district)
            #     1表示升序
            if sort == 1:
                # 降序
                query = query.order_by(Cinema.score.desc())
            elif sort == 2:
                # 表示升序
                query.order_by(Cinema.score.asc())
            cinemas = query.all()
            return to_response_success(cinemas, fields=CinemasFields.result_fields)
        except Exception as e:
            print(e)
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


"""
查看影院详情
影院表
电影表
排片表
影厅表


1>影院的信息
2>影院排片信息

必要参数影院id

多对多  必须有第三张表



"""


class CinemaDetail(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('cid', type=int, required=True)

    def get(self):
        cid = self.parser.parse_args().get('cid')
        # hs_list = HallScheduling.query.filter(HallScheduling.cinema_id == cid).all()
        # for hs in hs_list:
        #     print(hs.cinema.name)
        #     print(hs.movie.show_name)
        #     print(hs.cinema.hs_list)
        cinema = Cinema.query.get(cid)

        for hs in cinema.hs_list:
            print(hs.movie.show_name)
        return ''


class UpdateResource(Resource):
    def get(self):
        ares = Area.query.filter(Area.level == 3).all()
        for are in ares:
            Cinema.query.filter(Cinema.district == are.short_name).update({Cinema.district: str(are.aid)})
        db.session.commit()
        return ''

    #
    class HallSchedulingResource(Resource):
        def __init__(self):
            pass

        # 添加排片信息
        def post(self):
            pass

        # 修改排片信息
        def put(self):
            pass

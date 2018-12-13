# 通过排片的id查询座位的信息电影的信息
from flask_restful import Resource, reqparse, fields

# admin
from apps.cinemas.models import SeatScheduling, HallScheduling, Seats
from apps.order.helper import SeatOrderFields
from apps.order.model import Order, db
from apps.utils.helper import product_code
from apps.utils.resp_reslut import to_response_success, to_response_error


class SeatOrderResource(Resource):
    # 获取排片影片的座位信息
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('hs_id', type=int, required=True)

    def get(self):
        hs_id = self.parser.parse_args().get('hs_id')
        hs = HallScheduling.query.get(hs_id)
        seats = [ss.seat for ss in hs.ss_list]
        data = {'seats': seats, 'movie': hs.movie, 'hall': hs.hall, }
        return to_response_success(data=data, fields=SeatOrderFields.result_fields)

        #
        def post(self):
            # 生成订单
            pass

        # 更新座位排期
        def put(self):
            pass

        # 删除座位
        def put(self):
            pass


# 成功之后返回订单编号

result_fields = {
    'status': fields.Integer(default=200),
    'msg': fields.String(default='支付成功'),
    'data': fields.String,
}


class OrderResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('uid', type=int, )
        self.parser.add_argument('movie_id', type=int, )
        self.parser.add_argument('hs_id', type=int, )
        self.parser.add_argument('seat_ids', type=int, action='append')
        self.parser.add_argument('ss_id', type=int, default=1)

    def post(self):
        uid = self.parser.parse_args().get('uid')
        movie_id = self.parser.parse_args().get('movie_id')
        hs_id = self.parser.parse_args().get('hs_id')
        seat_ids = self.parser.parse_args().get('seat_ids')
        #       生成订单号
        try:
            # 查询选的座位是否可以购买
            seats = Seats.query.filter(Seats.sid.in_(seat_ids)).all()
            # 如果作为可选
            if is_choose(seats):
                #  修改座位不能在选
                for seat in seats:
                    seat.is_choose = False
                db.session.add_all(seats)
                # 订单号
                no = product_code()
                # 计算总金额
                hs = HallScheduling.query.get(hs_id)
                total = hs.current_price * 2
                # 生成订单
                order = Order(no=no,
                              number=2,
                              total=total,
                              status=1,
                              movie_id=movie_id,
                              hs_id=hs_id,
                              cinema_id=1,
                              seat_id=1,
                              ss_id=1
                              )
                # 保存订单
                db.session.add(order)
                db.session.commit()
                return to_response_success(data=no, fields=result_fields)
            else:
                return to_response_error(status=-1, msg='座位已被选,请重新选座')
        except Exception  as e:
            print(e)
            db.session.rollback()
            return ''


# 判断是否可以购买
def is_choose(seats):
    for seat in seats:
        if seat.is_choose:
            continue
        else:
            return False
    return True

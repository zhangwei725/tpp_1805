from flask_restful import Resource, fields, marshal_with
from sqlalchemy import func, desc, asc

from apps.main.field import RatingFields
from apps.main.models import Banner, Movie, Rating

# limit  offset
# 横向拆分 经常变化的数据尽量拆分
#  经常修改的字段会开事务
#  缓存
#  读写分离 主从赋值
#  主数据  -  增删改
from apps.utils.resp_reslut import to_response_success, to_response_error


class IndexResource(Resource):
    def get(self):
        result = {}
        try:
            # 查询轮播的相关信息
            banners = Banner.query.filter(Banner.is_delete is False).order_by(Banner.order.desc()).all()
            hot_movies = Movie.query.filter(Movie.flag == 1).order_by(Movie.open_day).limit(5).offset(0).all()
            ready_movies = Movie.query.filter(Movie.flag == 2).order_by(Movie.open_day).limit(5).offset(0).all()
            hot_count = Movie.query.filter(Movie.flag == 1).count()
            ready_count = Movie.query.filter(Movie.flag == 2).count()
            result.update(data={
                'banners': banners,
                'hot_movies': hot_movies,
                'ready_movies': ready_movies,
                'hot_count': hot_count,
                'ready_count': ready_count,
            })
        except Exception as e:
            result.update(status=404, msg='获取数据失败')
        return result


class HotRankingResource(Resource):
    def get(self):
        # SELECT  AVG(score) avg
        # from  rating
        # group by  movie_id
        # oder by  avg
        #    分组 统计
        try:
            # [()]
            ranking_moviess = Rating.query.with_entities(Rating.movie_id, func.avg(Rating.score).label('avg')) \
                .group_by(Rating.movie_id).order_by(desc('avg')).limit(5).all()
            data = []
            for rank in ranking_moviess:
                data.append({'score': rank[1]})
            return to_response_success(data=data, fields=RatingFields.result_fields)
        except Exception as e:
            return to_response_error()

# 给电影添加评分的接口

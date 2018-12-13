from flask_restful import Resource, fields, marshal_with
from sqlalchemy import func, desc, asc

from apps.ext import cache
from apps.main import field
from apps.main.field import RatingFields
from apps.main.models import Banner, Movie, Rating, Area

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
            data = {
                'banners': banners,
                'hot_movies': hot_movies,
                'ready_movies': ready_movies,
                'hot_count': hot_count,
                'ready_count': ready_count,
            }
            return to_response_success(data, fields=field.IndexFields.result_fields)
        except Exception as e:
            return to_response_error()


"""
# 分组查询  group_by
# 分组统计  func.max() func.count(),func.avg()   设置别名 label
# 排序    直接通过字段可以掉 desc()  涉及到统计函数,desc(别名)  
# 外连接   左外连接   右外连接  全连接
"""


class HotRankingResource(Resource):
    def get(self):
        # SELECT  AVG(score) avg
        # from  rating
        # group by  movie_id
        # oder by  avg
        #    分组 统计
        # 确定表
        #  rating 表    评分
        #  movie  表     电影id  电影图片  电影的名称
        # 确定关联字段
        # id = movie_id

        # SELECT  m.id ,m.show_name,m.image,round(avg(r.score)) avg
        # FROM movie m ,rating r
        # where m.id = r.movie_id
        # group by  r.movie.id
        # order by  avg  desc

        try:
            # [()]
            # 四舍五入round()
            # 截取 truncate
            # [()]
            ratings = Rating.query. \
                with_entities(Rating.movie_id,
                              func.round(func.avg(Rating.score).label('score'), 1)
                              , Movie.image, Movie.show_name) \
                .join(Movie, Movie.id == Rating.movie_id) \
                .group_by(Rating.movie_id) \
                .order_by(desc('score')) \
                .limit(5).offset(0).all()

            data = [{'movie_id': rating[0], 'score': rating[1],
                     'image': rating[2],
                     'show_name': rating[3],
                     } for rating in ratings]
            return to_response_success(data=data, fields=RatingFields.result_fields)
        except Exception as e:
            return to_response_error()


# 获取城市字母相关信息

class AreaResource(Resource):
    @cache(10 * 24 * 60)
    def get(self):
        firsts = Area.query.with_entities(Area.first).filter(Area.level == 2).group_by(Area.first).order_by(Area.first)
        ares = []
        for first in firsts:
            ares.append({first[0], Area.query.filter(Area.level == 2, Area.first == first[0]).all()})

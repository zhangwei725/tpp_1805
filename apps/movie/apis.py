from flask_restful import Resource, reqparse

from apps.main.models import Movie
from apps.movie.filed import MoviesFields
from apps.utils.resp_reslut import to_response_success


class MoviesPageResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('page', type=int, default=1)
        self.parser.add_argument('size', type=int, default=10)
        # 1 表示正在热映   2 表示即将上映
        self.parser.add_argument('flag', type=int, default=1)

    # 总页数  总条数
    def get(self):
        args = self.parser.parse_args()
        flag = 1 if args.get('flag') == 1 else 2
        pagination = Movie.query.filter(Movie.flag == flag).paginate(page=args.get('page'),
                                                                     error_out=False)
        data = {'movies': pagination.items, 'pagination': pagination}
        return to_response_success(data=data, fields=MoviesFields.result_fields)

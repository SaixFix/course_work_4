from flask import request
from flask_restx import Namespace, Resource

from project.container import movie_service
from project.setup.api.models import movie
from project.setup.api.parsers import page_parser

api = Namespace('movies')


@api.route('/')
class GenresView(Resource):
    @api.expect(page_parser)
    @api.marshal_with(movie, as_list=True, code=200, description='OK')
    def get(self):
        """
        Get all genres.
        """
        filter = request.args.get('status')

        if filter != None and (filter == 'new' or filter == 'old'):
            return movie_service.get_all(filter=filter, **page_parser.parse_args())
        else:
            return movie_service.get_all(**page_parser.parse_args())


@api.route("/<int:fid>")
class MovieView(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(movie, code=200, description='OK')
    def get(self, genre_id: int):
        """
        Get genre by id.
        """
        return movie_service.get_item(genre_id)



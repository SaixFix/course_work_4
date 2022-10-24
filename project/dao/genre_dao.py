from project.dao.base import BaseDAO
from project.dao.models.genre import Genre


class GenreDAO(BaseDAO[Genre]):
    __model__ = Genre

from project.dao.user_dao import UserDAO
from project.models import User
from project.exceptions import ItemNotFound
from typing import Optional
from project.tools.security import generate_password_hash, get_data_from_token, approve_refresh_token, generate_tokens


class UserService:

    def __init__(self, dao: UserDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> User:
        if user := self.dao.get_by_id(pk):
            return user
        raise ItemNotFound(f'User with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None) -> list[User]:
        return self.dao.get_all(page=page)

    def create_user(self, login, password):
        self.dao.create(login, password)

    def get_user_by_login(self, login):
        return self.dao.get_user_by_login(login)

    def check(self, login, password):
        user = self.get_user_by_login(login)
        return generate_tokens(email=user.email, password=password, password_hash=user.password)

    def update_token(self, refresh_token):
        return approve_refresh_token(refresh_token)

    def get_user_by_token(self, refresh_token):
        data = get_data_from_token(refresh_token)

        if data:
            return self.get_user_by_login(data.get('email'))

    def update_user(self, data: dict, refresh_token):
        user = self.get_user_by_token(refresh_token)
        if user:
            self.dao.update(login=user.email, data=data)

    def update_password(self, data, refresh_token):
        user = self.get_user_by_token(refresh_token)
        if user:
            check_pass = self.check(login=user.email, password=data.get('password'))
            if check_pass is not None:
                self.dao.update(login=user.email, data={'password': generate_password_hash(data.get('password_2'))})
                return self.check(login=user.email, password=data.get('password_2'))
            else:
                return "Логин или пароль не верный"


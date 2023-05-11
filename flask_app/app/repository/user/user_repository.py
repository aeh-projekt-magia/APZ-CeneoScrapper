from abc import ABC, abstractmethod
from typing import List

from app.models.UserModel import User
from app.repository.base_repository import BaseRepository


class UserRepository(BaseRepository, ABC):
    @abstractmethod
    def add_user(self, user):
        ...

    @abstractmethod
    def get_user_by_id(self, user_id) -> User:
        ...

    @abstractmethod
    def get_user_by_email(self, email_address) -> User:
        ...

    @abstractmethod
    def get_all_users(self) -> List[User]:
        ...

    @abstractmethod
    def delete_user_by_email_address(self, email_address):
        ...

    @abstractmethod
    def delete_user_by_id(self, user_id):
        ...

    @abstractmethod
    def delete_all_users(self):
        ...

    @abstractmethod
    def update_user(self, user):
        ...

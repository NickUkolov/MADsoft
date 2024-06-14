from abc import ABCMeta, abstractmethod

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_session


class AbstractCRUD(metaclass=ABCMeta):

    @abstractmethod
    def read_all(self, *args, **kwargs):
        ...

    @abstractmethod
    def read_one_by_id(self, *args, **kwargs):
        ...

    @abstractmethod
    def read_one_by_title(self, *args, **kwargs):
        ...

    @abstractmethod
    def create(self, *args, **kwargs):
        ...

    @abstractmethod
    def update(self, *args, **kwargs):
        ...

    @abstractmethod
    def delete(self, *args, **kwargs):
        ...


class CRUD(AbstractCRUD, metaclass=ABCMeta):

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

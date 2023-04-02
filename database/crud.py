from typing import Iterable

from database.core import get_session


class CRUD:

    _field = '_sa_instance_state'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def dict(self, *, include: Iterable = None, exclude: Iterable = None) -> dict:
        include = include or set(self.__dict__.keys())
        exclude = exclude or set()
        result = {}
        for k, v in self.__dict__.items():
            if k != self._field and k in include and k not in exclude:
                result[k] = v
        return result

    @classmethod
    def get_count(cls) -> int:
        session = get_session()
        return session.query(cls).count()

    @classmethod
    def get_autoincrement(cls) -> int:
        return cls.get_count() + 1

    @classmethod
    def get(cls, pk: int):
        session = get_session()
        return session.query(cls).filter_by(id=pk).first()

    @classmethod
    def get_many(cls, **kwargs):
        session = get_session()
        return session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def create(cls, **kwargs):
        session = get_session()
        pk = cls.get_autoincrement()
        instance = cls(id=pk, **kwargs)
        session.add(instance)
        session.commit()
        session.refresh(instance)
        return instance

    @classmethod
    def delete(cls, pk: int):
        instance = cls.get(pk)
        if instance:
            session = get_session()
            session.delete(instance)
            session.commit()

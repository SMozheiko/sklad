from typing import Iterable

from sqlalchemy import update, delete, func
from sqlalchemy.orm import Query

from database.core import session as sess


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
        session = sess.sess
        return session.query(cls).count()

    @classmethod
    def get_autoincrement(cls) -> int:
        session = sess.sess
        pk = session.query(func.max(cls.id)).scalar()
        return pk + 1 if pk else 1

    @classmethod
    def get(cls, pk: int):
        session = sess.sess
        return session.query(cls).filter_by(id=pk).first()

    @classmethod
    def in_(cls, field: str, values: list) -> list:
        session = sess.sess
        return session.query(cls).filter(getattr(cls, field).in_(values)).all()

    @classmethod
    def query(cls) -> Query:
        session = sess.sess
        return session.query(cls)

    @classmethod
    def get_many(cls, **kwargs):
        session = sess.sess
        return session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def create(cls, **kwargs):
        session = sess.sess
        pk = cls.get_autoincrement()
        instance = cls(id=pk, **kwargs)
        session.add(instance)
        session.commit()
        return instance

    @classmethod
    def delete(cls, params: dict):
        session = sess.sess
        query = delete(cls).filter_by(**params)
        session.execute(query)
        session.commit()

    @classmethod
    def update(cls, params: dict, **kwargs):
        session = sess.sess
        query = update(cls).filter_by(**params).values(**kwargs)
        session.execute(query)
        session.commit()

import datetime

from sqlalchemy import Column, String, Float, BigInteger, Enum, Engine, DateTime
from sqlalchemy.orm import declarative_base

from database.crud import CRUD
from utils import get_hashed_password


Base = declarative_base()


class Manager(Base, CRUD):
    __tablename__ = 'managers'
    id = Column(BigInteger, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    _created_at = Column(DateTime, name='created_at', nullable=False, default=datetime.datetime.now())

    @property
    def full_name(self):
        return f"{self.surname} {self.name}".title()

    @property
    def created_at(self) -> str:
        return self._created_at.strftime('%Y-%m-%d %H:%M')

    @classmethod
    def create(cls, **kwargs):
        kwargs['password'] = get_hashed_password(kwargs['password'])
        super().create(**kwargs)

def create_tables(engine: Engine):
    Base.metadata.create_all(bind=engine, checkfirst=True)
    count = Manager.get_count()
    if not count:
        Manager.create(
            **{
                'username': 'admin',
                'password': 'admin',
                'role': 'admin',
                'name': 'admin',
                'surname': 'god'
            }
        )

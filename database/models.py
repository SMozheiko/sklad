from sqlalchemy import Column, String, Float, BigInteger, Enum, Engine
from sqlalchemy.orm import declarative_base

from database.crud import CRUD


Base = declarative_base()


class Manager(Base, CRUD):
    __tablename__ = 'managers'
    id = Column(BigInteger, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    @property
    def full_name(self):
        return f"{self.surname} {self.name}".capitalize()


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

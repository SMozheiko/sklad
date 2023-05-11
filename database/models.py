import datetime

from sqlalchemy import Column, String, Float, BigInteger, Enum, Engine, DateTime, Table, \
    ForeignKey, Boolean, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base, relationship

from database.crud import CRUD
from database.core import session as sess
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
    email = Column(String, nullable=False)
    one_time_pass = Column(Boolean, nullable=False, default=True)
    _created_at = Column(DateTime, name='created_at', nullable=False, default=datetime.datetime.now)

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


class Category(Base, CRUD):
    __tablename__ = 'categories'
    title = Column(String, nullable=False, unique=True, primary_key=True)
    products = relationship(
        'Product',
        back_populates="category",
        uselist=True
    )

    @classmethod
    def create(cls, **kwargs):
        session = sess.sess
        instance = cls(title=kwargs.get('title'))
        session.add(instance)
        session.commit()
        return instance


class Manufacturer(Base, CRUD):
    __tablename__ = 'manufacturers'
    title = Column(String, nullable=False, unique=True, primary_key=True)

    products = relationship(
        'Product',
        back_populates='manufacturer',
        uselist=True
    )

    @classmethod
    def create(cls, **kwargs):
        session = sess.sess
        instance = cls(title=kwargs.get('title'))
        session.add(instance)
        session.commit()
        return instance


class Product(Base, CRUD):
    __tablename__ = 'products'
    id = Column(BigInteger, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    manufacturer_id = Column(ForeignKey('manufacturers.title', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    category_id = Column(ForeignKey('categories.title', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    quantity = Column(Float, nullable=False, default=0.0)
    price = Column(Float, nullable=False, default=0.0)
    units = Column(String, nullable=False)

    category = relationship(
        Category,
        back_populates="products",
        uselist=False
    )
    manufacturer = relationship(
        Manufacturer,
        back_populates='products',
        uselist=False
    )

    @staticmethod
    def get_categories_and_manufacturers(kwargs: dict) -> tuple:
        mf_title = kwargs.pop('manufacturer')
        manufacturer = Manufacturer.get_many(title=mf_title)
        if not manufacturer:
            manufacturer = Manufacturer.create(title=mf_title)
        else:
            manufacturer = manufacturer[0]
        category_name = kwargs.pop('category')
        category = Category.get_many(title=category_name)
        if not category:
            category = Category.create(title=category_name)
        else:
            category = category[0]
        return manufacturer, category

    @classmethod
    def create(cls, **kwargs):
        manufacturer, category = cls.get_categories_and_manufacturers(kwargs)
        pk = cls.get_autoincrement()
        instance = cls(id=pk, manufacturer=manufacturer, category=category, **kwargs)
        session = sess.sess
        session.add(instance)
        session.commit()

    @classmethod
    def update(cls, params: dict, **kwargs):
        manufacturer, category = cls.get_categories_and_manufacturers(kwargs)
        kwargs['manufacturer'] = manufacturer
        kwargs['category'] = category
        instance = cls.get(params.get('id'))
        if instance:
            for k, v in kwargs.items():
                setattr(instance, k, v)
            session = sess.sess
            session.add(instance)
            session.commit()


class Customer(Base, CRUD):
    __tablename__ = 'customers'
    id = Column(BigInteger, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    inn = Column(String)
    kpp = Column(String)


def create_tables(engine: Engine):
    Base.metadata.create_all(bind=engine, checkfirst=True)
    sess.init()
    count = Manager.get_count()
    if not count:
        Manager.create(
            **{
                'username': 'admin',
                'password': 'admin',
                'role': 'admin',
                'name': 'admin',
                'surname': 'god',
                'email': 'email@email.ru'
            }
        )

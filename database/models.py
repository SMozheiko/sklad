import datetime

from sqlalchemy import Column, String, Float, BigInteger, Enum, Engine, DateTime, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

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


association_table = Table(
    "products_categories",
    Base.metadata,
    Column("product_id", ForeignKey("products.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
)


class Category(Base, CRUD):
    __tablename__ = 'categories'
    id = Column(BigInteger, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    products = relationship(
        'Product',
        secondary=association_table, back_populates="categories"
    )


class Manufacturer(Base, CRUD):
    __tablename__ = 'manufacturers'
    id = Column(BigInteger, primary_key=True)
    title = Column(String, nullable=False, unique=True)

    products = relationship(
        'Product',
        back_populates='manufacturer',
        uselist=True
    )


class Product(Base, CRUD):
    __tablename__ = 'products'
    id = Column(BigInteger, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    manufacturer_id = Column(ForeignKey('manufacturers.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    quantity = Column(Float, nullable=False, default=0.0)
    price = Column(Float, nullable=False, default=0.0)
    units = Column(String, nullable=False)

    categories = relationship(
        Category,
        secondary=association_table, back_populates="products"
    )
    manufacturer = relationship(
        Manufacturer,
        back_populates='products',
        uselist=False
    )


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

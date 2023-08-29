import datetime

from sqlalchemy import Column, String, Float, BigInteger, Engine, DateTime, ForeignKey, Boolean, Date
from sqlalchemy.orm import declarative_base, relationship

from database.crud import CRUD
from database.core import session as sess
from settings import settings
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

    orders = relationship(
        'Order',
        back_populates='manager',
        uselist=True
    )

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
    kind = Column(String, nullable=True)
    title = Column(String, nullable=False, unique=True)
    inn = Column(String, nullable=True)
    kpp = Column(String, nullable=True)
    region = Column(String, nullable=True)
    district = Column(String, nullable=True)
    place = Column(String, nullable=True)
    street = Column(String, nullable=True)
    building = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    orders = relationship(
        'Order',
        back_populates='customer',
        uselist=True
    )

    @property
    def payments(self):
        return 0

    @property
    def verbose_title(self) -> str:
        return f'{self.kind} "{self.title}"' if self.kind else self.title

    @property
    def address(self) -> str:
        return '{}{}{}{}{}'.format(
            self.region + ', ' if self.region else '',
            self.district + ', ' if self.district else '',
            self.place + ', ' if self.place else '',
            self.street + ', ' if self.street else '',
            f'д. {self.building}' if self.building else ''
        )


class Order(Base, CRUD):
    __tablename__ = 'orders'
    id = Column(BigInteger, primary_key=True)
    manager_id = Column(ForeignKey(Manager.id, onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    customer_id = Column(ForeignKey(Customer.id, onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updated_at = Column(DateTime, nullable=True, default=datetime.datetime.now)
    payed = Column(Float(decimal_return_scale=2), nullable=False, default=0)
    delivery_date = Column(Date, nullable=False, default=datetime.datetime.today)

    @property
    def cost(self) -> float:
        return sum(
            [x.price * x.quantity for x in self.items]
        )

    manager = relationship(
        Manager,
        back_populates='orders',
        uselist=False
    )

    customer = relationship(
        Customer,
        back_populates='orders',
        uselist=False
    )

    items = relationship(
        'OrderItem',
        back_populates='order',
        uselist=True
    )


class OrderItem(Base, CRUD):
    __tablename__ = 'orders_items'
    id = Column(BigInteger, primary_key=True)
    order_id = Column(ForeignKey(Order.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    product_id = Column(ForeignKey(Product.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    quantity = Column(Float(decimal_return_scale=3), nullable=False, default=0)
    price = Column(Float(decimal_return_scale=3), nullable=False, default=0)
    order = relationship(
        Order,
        back_populates='items',
        uselist=False
    )

    product = relationship(
        Product,
        uselist=False
    )


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
    count = Customer.get_count()
    if not count:
        Customer.create(
            **{
                'title': 'Частное лицо'
            }
        )

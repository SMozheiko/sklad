from sqlalchemy import Column, String, Float, BigInteger, Enum
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Manager(Base):
    __tablename__ = 'managers'
    id = Column(BigInteger, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    @property
    def full_name(self):
        return f"{self.surname} {self.name}"


if __name__ == '__main__':
    user = Manager(
        username='username',
        password='password',
        role='role',
        name='name',
        surname='surname'
    )
    for field in user.__dict__.items():
        print(field)


from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session

from settings import db_settings


def _get_engine():
    engine = create_engine(db_settings.get_src())
    try:
        yield engine
    finally:
        engine.dispose()


def get_engine() -> Engine:
    for e in _get_engine():
        return e


def _get_session():
    session = Session(bind=get_engine())
    try:
        yield session
    finally:
        session.close()


def get_session() -> Session:
    for sess in _get_session():
        return sess

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session

from settings import db_settings


def _get_engine() -> Engine:
    while True:
        engine = create_engine(db_settings.get_src())
        try:
            yield engine
        finally:
            engine.dispose()


engines = _get_engine()


def _get_session() -> Session:
    while True:
        session = Session(bind=next(engines))
        try:
            yield session
        finally:
            session.close()

session = _get_session()
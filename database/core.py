from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session

from settings import db_settings


def get_engine() -> Engine:
    return create_engine(db_settings.get_src())


def _get_session():
    engines = get_engine()
    try:
        while True:
            sess = Session(bind=engines)
            try:
                yield sess
            finally:
                sess.close()
    except:
        pass
    finally:
        engines.dispose()


class SessionManager:

    def __init__(self):
        self._eng = None
        self.session = None

    def init(self):
        if not self.session:
            self._eng = get_engine()
            self.session = Session(bind=self._eng)

    @property
    def sess(self) -> Session:
        return self.session

    def __del__(self):
        self.session.close()
        self._eng.dispose()


session = SessionManager()

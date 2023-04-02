from typing import Iterable


class CRUD:

    _field = '_sa_instance_state'

    def __init__(self):
        super().__init__()

    def dict(self, *, include: Iterable = None, exclude: Iterable = None) -> dict:
        include = include or set(self.__dict__.keys())
        exclude = exclude or set()
        result = {}
        for k, v in self.__dict__.items():
            if k != self._field and k in include and k not in exclude:
                result[k] = v
        return result

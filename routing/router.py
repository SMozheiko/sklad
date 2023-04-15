from collections import deque
from typing import List, Callable

from database.core import get_engine
from database.models import Manager, create_tables
from utils import render


class URLPattern:

    def __init__(self, url: str, callback: Callable, methods: List[str]):

        self.instance = {
           url: callback
        }
        self.methods = methods


class Router:

    def __init__(self):
        self.user = None
        self._post = {}
        self._get = {}
        self.actions = deque(maxlen=2)
        create_tables(get_engine())

    def register(self, urls: List[URLPattern]):
        for url in urls:
            for method in url.methods:
                route = getattr(self, method)
                route.update(**url.instance)

    def login(self, action: str, method: str, data: dict = None):
        errors = []
        if data:
            user = Manager.get_many(**data)
            if user:
                self.user = user
                return self.dispatch(action, method, data)
            errors.append('Пользователь не найден')
        return render('managers', 'login.html', {'errors': errors})

    def dispatch(self, action: str, method: str, data: dict = None) -> str:
        if method == 'get':
            self.actions.append((action, method, data))

        if self.user is None:
            return self.login(action, method, data)

        _method = getattr(self, f'_{method}').get(action)
        if _method:
            if method == 'get':
                return _method.get(data)
            _method.post(data)
            return self.dispatch(*self.actions[0])
        return 'Not found'

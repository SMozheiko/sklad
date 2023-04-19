from collections import deque
from typing import List, Callable

from database.core import get_engine
from database.models import Manager, create_tables
from schema.http import Request, Response
from utils import render


class URLPattern:

    def __init__(self, url: str, callback: Callable, methods: List[str], tag: str):

        self.instance = {
           url: (callback, tag)
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
                route = getattr(self, f"_{method}")
                route.update(**url.instance)

    def login(self, request: Request):
        errors = []
        if request.data:
            user = Manager.get_many(**data)
            if user:
                self.user = user
                return self.dispatch(*self.actions[0])
            errors.append('Пользователь не найден')
            
        return Response(tag='frame', html=render('managers', 'login.html', {'errors': errors}), errors=errors)

    def dispatch(self, action: str, method: str, params: dict = None, data: dict = None) -> Response:
        if method == 'get':
            self.actions.append((action, method, params, data))
        
        request = Request.parse_obj({'method': method, 'action': action, 'params': params, 'data': data})

        response = None
        if self.user is None:
            return self.login(request)
        
        _method, tag = getattr(self, f'_{method}').get(action)
        if _method:
            if method == 'get':
                return Response(tag=tag, html=_method.get(request))
                
            result = _method.post(request)
            if not result:
                return self.dispatch(*self.actions[0])
            
            return Response(tag=tag, html=result)
        return Response(tag='body', html='Not Found')

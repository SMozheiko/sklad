from collections import deque
from typing import List, Type

from database.core import engines
from database.models import Manager, create_tables
from schema.http import Request, Response
from views.base import BaseView
from utils import render, get_hashed_password


class URLPattern:

    def __init__(self, url: str, callback: Type[BaseView], methods: List[str], tag: str, title: str = None):

        self.instance = {
           url: (callback, tag)
        }
        self.methods = methods
        self.action = url
        self.title = title


class Router:

    _links = [
    ]

    def __init__(self):
        self.user = None
        self._post = {}
        self._get = {}
        self.actions = deque(maxlen=2)
        create_tables(next(engines))

    def register(self, urls: List[URLPattern]):
        for url in urls:
            for method in url.methods:
                route = getattr(self, f"_{method}")
                route.update(**url.instance)
            if url.title:
                self._links.append(
                    {
                        'action': url.action,
                        'title': url.title
                    }
                )

    def login(self, request: Request):
        errors = []
        if request.data:
            user = Manager.get_many(username=request.data.get('username'))
            if user:
                user = user[0]
                if user.password == get_hashed_password(request.data.get('password')):
                    self.user = user
                    return self.dispatch(*self.actions[0])
                errors.append('Не правильный пароль')
            else:
                errors.append('Пользователь не найден')
            
        return Response(tag='frame', html=render('managers', 'login.html', {'errors': errors}), errors=errors)

    def get_header_html(self, action: str) -> str:
        if action in [x['action'] for x in self._links]:
            return render('', 'header.html', {'action': action, 'user': self.user, 'links': self._links})

    def dispatch(self, action: str, method: str, params: dict = None, data: dict = None) -> Response:
        if action == 'logout':
            self.user = None
            return self.dispatch(*self.actions[-1])

        if method == 'get' and action != 'password_reset':
            self.actions.append((action, method, params, data))
        
        request = Request.parse_obj(
            {'method': method, 'action': action, 'params': params, 'data': data, 'user': self.user}
        )
        if self.user is None and action != 'password_reset':
            return self.login(request)
        
        _method, tag = getattr(self, f'_{method}').get(action)
        if _method:
            if method == 'get':
                return Response(tag=tag, html=_method.get(request), header=self.get_header_html(request.action))
                
            result = _method.post(request)
            if not result:
                return self.dispatch(*self.actions[0])
            
            return Response(tag=tag, html=result, header=self.get_header_html(request.action))
        return Response(tag='body', html='Not Found')

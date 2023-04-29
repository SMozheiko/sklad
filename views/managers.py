from database.models import Manager
from schema.http import Request
from views.base import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView
from utils import render, get_hashed_password


class ManagersListView(BaseListView):

    template_path = 'managers'
    template = 'list.html'
    model = Manager


class ManagerCreateView(BaseCreateView):

    model = Manager
    template = "create.html"
    template_path = 'managers'

    def post(self, request: Request):
        try:
            super().post(request)
        except Exception as e:
            return render(self.template_path, self.template, {'errors': [str(e)]})
    
    def get(self, request: Request):
        return render(self.template_path, self.template, {})


class ManagerUpdateView(BaseUpdateView):
    model = Manager
    template = "update.html"
    template_path = 'managers'

    def post(self, request: Request):
        try:
            super().post(request)
        except Exception as e:
            context = self.get_context(request)
            context.update({'errors': [str(e)]})
            return render(self.template_path, self.template, context)


class ManagerPasswordResetView(BaseUpdateView):
    model = Manager
    template = 'password_reset.html'
    template_path = 'managers'

    def get_queryset(self, request: Request):
        return self.model.get_many(username=request.data.get('username'))
    
    def post(self, request: Request):
        if request.data.get('password') != request.data.get('password2'):
            context = self.get_context(request)
            context.update({'errors': ['Пароль и подтверждение не совпадают']})
            return render(self.template_path, self.template, context)

        password = get_hashed_password(request.data.get('password'))
        self.model.update({'username': request.data.pop('username')}, password=password)



class ManagerDeleteView(BaseDeleteView):
    model = Manager
    template = 'delete.html'
    template_path = 'managers'
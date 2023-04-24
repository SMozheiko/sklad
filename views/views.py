from database.models import Manager
from schema.http import Request
from views.base import BaseListView, BaseCreateView
from utils import render


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
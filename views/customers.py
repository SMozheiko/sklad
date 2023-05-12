import math

from database.models import Customer
from schema.http import Request
from utils import render
from views.base import BaseListView, BaseDeleteView, BaseCreateView
from views.mixins import LoginRequiredMixin


class CustomerListView(BaseListView):
    model = Customer
    template = "list.html"
    template_path = 'customers'

    def __init__(self):
        super().__init__()
        self.request_params = {}
    
    def get_context(self, request: Request):
        self.request_params.update(request.params)
        queryset = Customer.query()
        context = {
            'user': request.user
        }
        page = int(self.request_params.get('page', 1))
        limit = int(self.request_params.get('limit', 10))

        search = self.request_params.get('search', '')
        if search:
            queryset = queryset.filter(Customer.title.icontains(search))

        pages = int(math.ceil(queryset.count() / limit))

        if page > pages:
            page = pages
            self.request_params['page'] = pages
        if pages == 0:
            page = 1
            pages = 1
            self.request_params['page'] = pages
            self.request_params['pages'] = pages
        queryset = queryset.offset(
                (page - 1) * limit
            ).limit(
                limit
            ).all()
        context['objects'] = queryset
        context['page'] = page
        context['limit'] = limit
        context['pages'] = pages
        context['search'] = search
        return context


class CustomerDeleteView(LoginRequiredMixin, BaseDeleteView):

    model = Customer
    template = 'delete.html'
    template_path = 'customers'


class CustomerCreateView(LoginRequiredMixin, BaseCreateView):
    
    model = Customer
    template = 'create.html'
    template_path = 'customers'

    def post(self, request: Request):
        try:
            super().post(request)
        except Exception as e:
            return render(self.template_path, self.template, {'errors': [str(e)]})
    
    def get(self, request: Request):
        return render(self.template_path, self.template, {})
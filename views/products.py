import math

from database.models import Category, Product, Manufacturer
from schema.http import Request
from utils import render
from views.base import BaseListView, BaseCreateView, BaseDeleteView, BaseUpdateView
from views.mixins import LoginRequiredMixin


class ProductsListView(LoginRequiredMixin, BaseListView):

    model = Product
    template = 'list.html'
    template_path = 'products'

    def __init__(self):
        super().__init__()
        self.request_params = {}
    
    def get_context(self, request: Request):
        self.request_params.update(request.params)
        queryset = Product.query()
        context = {
            'user': request.user,
            'categories': Category.get_many(),
            'manufacturers': Manufacturer.get_many()
        }
        page = self.request_params.get('page', 1)
        limit = self.request_params.get('limit', 20)

        search = self.request_params.get('search', '')
        if search:
            queryset = queryset.filter(Product.title.icontains(search))

        manufacturers = self.request_params.get('filter', {}).get('manufacturer', [])
        categories = self.request_params.get('filter', {}).get('category', [])
        if manufacturers:
            queryset = queryset.filter(Product.manufacturer_id.in_(manufacturers))
        if categories:
            queryset = queryset.filter(Product.category_id.in_(categories))

        ordering = self.request_params.get('sorting', {}).get('order')
        if ordering:
            ordering = bool(int(ordering))
        if self.request_params.get('sorting', {}).get('sort') == 'manufacturer':
            if ordering:
                queryset = queryset.order_by(Product.manufacturer_id.desc())
            else:
                queryset = queryset.order_by(Product.manufacturer_id.asc())
        elif self.request_params.get('sorting', {}).get('sort') == 'category':
            if ordering:
                queryset = queryset.order_by(Product.category_id.desc())
            else:
                queryset = queryset.order_by(Product.category_id.asc())
        else:
            if ordering:
                queryset = queryset.order_by(Product.title.desc())
            else:
                queryset = queryset.order_by(Product.title.asc())

        queryset = queryset.offset(
                int((page - 1) * limit)
            ).limit(
                int(limit)
            ).all()
        context['objects'] = queryset
        context['page'] = page
        context['limit'] = limit
        context['pages'] = int(math.ceil(Product.get_count() / limit))
        context.setdefault('filter', {})['category'] = categories
        context.setdefault('filter', {})['manufacturer'] = manufacturers
        context.setdefault('sorting', {})['order'] = ordering
        context.setdefault('sorting', {})['sort'] = self.request_params.get('sorting', {}).get('sort')
        context['search'] = search
        
        return context


class ProductsCreateView(LoginRequiredMixin, BaseCreateView):

    model = Product
    template = 'create.html'
    template_path = 'products'
    context_variable = 'manufacturers'

    def get_queryset(self, request: Request):
        return Manufacturer.get_many()

    def get_context(self, request: Request):
        context = super().get_context(request)
        context.update(categories=Category.get_many())
        return context


class ProductDeleteView(LoginRequiredMixin, BaseDeleteView):

    model = Product
    template = 'delete.html'
    template_path = 'products'


class ProductUpdateView(LoginRequiredMixin, BaseUpdateView):

    model = Product
    template = 'update.html'
    template_path = 'products'

    def post(self, request: Request):
        try:
            super().post(request)
        except Exception as e:
            context = self.get_context(request)
            context.update({'errors': [str(e)]})
            return render(self.template_path, self.template, context)

    def get_context(self, request: Request) -> dict:
        context = super().get_context(request)
        context.update(
            {
                'categories': Category.query().all(),
                'manufacturers': Manufacturer.query().all()
            }
        )
        return context

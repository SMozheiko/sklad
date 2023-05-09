from database.models import Category, Product, Manufacturer
from schema.http import Request
from utils import render
from views.base import BaseListView, BaseCreateView, BaseDeleteView, BaseUpdateView
from views.mixins import LoginRequiredMixin


class ProductsListView(LoginRequiredMixin, BaseListView):

    model = Product
    template = 'list.html'
    template_path = 'products'
    
    def get_context(self, request: Request):
        if not request.params:
            context = super().get_context(request)
            context['categories'] = Category.get_many()
            context['manufacturers'] = Manufacturer.get_many()
            return context
        if request.params.get('search'):
            search = request.params.pop('search')
            context = super().get_context(request)
            context['categories'] = Category.get_many()
            context['manufacturers'] = Manufacturer.get_many()
            context['objects'] = [x for x in context['objects'] if x.title.lower().find(search.lower()) != -1]
            return context

        queryset = Product.query()
        context = {
            'user': request.user,
            'categories': Category.get_many(),
            'manufacturers': Manufacturer.get_many()
        }
        manufacturers = request.params.get('filter').get('manufacturer')
        categories = request.params.get('filter').get('category')
        if manufacturers:
            queryset = queryset.filter(Product.manufacturer_id.in_(manufacturers))
        if categories:
            queryset = queryset.filter(Product.category_id.in_(categories))

        ordering = bool(int(request.params.get('sorting').get('order')))
        if request.params.get('sorting').get('sort') == 'manufacturer':
            if ordering:
                queryset = queryset.order_by(Product.manufacturer_id.desc())
            else:
                queryset = queryset.order_by(Product.manufacturer_id.asc())
        else:
            if ordering:
                queryset = queryset.order_by(Product.title.desc())
            else:
                queryset = queryset.order_by(Product.title.asc())

        context['objects'] = queryset.all()
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

from database.models import Category, Product, Manufacturer
from schema.http import Request
from views.base import BaseListView, BaseCreateView


class ProductsListView(BaseListView):

    model = Product
    template = 'list.html'
    template_path = 'products'


class ProductsCreateView(BaseCreateView):

    model = Product
    template = 'create.html'
    template_path = 'products'

    def get_context(self, request: Request):
        manufacturers = Manufacturer.get_many()
        context = self.base_context.copy()
        context.update(
            {
                'manufacturers': manufacturers,
                'errors': []
            }
        )
        return context

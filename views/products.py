from database.models import Category, Product, Manufacturer
from schema.http import Request
from views.base import BaseListView, BaseCreateView
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

        context = {
            'user': request.user,
            'categories': Category.get_many(),
            'manufacturers': Manufacturer.get_many()
        }
        manufacturers = request.params.get('filter').get('manufacturer')
        categories = request.params.get('filter').get('category')
        if manufacturers and categories:
            queryset = self.model.query().filter(self.model.manufacturer_id.in_(manufacturers)).all()
            queryset = [x for x in queryset if set([a.id for a in x.categories]).intersection(set(categories))]
        elif not manufacturers and categories:
            queryset = []
            exist = set()
            cats = [x for x in context['categories'] if x.id in categories]
            for category in cats:
                for item in category.products:
                    if item.id not in exist:
                        queryset.append(item)
                        exist.add(item.id)
        elif not manufacturers and not categories:
            queryset = self.model.get_many()
        else:
            queryset = self.model.query().filter(self.model.manufacturer_id.in_(manufacturers)).all()
            for x in queryset:
                print(x.categories, x.title)

        if request.params.get('sorting').get('sort') == 'manufacturer':
            queryset.sort(key=lambda x: x.manufacturer.title, reverse=bool(int(request.params.get('sorting').get('order'))))
        else:
            queryset.sort(key=lambda x: x.title, reverse=bool(int(request.params.get('sorting').get('order'))))
        context['objects'] = queryset
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


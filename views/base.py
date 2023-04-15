from typing import Type

from database.models import Base
from settings import settings
from utils import render


class BaseView:

    template: str
    template_path: str = ''
    base_context = {}

    def get_context(self, **kwargs):
        return self.base_context

    def get(self, **kwargs):
        context = self.get_context(**kwargs)
        return render(self.template_path, self.template, context)


class BaseModelView(BaseView):

    model: Type[Base] = None
    context_variable = 'object'
    queryset = None

    def get_queryset(self, **kwargs):
        if self.queryset:
            return self.queryset
        return self.model.get(**kwargs)

    def get_context(self, **kwargs):
        instance = self.get_queryset(**kwargs)
        return self.base_context.update({self.context_variable: instance})


class BaseListView(BaseModelView):

    context_variable = 'objects'
    queryset = []

    def get_queryset(self, **kwargs):
        return self.queryset or self.model.get_many(**kwargs)


class BaseDetailView(BaseModelView):

    queryset = None
    pk_key = 'pk'

    def get_queryset(self, **kwargs):
        return self.queryset or self.model.get(kwargs.get(self.pk_key))


class BaseDeleteView(BaseDetailView):

    def post(self, **kwargs):
        self.model.delete(kwargs.get(self.pk_key))


class BaseUpdateView(BaseDetailView):

    def post(self, **kwargs):
        kwargs['pk'] = kwargs.pop(self.pk_key)
        return self.model.update(**kwargs)


class BaseCreateView(BaseModelView):

    def post(self, **kwargs):
        return self.model.create(**kwargs)

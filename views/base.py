from typing import Type

from database.models import Base
from schema.http import Request
from settings import settings
from utils import render


class BaseView:

    template: str
    template_path: str = ''
    base_context = {}

    def get_context(self, request: Request):
        return self.base_context

    def get(self, request: Request):
        context = self.get_context(request)
        return render(self.template_path, self.template, context)


class BaseModelView(BaseView):

    model: Type[Base] = None
    context_variable = 'object'
    queryset = None

    def get_queryset(self, request: Request):
        if self.queryset:
            return self.queryset
        return self.model.get(**request.params)

    def get_context(self, request: Request):
        instance = self.get_queryset(request)
        self.base_context.update({self.context_variable: instance})
        return self.base_context


class BaseListView(BaseModelView):

    context_variable = 'objects'
    queryset = []

    def get_queryset(self, request: Request):
        return self.queryset or self.model.get_many(**request.params)


class BaseDetailView(BaseModelView):

    queryset = None
    pk_key = 'pk'

    def get_queryset(self, request: Request):
        return self.queryset or self.model.get(request.params.get(self.pk_key))


class BaseDeleteView(BaseDetailView):

    def post(self, request: Request):
        self.model.delete(request.data.get(self.pk_key))


class BaseUpdateView(BaseDetailView):

    def post(self, request: Request):
        kwargs = request.data.copy()
        kwargs['pk'] = request.data.pop(self.pk_key)
        return self.model.update(**kwargs)


class BaseCreateView(BaseModelView):

    def post(self, request: Request):
        return self.model.create(**request.data)

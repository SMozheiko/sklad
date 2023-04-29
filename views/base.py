from typing import Type

from database.models import Base
from schema.http import Request
from utils import render


class BaseView:

    template: str
    template_path: str = ''
    base_context = {}

    def get_context(self, request: Request):
        context = self.base_context.copy()
        context.update({'user': request.user})
        return context

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
        context = super().get_context(request)
        context.update({self.context_variable: instance})
        return context


class BaseListView(BaseModelView):

    context_variable = 'objects'
    queryset = []

    def get_queryset(self, request: Request):
        return self.queryset or self.model.get_many(**request.params)


class BaseDetailView(BaseModelView):

    queryset = None

    def get_queryset(self, request: Request):
        return self.queryset or self.model.get(request.params.get('id'))


class BaseDeleteView(BaseDetailView):

    def post(self, request: Request):
        self.model.delete(request.params)


class BaseUpdateView(BaseDetailView):

    def post(self, request: Request):
        return self.model.update(request.params, **request.data)


class BaseCreateView(BaseModelView):

    def post(self, request: Request):
        return self.model.create(**request.data)

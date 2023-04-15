from database.models import Manager
from views.base import BaseListView


class ManagersListView(BaseListView):

    template_path = 'managers'
    template = 'list.html'
    model = Manager

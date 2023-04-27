from routing.router import Router, URLPattern
from views.managers import ManagersListView, ManagerCreateView, ManagerUpdateView, ManagerDeleteView


urlpatterns = [
    URLPattern('managers_list', ManagersListView(), methods=['get'], tag='body'),
    URLPattern('create_manager', ManagerCreateView(), methods=['get', 'post'], tag='frame'),
    URLPattern('update_manager', ManagerUpdateView(), methods=['get', 'post'], tag='frame'),
    URLPattern('delete_manager', ManagerDeleteView(), methods=['get', 'post'], tag='frame'),
]

router = Router()
router.register(urlpatterns)

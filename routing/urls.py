from routing.router import Router, URLPattern
from views.views import ManagersListView, ManagerCreateView


urlpatterns = [
    URLPattern('managers_list', ManagersListView(), methods=['get'], tag='body'),
    URLPattern('create_manager', ManagerCreateView(), methods=['get', 'post'], tag='frame')
]

router = Router()
router.register(urlpatterns)

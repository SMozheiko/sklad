from routing.router import Router, URLPattern
from views.views import ManagersListView


urlpatterns = [
    URLPattern('managers_list', ManagersListView)
]

router = Router()
router.register(urlpatterns)

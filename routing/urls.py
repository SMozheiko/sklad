from routing.router import Router, URLPattern
from views.managers import ManagersListView, ManagerCreateView, ManagerUpdateView, ManagerDeleteView, \
    ManagerPasswordResetView
from views.products import ProductsListView, ProductsCreateView, ProductDeleteView, ProductUpdateView
from views.customers import CustomerListView, CustomerCreateView, CustomerDeleteView, CustomerDetailView, \
    CustomerUpdateView


urlpatterns = [
    URLPattern('managers_list', ManagersListView(), methods=['get'], tag='body', title='Менеджеры'),
    URLPattern('create_manager', ManagerCreateView(), methods=['get', 'post'], tag='frame'),
    URLPattern('update_manager', ManagerUpdateView(), methods=['get', 'post'], tag='frame'),
    URLPattern('delete_manager', ManagerDeleteView(), methods=['get', 'post'], tag='frame'),
    URLPattern('password_reset', ManagerPasswordResetView(), methods=['get', 'post'], tag='frame'),
    URLPattern('products_list', ProductsListView(), methods=['get'], tag='body', title='Продукты'),
    URLPattern('create_product', ProductsCreateView(), methods=['get', 'post'], tag='frame'),
    URLPattern('delete_product', ProductDeleteView(), methods=['get', 'post'], tag='frame'),
    URLPattern('update_product', ProductUpdateView(), methods=['get', 'post'], tag='frame'),
    URLPattern('customerss_list', CustomerListView(), methods=['get'], tag='body', title='Контрагенты'),
    URLPattern('create_customer', CustomerCreateView(), methods=['get', 'post'], tag='frame'),
    URLPattern('delete_customer', CustomerDeleteView(), methods=['get', 'post'], tag='frame'),
    URLPattern('detail_customer', CustomerDetailView(), methods=['get', 'post'], tag='frame'),
    URLPattern('update_customer', CustomerUpdateView(), methods=['get', 'post'], tag='frame'),
]

router = Router()
router.register(urlpatterns)

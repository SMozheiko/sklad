from database.models import Order, OrderItem, Product, Customer, Manager
from views.base import BaseListView, BaseDetailView, BaseCreateView
from views.mixins import LoginRequiredMixin


class OrderCreateView(LoginRequiredMixin, BaseCreateView):
    model = Order
    template = 'create.html'
    template_path = 'orders'


class OrderListView(LoginRequiredMixin, BaseListView):
    model = Order
    template_path = 'orders'
    template = 'list.html'

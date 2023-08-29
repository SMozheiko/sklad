from database.models import Order, OrderItem, Product, Customer, Manager
from schema.http import Request
from views.base import BaseListView, BaseDetailView, BaseCreateView
from views.mixins import LoginRequiredMixin


class OrderCreateView(LoginRequiredMixin, BaseCreateView):
    model = Order
    template = 'create.html'
    template_path = 'orders'
    context_variable = 'products'

    def get_queryset(self, request: Request):
        return Product.get_many()

    def get_context(self, request: Request):
        context = super().get_context(request)
        context.update(customers=Customer.get_many())
        return context

    def post(self, request: Request):
        customer_id = request.data.get('customer')
        order = Order.create(
            manager_id=request.user.id,
            customer_id=customer_id,
        )
        for position in request.data.get('positions'):
            OrderItem.create(
                product_id=int(position.get('id')),
                quantity=float(position.get('quantity')),
                price=float(position.get('price')),
                order=order
            )


class OrderListView(LoginRequiredMixin, BaseListView):
    model = Order
    template_path = 'orders'
    template = 'list.html'

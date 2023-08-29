from database.models import Product, Customer
from schema.rest import ProductsList, RestRequest, CustomersList


class ProductsListView:

    def get(self, request: RestRequest) -> ProductsList:
        result = Product.query().filter_by(**request.filter_by if request.filter_by else {}).order_by(request.dict().get('order_by', 'id'))
        if request.limit is not None:
            result = result.offset(request.dict().get('offset', 0)).limit(request.limit)
        response = ProductsList(
            status='OK',
            result=list()
        )
        for item in result:
            response.result.append(
                {
                    'id': item.id,
                    'title': item.title,
                    'quantity': item.quantity,
                    'price': item.price,
                    'units': item.units
                }
            )
        return response


class CustomersListView:

    def get(self, request: RestRequest) -> CustomersList:
        result = Customer.query().filter_by(**request.filter_by if request.filter_by else {}).order_by(request.dict().get('order_by', 'id'))
        if request.limit is not None:
            result = result.offset(request.dict().get('offset', 0)).limit(request.limit)
        response = CustomersList(
            status='OK',
            result=list()
        )
        for item in result:
            response.result.append(
                {
                    'id': item.id,
                    'title': item.title,
                }
            )
        return response

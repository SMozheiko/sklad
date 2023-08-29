import eel

from routing.urls import router
from schema.rest import RestRequest, BaseJsonResponse
from views.json_views import ProductsListView, CustomersListView


@eel.expose
def route(*args, **kwargs):
    print(args)
    response = router.dispatch(*args, **kwargs)
    eel.renderResponse(response.dict())


@eel.expose
def json_data(request: dict) -> dict:
    routes = {
        'customers': CustomersListView(),
        'products': ProductsListView()
    }
    request = RestRequest.parse_obj(request)
    handler = routes.get(request.action)
    response = handler.get(request)
    return response.dict()


if __name__ == '__main__':
    eel.init('frontend')
    eel.start('index.html')

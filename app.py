import eel

from routing.urls import router
from schema.http import Response


@eel.expose
def route(*args, **kwargs):
    print(args)
    response = router.dispatch(*args, **kwargs)
    eel.renderResponse(response.dict())


if __name__ == '__main__':
    eel.init('frontend')
    eel.start('index.html')

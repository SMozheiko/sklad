import eel

from routing.urls import router


@eel.expose
def route(*args, **kwargs):
    print(args)
    return router.dispatch(*args, **kwargs)


if __name__ == '__main__':
    eel.init('frontend')
    eel.start('index.html')

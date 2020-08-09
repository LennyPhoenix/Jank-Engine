from . import Application


class Globals:
    app: Application


def get_app() -> Application:
    return Globals.app


def set_app(app: Application):
    Globals.app = app

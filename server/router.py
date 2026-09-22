from .constants import allowed_methods
from .handler import RequestHandler


class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, path, methods):
        def register_route(handler):
            if path in self.routes:
                raise Exception(f"Route '{path}' already registered!")
            self.routes[path] = {}
            for method in methods:
                if method not in allowed_methods:
                    raise Exception(f"Invalid HTTP method '{method}'")
                self.routes[path][method] = handler

            return handler
        return register_route

    def add_handler(self, path, handler, method = "GET"):
        if not isinstance(handler, RequestHandler):
            raise TypeError(
                "handler must inherit RequestHandler"
            )

        if method not in allowed_methods:
            raise ValueError(
                f"Invalid HTTP method '{method}'"
            )

        if path not in self.routes:
            self.routes[path] = {}

        if method in self.routes[path]:
            raise ValueError(
                f"Roule '{path}' with method"
                f"'{method}' already registered"
            )

        self.routes[path][method] = handler
        

    def handle_route(self, request, response):
        route = self.routes.get(request.path)
        if route is None:
            response.status_code = 404 # Not Found
            return
        handler = route.get(request.method)
        if request.method not in allowed_methods or handler is None:
            response.status_code = 405 # Method Not Allowed
            return

        try:
            handler(request, response)
        except Exception:
            response.status_code = 500 # Internal Server Error

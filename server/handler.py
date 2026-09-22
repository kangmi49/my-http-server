from abc import ABC, abstractmethod
import json


class RequestHandler(ABC):
    """
    所有类式请求处理器的抽象父类
    """

    def __call__(self, request, response):
        return self.handle(request, response)

    @abstractmethod
    def handle(self, request, response):
        pass


class TextHandler(RequestHandler):
    """
    返回纯文本
    """

    def __init__(self, text):
        self.text = text

    def handle(self, request, response):
        response.headers["Content-Type"] = "text/plain"
        response.body = self.text


class JsonHandler(RequestHandler):
    """
    返回 JSON
    """

    def __init__(self, data):
        self.data = data

    def handle(self, request, response):
        response.headers["Content-Type"] = "application/json"
        response.body = json.dumps(
            self.data,
            ensure_ascii=False
        )


class HtmlHandler(RequestHandler):
    """
    返回 HTML
    """

    def __init__(self, html):
        self.html = html

    def handle(self, request, response):
        response.headers["Content-Type"] = "text/html"
        response.body = self.html

class FileHandler(RequestHandler):

    def __init__(self, file_path):
        self.file_path = file_path

    def handle(
        self,
        request,
        response
    ):

        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                response.body = file.read()

            response.headers[
                "Content-Type"
            ] = "text/plain"

        except FileNotFoundError:

            response.status_code = 404
            response.body = "File Not Found"
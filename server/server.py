import socket
from concurrent.futures import ThreadPoolExecutor
from .router import Router
from .plumbing import Request, Response


class Server:
    def __init__(self, max_workers=8):
        self.router = Router()

        self.executor = ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix="http-worker"
        )

    def start(self, port=5000, host="", header_size=1024):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
            sock.listen(1)
            print(f"Listening on http://{socket.getfqdn()}:{port}/")
        try:
            while True:

                conn, addr = sock.accept()

                self.executor.submit(
                    self.handle_connection,
                    conn,
                    addr,
                    header_size
                )

        except KeyboardInterrupt:
            print("\nServer shutting down...")

        finally:
            self.executor.shutdown(
                wait=True
            ) 
            
    def handle_connection(self, conn, addr, header_size):
        request_bytes = conn.recv(header_size)
        with conn:
            response = Response()
            try:
                request = Request(request_bytes, addr)
                self.router.handle_route(request, response)
                print(f"{response.status_code} {request}")
            except Exception:
                response.status_code = 400
            conn.sendall(response.serialize())

    def route(self, uri, methods=None):
        if methods is None:
            methods = ["GET"]
        return self.router.add_route(uri, methods)

    def add_handler(self, path, handler, method = "GET"):
        self.router.add_handler(path, handler, method)
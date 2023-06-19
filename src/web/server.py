from http.server import BaseHTTPRequestHandler,HTTPServer
import re

from dotenv import dotenv_values
config = dotenv_values(".env")

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
        path = self.path
        if path == "/":
            path = "/dashboard.html"
        file = path.split("/")[len(path.split("/"))-1]
        self.send_header('Content-type',getMime(path))
        self.end_headers()

        if bool(re.compile("dashboard.html").search(path)):
            return self.wfile.write(serveFile('./src/web'+path))

        """
        Note: ([a-zA-Z0-9]*) matches all single word strings.
        no extra characters besides the following are allowed:
            - uppercase letters
            - lowercase letters
            - numbers

        To Extend stuff here you need to enter the required file here.
        You also might have to extend the getMime function down below!
        """

        if bool(re.compile("/res/([a-zA-Z0-9]*).png").search(path)):
            return self.wfile.write(serveFile(f"./src/web/res/{file}"))

        if bool(re.compile("/res/([a-zA-Z0-9]*).jpg").search(path)):
            return self.wfile.write(serveFile(f"./src/web/res/{file}"))

        if bool(re.compile("/static/([a-zA-Z0-9]*).css").search(path)):
            return self.wfile.write(serveFile(f"./src/web/static/{file}"))

        if bool(re.compile("/static/([a-zA-Z0-9]*).js").search(path)):
            return self.wfile.write(serveFile(f"./src/web/static/{file}"))

        self.wfile.write("no".encode())

def serveFile(path):
    # print(f"[WEB] Serving {path}") # For debug
    with open(path, 'rb') as file_handle:
        ret = file_handle.read()
        return ret

def getMime(file):
    if file.endswith('.js'):
        return 'application/javascript'
    if file.endswith('.css'):
        return 'text/css'
    if file.endswith('.jpg'):
        return 'image/jpeg'
    if file.endswith('.png'):
        return 'image/png'
    if file.endswith('.html'):
        return 'text/html'
    return 'text/plain'

def runWebserver(server_class=HTTPServer, handler_class=Server):
    port = int(config.get("WEB_PORT"))
    print(f"Webserver listening on http://localhost:{port}")
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    httpd.serve_forever()
    print("Webserver gone")

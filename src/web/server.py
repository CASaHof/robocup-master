from http.server import BaseHTTPRequestHandler,HTTPServer

class Server(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")

    # GET sends back a Hello world message
    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
        #self.send_header('Content-type','text/html')
        self.end_headers()
        if self.path.endswith("/"):
            self.send_header('Content-type','text/html')
            self.wfile.write(open('./src/web/dashboard.html', 'r').read().encode())
            return
        self.wfile.write("no".encode())

def runWebserver(server_class=HTTPServer, handler_class=Server, port=8764):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    httpd.serve_forever()

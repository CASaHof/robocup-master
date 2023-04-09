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
        # Serving files in python webserver

        if self.path.startswith("/res/") and self.path.endswith(".png"):
            self.send_header('Content-type','image/png')
            with open('./src/web'+self.path, 'rb') as file_handle:
                self.wfile.write( file_handle.read())
            return
        if self.path.startswith("/res/") and self.path.endswith(".jpg"):
            self.send_header('Content-type','image/jpeg')
            with open('./src/web'+self.path, 'rb') as file_handle:
                self.wfile.write( file_handle.read())
            return
        
        self.wfile.write("no".encode())

def runWebserver(server_class=HTTPServer, handler_class=Server, port=8764):
    print("Webserver listening on http://localhost:8765")
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    httpd.serve_forever()

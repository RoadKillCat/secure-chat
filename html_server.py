#! /usr/bin/python3.6
import http.server, os, socketserver

PORT = 80

os.chdir('/home/joe/secure_chat')
class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        #get all files
        fs = [f for f in os.listdir() if f in self.path]
        #if no file in dir, default to index.html
        f  = fs[0] if len(fs) else 'index.html'
        #open file in read binary mode and read
        with open(f, 'rb') as fh:
            body = fh.read()
        ctype = 'text/html' if f == 'index.html' else 'text/plain'

        self.send_response(200)
        self.send_header('Content-Type', ctype)
        self.end_headers()
        self.wfile.write(body)
    def log_message(*args):
        return

socketserver.TCPServer.allow_reuse_address = 1
with socketserver.TCPServer(('',PORT), Handler) as httpd:
    httpd.serve_forever()

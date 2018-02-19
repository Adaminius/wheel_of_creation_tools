# !/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer


# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    def index(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client
        index_val = open('index.html').read()
        # Write content as utf-8 data
        self.wfile.write(bytes(index_val, "utf8"))

    # GET
    def do_GET(self):
        if self.path == '/':
            self.index()

        return


def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


run()

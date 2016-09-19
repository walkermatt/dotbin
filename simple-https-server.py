# taken from http://www.piware.de/2011/01/creating-an-https-server-in-python/
# generate server.pem with the following command:
#    openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
# change to the directory you want to serve and run as follows:
#    python simple-https-server.py
# then in your browser, visit:
#    https://localhost:4443
# to add the certificate to Chrome see:
#    http://stackoverflow.com/a/15076602/526860
import BaseHTTPServer
import SimpleHTTPServer
import ssl
import os

# Read the certificate from the same directory as the script
this_dir = os.path.dirname(os.path.realpath(__file__))
certfile = os.path.join(this_dir, 'server.pem')

httpd = BaseHTTPServer.HTTPServer(('localhost', 4443), SimpleHTTPServer.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(httpd.socket, certfile=certfile, server_side=True)
httpd.serve_forever()

#!/usr/bin/env python
import random
import socket
import time

s = socket.socket()         # Create a socket object
host = socket.getfqdn() # Get local machine name
port = random.randint(8000, 9999)
s.bind((host, port))        # Bind to the port

print 'Starting server on', host, port
print 'The Web server URL for this would be http://%s:%d/' % (host, port)

s.listen(5)                 # Now wait for client connection.

#     @MGB these comments didn't have a space after the #
# httpcode = '''<\HTTP/1.0 200 OK> \r\nContent-Type: text/html \r\n <html>
# \r\n<body> \r\n<h1>Hello World</h1> \r\n This is sarteleb's web server
# \r\n</body> \r\n</html>\r\n'''


print 'Entering infinite loop; hit CTRL-C to exit'
while True:
#    Establish connection with client.    

# @MGB these lines had 8 spaces instead of 4 which is apparently "standard"
    c, (client_host, client_port) = s.accept()
    print c.recv(1000)
    print 'Got connection from', client_host, client_port
    c.send('HTTP/1.0 200 OK\nContent-Type: text/html\n\n')
    c.send('<h1>Hello World!</h1> this is sarteleb\'s web server.')
    c.close()

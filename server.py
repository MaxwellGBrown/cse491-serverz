#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse, parse_qs

## for the new POST request handling
from StringIO import StringIO
import cgi

## for the templates
import jinja2
import os


##
## HANDLE CONNECTION DEFINITION
##
def handle_connection(conn):
    
    # Start reading in data from the connection
    read = conn.recv(1)
    while read[-4:] != '\r\n\r\n':
	read += conn.recv(1)
	
    if read[-4:] == '\r\n\r\n':
	print "READ IS DONE!"
	
    # Parse headers
    request, data = read.split('\r\n',1)
    print read

    headers = {}
    for line in data.split('\r\n')[:-2]:
	k, v = line.split(': ',1)
	headers[k.lower()] = v
	
    # Parse path and related info
    path = urlparse(request.split(' ', 3)[1])
    
    # corrospond requests to .html files
    response = {
		'/'		: 'index.html',		\
		'/content'	: 'content.html',	\
		'/file'		: 'file.html',		\
		'/image'	: 'image.html',		\
		'/form'		: 'form.html',		\
		'/submit'	: 'submit.html',	\
		}
    
    # setup and run jinja2 templates
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)
    response_header =	'HTTP/1.0 200 OK\r\n' + \
			'Content-type: text/html\r\n\r\n'
    content = ''
    
    # path[4] corrosponds to field=value, and parse_qs handles that
    values = parse_qs(path[4])
    
    if request.startswith('POST '):
	while len(content) < int(headers['content-length']):
	    content += conn.recv(1)
    
    environ = {'REQUEST_METHOD' : 'POST'}
    form = cgi.FieldStorage(fp=StringIO(content), headers=headers, environ=environ)
    
    print 'form made!'
    
    # add the newly found values into the parse_qs object
    new_values = {}
    for key in form.keys():
	new_values[key] = form[key].value

    values.update(new_values)
    
    print 'values updated!'
    
    # Try to connect to requested page
    if path[2] in response:
	template = env.get_template(response[path[2]])
    else:
	values['page'] = path[2]
	response_header = 'HTTP/1.0 404 Not Found\r\n\r\n'
	template = env.get_template('404.html')
    
    print 'tried '+path[2]
    
    # use jinja2's render to get the return string
    response_content = template.render(values)   
    
    # send response_header to client
    conn.send(response_header)
    # send response_content (aka, html) to client
    conn.send(response_content)
    
    print 'conn sent!'
    
    # close the connection
    conn.close()
    
    print 'conn closed!'
	




##
## MAIN FUNCTION DEFINITION
##

def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn()     # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port
    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)
    s.listen(5)                 # Now wait for client connection.
    print 'Entering infinite loop; hit CTRL-C to exit'
    
    while True:

        # Ctrl+C KeyboardInterrupt error handler
        try:
            # Establish connection with client.
            c, (client_host, client_port) = s.accept()
            print 'Got connection from', client_host, client_port
            # handle connection to serve page
            handle_connection(c)

            
        except (KeyboardInterrupt):
            print "\r\nEnding server.py ...\r\n"
            exit(0)



##
## RUN MAIN
##

if __name__ == '__main__':
    main()

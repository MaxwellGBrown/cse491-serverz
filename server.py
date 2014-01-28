#!/usr/bin/env python
import random
import socket
import time
import urlparse


# Define these global variables, because
host = str()
port = int()
    
def main():
    s = socket.socket()         # Create a socket object

    global host
    host = socket.getfqdn() # Get local machine name
    global port
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
## THESE FUNCTIONS RETURN PAGE HTML CONTENT 
##

            
def index(values):
    return_str = '<h1>Hello, world.</h1>' + \
                 'This is MaxwellGBrown\'s Web server.' + \
                 '<ul>' + \
                 '<li><a href="/content">content</a></li>' + \
                 '<li><a href="/file">file</a></li>' + \
                 '<li><a href="/image">image</a></li>' + \
                 '<li><a href="/form">form</a></li>' + \
                 '</ul>'
    return return_str


def files(values):
    return_str = '<h1>Hello, world.</h1>' + \
                 'This is MaxwellGBrown\'s Web server.' + \
                 '<h2>File</h2>'
    return return_str


def image(values):
    return_str = '<h1>Hello, world.</h1>' + \
                 'This is MaxwellGBrown\'s Web server.' + \
                 '<h2>Image</h2>'
    return return_str


def content(values):
    return_str = '<h1>Hello, world.</h1>' + \
                 'This is MaxwellGBrown\'s Web server.' + \
                 '<h2>Content</h2>'
    return return_str

def form(values):
    return_str = '<h1>Hello, world.</h1>' + \
                 'This is MaxwellGBrown\'s Web server.' + \
                 '<h2>Form</h2>' +\
                 "<form action='/submit' method='POST'>" + \
                 "<input type='text' name='firstname'>" + \
                 "<input type='text' name='lastname'>" + \
                 "<input type='submit' value='Submit'>" + \
                 "</form>"
    return return_str

def submit(values):
    
    names = values
        
##    names = (values.rsplit('&')[0].rsplit('=')[1],\
##             values.rsplit('&')[1].rsplit('=')[1])
    
    return_str = '<h1>Hello, %s ' %(names["firstname"]) + \
                 '%s.</h1>' % (names["lastname"]) + \
                 'This is MaxwellGBrown\'s Web server.' + \
                 '<h2>Submit</h2>'
                 
    return return_str





##
## A function that parses the values from a URL field as a dict
##
def split_values(values):
    '''Takes values from URL and returns a dict with field:value qualities'''
    return_dict = dict()

    if values == '': return return_dict # handle no value error case
    
    for item in values.rsplit('&'):
        return_dict[item.rsplit('=')[0]] = item.rsplit('=')[1]

    return return_dict







##
## Parses connection object for path and refers it to correct function
##
def handle_connection(conn):
    
    ## handle request data
    request_data = conn.recv(1000)
    print request_data
    request_type = request_data.splitlines()[0].rsplit(' ')[0] # prints the page requested (1st line, 1st word)
    page_request = request_data.splitlines()[0].rsplit(' ')[1] # prints the page requested (1st line, 2nd word)

    print request_type + ' ' + page_request


    ## create a full url string for url parse
    url = "http://%s:%s%s" % (host, port, page_request)
##    print "URL: %s" % (url)

    parsed_url = urlparse.urlparse(url)

    
    ## initialize html_text
    html_text = str()

    ## set http_response
    ## don't send the http_response just yet, incase page doesn't exist
    http_response =  'HTTP/1.0 200 OK\r\n'
    content_type = 'Content-type: text/html\r\n'



    ## handle different types of HTML requests
    if request_type == "GET":
        ## serve HTML content

        ## Split the values passed in the url as dict to pass
        values = split_values(parsed_url.query)

        
        if parsed_url.path == '/':
            ## cse.msu.edu:xxxx/
            html_text = index(values)
            
        elif parsed_url.path == '/content':
            ## cse.msu.edu:xxxx/content
            html_text = content(values)
            
        elif parsed_url.path == '/file':
            ## cse.msu.edu:xxxx/file
            html_text = files(values)
            
        elif parsed_url.path == '/image':
            ## cse.msu.edu:xxxx/image
            html_text = image(values)

        elif parsed_url.path == '/form':
            ## cse.msu.edu:xxxx/form
            html_text = form(values)

        elif parsed_url.path == '/submit':
            ## cse.msu.edu:xxxx/submit?firstname=value1&lastname=value2
            ## only with GET
            
            html_text = submit(values)


    elif request_type == "POST":
        ## POST request handler

        ## Split the values passed in the HTML request as dict to pass
        values = split_values(request_data.splitlines()[-1])
        
        if parsed_url.path == '/submit':
            ## cse.msu.edu:xxxx/submit
            ## with POST
            html_text = submit(values)
            
        else:
            html_text = '<h1>Hello, world.</h1>' + \
                        'MaxwellGBrown\'s POST request HTML.'



    
    ## send http response and content
    conn.send(http_response)
    conn.send(content_type)
    conn.send('\r\n')
    conn.send(html_text)
    conn.close()






##
## RUN MAIN
##

if __name__ == '__main__':
    main()

## for parsing path and query string
from urlparse import urlparse, parse_qs

## for the templates
import jinja2
import os



def simple_app(environ, start_response):
  
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
    jinja2_environment = jinja2.Environment(loader=loader)
    
    
    # if any values are stored in the URL, this will get them
    values = parse_qs(environ['QUERY_STRING'])
    # initialize empty dictionary for POST requests that can be updated
    # with the contents of the awful cgi thing
    new_values = {}
    if environ['REQUEST_METHOD'] is 'POST':
      
	print "environ['wsgi.input'].keys()"
	print environ['wsgi.input'].keys()
	
	for key in environ['wsgi.input'].keys():
	    new_values[key] = environ['wsgi.input'][key].value
	    print "%s = %s \r\n" % (key, new_values[key])
	
	values.update(new_values)
	print 'values updated!' 
    
    
    # Try to connect to requested page
    if environ['PATH_INFO'] in response:
	response_status =	'200 OK'
	template = jinja2_environment.get_template(response[environ['PATH_INFO']])
    else:
	values['page'] = environ['PATH_INFO']
	response_status = '404 Not Found'
	template = jinja2_environment.get_template('404.html')
  
    # set response_headers to text/html since that's all we've got for now
    response_headers = [('Content-type', 'text/html')]
    
    print 'tried '+ environ['PATH_INFO']
    
    
    # start_response before building from template
    # does the app.send() for the status and headers
    start_response(response_status, response_headers)
    
    # use jinja2's render to get the return string
    response_content = template.render(values).encode('latin-1', 'replace')
    
    # return a string which will be sent in the handle connection function
    return response_content
    
    
    
# still needed?
def make_app():
    return simple_app
    
    
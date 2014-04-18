import quixote
from quixote.directory import Directory, export, subdir

from . import html, image

import sqlite3, sys


class RootDirectory(Directory):
    _q_exports = []

    @export(name='')                    # this makes it public.
    def index(self):
        print "User: %s"%(quixote.get_cookie('User') )
        return html.render('index.html')
        
    @export(name='login')
    def login(self):
        return html.render('login.html')
        
    @export(name='do_login')
    def do_login(self):
        request = quixote.get_request()
        print "User: %s Password: %s\n\n"%(request.form['username'], request.form['password'])
        
        conn = sqlite3.connect('MBimageapp.db')
	c = conn.cursor()
	
	#change to standard text before reading
	conn.text_factory = str
	
	t = (request.form['username'], request.form['password'])
	for row in c.execute('SELECT * FROM imageapp1 WHERE username=? AND password=?', t):
	    if (row[0] == request.form['username']) & (row[1] == request.form['password']):
	        request.response.set_cookie('User', row[0])
	        # close connection
	        conn.close()
	        return "<p>Login successful! :) <a href='/'> return to index</a></p>"
	    
	# close connection
	conn.close()
	
	#return unsuccessful
	return "<p>Login unsuccessful! :( <a href='/'> return to index</a></p>"

        
        
    @export(name='register')
    def register(self):
        request = quixote.get_request()
        if request.form['password'] == request.form['confirm']:
	    conn = sqlite3.connect('MBimageapp.db')
	    c = conn.cursor()
	    
	    #change to standard text before reading
	    conn.text_factory = str
	    
	    s = "INSERT INTO imageapp1 VALUES ('%s','%s', 'NULL')" % (request.form['username'], request.form['password'])
	    c.execute(s)
	    
	    conn.commit()
	    conn.close()
	     
	    # set the new account as the cookie
	    request.response.set_cookie('User', request.form['username'])

	    return "<p>Account successfully created!<a href='/'> return to index</a></p>"
	else:
	    # return failure
	    return "<p>Account creation was unsucessful :( <a href='/'> return to index</a></p>"
	    
    @export(name='list')
    def list(self):
        html.get_template('list.html')
        values = get_all_images()
        
        
    @export(name='logout')    
    def logout(self):
        quixote.get_response().expire_cookie('User', path='/')
        return quixote.redirect("/")

    @export(name='upload')
    def upload(self):
        return html.render('upload.html')

    @export(name='upload_receive')
    def upload_receive(self):
        request = quixote.get_request()
        # print request.form.keys()

        the_file = request.form['file']
        # print dir(the_file)
        # print 'received file with name:', the_file.base_filename
        data = the_file.read(int(1e9))
        
#        image.add_image(data)
        image.add_image(data, quixote.get_cookie("User") )
        
        return quixote.redirect('/') # redirects to index
        
        
    @export(name='image')
    def image(self):
        return html.render('image.html')
    
    
    
    # returns stylesheet when requested
    @export(name='style.css')
    def style(self):
        request = quixote.get_request()
        request.response.set_content_type("text/css")
        #return html.render('Flan/style.css')
      
	file_obj = open("./imageapp/Flan/style.css", "rb")
	data = file_obj.read();
	file_obj.close()
        return data

        
        
    @export(name='image_raw')
    def image_raw(self):
        response = quixote.get_response()
        
        # added for user tracking
        user = quixote.get_cookie("User")
        
        response.set_content_type('image/png')
        
        # img = image.get_latest_image()
        img = image.get_image(user)
        
        return img

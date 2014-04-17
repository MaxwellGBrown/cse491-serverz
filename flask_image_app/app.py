import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
                  render_template, flash
    

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flask-imageapp.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
    ))
# Set FLASK-IMAGEAPP_SETTINGS as a variable to the file path for the
# settings, if you wish. silent means if there is none it wont explode
app.config.from_envvar('FLASK_IMAGEAPP_SETTINGS', silent=True)

def make_app():    
    return app
    

    
    
    
    
    
    
    
@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, image from flask_images order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)
    
@app.route('/image/<int:image_id>')
def get_image(image_id):
    db = get_db()
    cur = db.execute('select image from flask_images where id=?', (image_id,) )
    conn.text_factory = bytes
    # .fetchone() returns a tuple object. The image is in the first index of it.
    img = c.fetchone()[0]
    
    response.set_content_type('image/png')    
    return img
    
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    
    # change the data from image into a picture... or something
    the_file = request.form['image']
    image = the_file.read(int(1e9))
    
    title = request.form['title']
    title = title.encode('latin-1', 'replace')
    
    db = get_db()
    db.text_factory = bytes
    db.execute('insert into flask_images (title,image) values (?,?)',
                   [request.form['title'], image ])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries') )
    
@app.route('/login', methods=['GET', 'POST'] )
def login():
    error = None
    if request.method == "POST":
        if request.form['username'] != app.config['USERNAME']:
	    error = 'Invalid username'
	elif request.form['password'] != app.config['PASSWORD']:
	    error = "Invalid password"
	else:
	    session['logged_in'] = True
	    flash('You were logged in')
	    return redirect(url_for("show_entries") )
    return render_template('login.html', error=error)
    
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries') )
    
    
    
    
    
    
    
    
	
	
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
    
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    '''Closes the database again at the end of the request. '''
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
        
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
	    db.cursor().executescript(f.read())
	db.commit()

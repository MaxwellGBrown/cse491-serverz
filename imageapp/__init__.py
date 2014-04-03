# __init__.py is the top level file in a Python package.

from quixote.publish import Publisher

# this imports the class RootDirectory from the file 'root.py'
from .root import RootDirectory
from . import html, image

import sqlite3

def create_publisher():
     p = Publisher(RootDirectory(), display_exceptions='plain')
     p.is_thread_safe = True
     return p
 
def setup():                            # stuff that should be run once.
    html.init_templates()

    ##try:
	##db = sqlite3.connect('images.sqlite')
	##db.execute('CREATE TABLE image_users ( username TEXT, password TEXT)');
	##db.commit()
	##db.close()
	##print "new table made\n"
    ##except sqlite3.OperationalError:
        ##print "user table already exists\n"
        ##pass
      
    ##try:
	##db = sqlite3.connect('images.sqlite')
	##db.execute('CREATE TABLE image_pic ( username TEXT, image BLOB)');
	##db.commit()
	##db.close()
	##print "new pic table made\n"
    ##except sqlite3.OperationalError:
        ##print "pic table already exists\n"
        ##pass
        
        
    some_data = open('imageapp/dice.png', 'rb').read()
#    image.add_image(some_data)
    # Added "None" User for default cookie when nobody is logged in
    image.add_image(some_data, None)

def teardown():                         # stuff that should be run once.
    pass

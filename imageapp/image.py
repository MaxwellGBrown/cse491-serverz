# image handling API
import sqlite3

def add_image(data, user):
  
    conn = sqlite3.connect('MBimageapp.db')
    c = conn.cursor()
    
    # do this so images can work and stuff
    conn.text_factory = bytes
    
    t = (data, user)
    c.execute("UPDATE imageapp1 SET picture=? WHERE username=?", t)
    
    conn.commit()
    conn.close()
    
#def get_image(num):
#    return images[num]

def get_image(user):
  
    conn = sqlite3.connect('MBimageapp.db')
    c = conn.cursor()
    
    # do this so images can work and stuff
    conn.text_factory = str
    
    t = (user,)
    c.execute('SELECT picture FROM imageapp1 WHERE username=?', t )
    
    conn.text_factory = bytes
    
    # .fetchone() returns a tuple object. The image is in the first index of it.
    image = c.fetchone()[0]
    
    
    
    # finish sql queury	    
    conn.close()
    
    return image

def get_latest_image():
    image_num = max(images.keys())
    return images[image_num]

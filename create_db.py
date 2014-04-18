import sqlite3

# create new db and make connection
conn = sqlite3.connect('MBimageapp.db')    
c = conn.cursor()

# create table
c.execute('''CREATE TABLE imageapp1
             (username TEXT, password TEXT, picture BLOB)''')

# commit changes
conn.commit()

# close connection
conn.close()

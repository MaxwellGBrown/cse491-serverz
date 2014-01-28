import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

# Test a basic GET call.

def test_handle_connection_index():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Hello, world.</h1>' + \
                      'This is MaxwellGBrown\'s Web server.' + \
                      '<ul>' + \
                      '<li><a href="/content">content</a></li>' + \
                      '<li><a href="/file">file</a></li>' + \
                      '<li><a href="/image">image</a></li>' + \
                      '<li><a href="/form">form</a></li>' + \
                      '</ul>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)


def test_handle_connection_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Hello, world.</h1>' + \
                      'This is MaxwellGBrown\'s Web server.' + \
                      '<h2>File</h2>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Hello, world.</h1>' + \
                      'This is MaxwellGBrown\'s Web server.' + \
                      '<h2>Content</h2>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Hello, world.</h1>' + \
                      'This is MaxwellGBrown\'s Web server.' + \
                      '<h2>Image</h2>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)                              

def test_handle_connection_form():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                          'Content-type: text/html\r\n' + \
                          '\r\n' + \
                          '<h1>Hello, world.</h1>' + \
                          'This is MaxwellGBrown\'s Web server.' + \
                          '<h2>Form</h2>' +\
                          "<form action='/submit' method='POST'>" + \
                          "<input type='text' name='firstname'>" + \
                          "<input type='text' name='lastname'>" + \
                          "<input type='submit' value='Submit'>" + \
                          "</form>"

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_submit_GET():
    firstname = "John"
    lastname = "Smith"
    conn = FakeConnection("GET /submit?firstname=%s" % (firstname) + \
                          "&lastname=%s HTTP/1.0\r\n\r\n" % (lastname) )
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                          'Content-type: text/html\r\n' + \
                          '\r\n' + \
                          '<h1>Hello, %s %s.</h1>' % (firstname, lastname) + \
                          'This is MaxwellGBrown\'s Web server.' + \
                          '<h2>Submit</h2>'
                          

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_submit_POST():
    firstname = "John"
    lastname = "Smith"
    conn = FakeConnection("POST /submit HTTP/1.0\r\n" + \
                          "firstname=%s&lastname=%s\r\n" % (firstname,lastname))
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                          'Content-type: text/html\r\n' + \
                          '\r\n' + \
                          '<h1>Hello, %s %s.</h1>' % (firstname, lastname) + \
                          'This is MaxwellGBrown\'s Web server.' + \
                          '<h2>Submit</h2>'
                          

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_POST():
    conn = FakeConnection("POST / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                          'Content-type: text/html\r\n' + \
                          '\r\n' + \
                          '<h1>Hello, world.</h1>' + \
                          'MaxwellGBrown\'s POST request HTML.'
    
    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

    

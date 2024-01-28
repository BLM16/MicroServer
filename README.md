# MicroServer
[![PyPI](https://img.shields.io/pypi/v/BLM16-MicroServer?style=flat&logo=PyPi&logoColor=yellow&label=PyPi&color=blue)](https://pypi.python.org/pypi/BLM16-MicroServer)

MicroServer is a lightweight Python webserver with minimal overhead and no external dependencies
MicroServer provides complete flexibility by leaving all data processing and templating to the user.

```py
from microserver import MicroServer, Response, request

server = MicroServer()

# Configures the route / to be handled by the home function.
@server.route('/')
def home():
    data = server.load_view('index.html')
    mime = 'text/html'
    return Response(data, mime)

@server.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return Response(server.load_view('login.html'), 'text/html')
    else:
        username = request.form['username'].value
        password = request.form['password'].value
        # ...
        return Response.redirect('/', status=303)

# Configures all 404 errors to be handled by the e404 function.
@server.errorhandler(404)
def e404():
    data = server.load_view('404.html')
    mime = 'text/html'
    return Response(data, mime)

# Starts the server on the given host and port.
server.start('localhost', 8080)
```

## Installation

MicroServer can be installed using `pip` with the package name `BLM16-MicroServer`.
```sh
pip3 install -U BLM16-MicroServer
```

MicroServer releases can also be installed from the GitHub [releases](https://github.com/BLM16/MicroServer/releases) (as .tar.gz or a wheel) along with the signing artifacts.

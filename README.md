# MicroServer

MicroServer is a lightweight Python webserver with minimal overhead and no external dependencies
MicroServer provides complete flexibility by leaving all data processing and templating to the user.

```py
from microserver import MicroServer, Response

server = MicroServer()

# Configures the route / to be handled by the home function.
@server.route('/')
def home():
    data = server.load_view('index.html')
    mime = 'text/html'
    return Response(data, mime)

# Configures all 404 errors to be handled by the e404 function.
@server.errorhandler(404)
def e404():
    data = server.load_view('404.html')
    mime = 'text/html'
    return Response(data, mime)

# Starts the server on the given host and port.
server.start('localhost', 8080)
```

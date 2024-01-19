from microserver import MicroServer, Response

HOST = 'localhost'
PORT = 8080

server = MicroServer()

# Configures the route / to be handled by the home function.
# Returns a Response with the contents of views/index.html.
@server.route('/')
def home():
    data = server.load_view('index.html')
    mime = 'text/html'
    return Response(data, mime)

# Configures all 404 errors to be handled by the e404 function.
# Returns a Response with the contents of view/404.html.
@server.errorhandler(404)
def e404():
    data = server.load_view('404.html')
    mime = 'text/html'
    return Response(data, mime)

# Starts the server on the given host and port.
server.start(HOST, PORT)

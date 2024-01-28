from microserver import MicroServer, Response

from routes import routes

HOST = 'localhost'
PORT = 8080

server = MicroServer()

# Register all the routes from the routes blueprint
server.register_blueprint(routes)

# Configures all 404 errors to be handled by the e404 function
@server.errorhandler(404)
def e404():
    data = server.load_view('404.html')
    return Response(data, 'text/html')

server.start(HOST, PORT)

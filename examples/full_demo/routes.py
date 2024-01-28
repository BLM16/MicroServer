from microserver import Blueprint, Response, request
import pybars

import auth
from models.user import User

routes = Blueprint()

COMPILER = pybars.Compiler()
PARTIALS = {
    'header': COMPILER.compile(routes.load_view('partials/header.hbs'))
}

@routes.route('/')
def home():
    source = routes.load_view('index.hbs')
    template = COMPILER.compile(source)
    data = template({ 'user': auth.get_user_from_session_cookie(request.cookies.get('session_id')) }, partials=PARTIALS)

    return Response(data, 'text/html')

@routes.route('/profile')
def profile():
    user = auth.get_user_from_session_cookie(request.cookies.get('session_id'))
    if not user:
        return Response.for_status(401) # Unauthorized

    source = routes.load_view('profile.hbs')
    template = COMPILER.compile(source)
    data = template({ 'user': user }, partials=PARTIALS)

    return Response(data, 'text/html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        source = routes.load_view('login.hbs')
        template = COMPILER.compile(source)
        data = template({ 'user': auth.get_user_from_session_cookie(request.cookies.get('session_id')) }, partials=PARTIALS)

        return Response(data, 'text/html')
    
    if 'username' not in request.form or 'password' not in request.form:
        return Response.for_status(422) # Unprocessable content
    
    username = request.form['username'].value
    password = request.form['password'].value

    if not username in auth.users:
        return Response.for_status(401) # Unauthorized
    
    user = auth.users[username]
    if password != user.password:
        return Response.for_status(401) # Unauthorized
    
    guid = auth.new_guid()
    auth.sessions[guid] = user

    res = Response.redirect('/', status=303) # See other (redirecting away from login page)
    res.add_cookie('session_id', guid)
    return res

@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        source = routes.load_view('register.hbs')
        template = COMPILER.compile(source)
        data = template({ 'user': auth.get_user_from_session_cookie(request.cookies.get('session_id')) }, partials=PARTIALS)

        return Response(data, 'text/html')
    
    if 'username' not in request.form or 'password' not in request.form:
        return Response.for_status(422) # Unprocessable content
    
    username = request.form['username'].value
    password = request.form['password'].value

    user = User(username, password)
    guid = auth.new_guid()

    auth.users[username] = user
    auth.sessions[guid] = user

    res = Response.redirect('/', status=303) # See other (redirecting away from register page)
    res.add_cookie('session_id', guid)
    return res

@routes.route('/logout')
def logout():
    session_id = request.cookies.get('session_id')
    if not session_id or not auth.get_user_from_session_cookie(session_id):
        return Response.for_status(204) # No content (user wasn't logged in, so no change)

    auth.sessions.pop(session_id.value, None)
    return Response.redirect('/login', status=302) # See other (redirecting to login because access lost1)

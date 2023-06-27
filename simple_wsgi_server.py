from wsgiref.simple_server import make_server
from urllib.parse import parse_qs

PORT = 8000

'''
TODO:   app itself, auth middleware, logger middleware, args
https://www.fullstackpython.com/wsgi-servers.html
'''


def simple_app(environ, start_response):
    user, status = auth_middleware(environ)
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    response = status
    if user:
        response = f'Hy {user["user"]}!'
    start_response(status, headers)
    return [response.encode()]


def auth_middleware(environ):
    query = parse_qs(environ['QUERY_STRING'])
    user = query.get('user')
    if user:
        return {'user': user[0]}, '200 OK'
    return [], '401 Unauthorized'


with make_server('', PORT, simple_app) as httpd:
    print(f'Serving at port {PORT}...')
    httpd.serve_forever()

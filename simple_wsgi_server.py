from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
import argparse

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Specify some parameters.')
    parser.add_argument('-p', '--port', type=int, default=8000, required=False, help='Specify server port.')
    d = vars(parser.parse_args())
    with make_server('', d['port'], simple_app) as httpd:
        print(f'Serving at port {d["port"]}...')
        httpd.serve_forever()

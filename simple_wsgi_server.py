from wsgiref.simple_server import make_server

PORT = 8000

'''
TODO:   app itself, auth middleware, logger middleware, args

'''


def simple_app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, headers)
    return [b'Hello from wsgi-app.']


with make_server('', PORT, simple_app) as httpd:
    print(f'Serving at port {PORT}...')
    httpd.serve_forever()
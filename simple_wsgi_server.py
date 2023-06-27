from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
import argparse
import logging

'''
https://www.fullstackpython.com/wsgi-servers.html
'''


def simple_app(environ, start_response):
    user, status = auth_middleware(environ)
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    response = status
    if user:
        response = f'Hy {user["user"]}!'

    logging_middleware(environ, user)
    start_response(status, headers)
    return [response.encode()]


def auth_middleware(environ):
    query = parse_qs(environ['QUERY_STRING'])
    user = query.get('user')
    if user:
        return {'user': user[0]}, '200 OK'
    return [], '401 Unauthorized'


def logging_middleware(environ, user):
    if not user:
        msg = f'''
        Someone tried to access website...
        ---DATA ABOUT HIM---
        HTTP_USER_AGENT: {environ.get("HTTP_USER_AGENT")}
        HTTP_REFERER: {environ.get("HTTP_REFERER")}
        HTTP_SEC_CH_UA: {environ.get("HTTP_SEC_CH_UA")}
        --------------------'''
        logging.warning(msg)
    else:
        msg = f"User '{user['user']}' access website."
        logging.info(msg)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Specify some parameters.')
    parser.add_argument('-p', '--port', type=int, default=8000, required=False, help='Specify server port. '
                                                                                     'Default: 8000')
    d = vars(parser.parse_args())

    logging.basicConfig(level=logging.INFO, filename='wsgi_log.log', format="%(asctime)s %(levelname)s %(message)s")

    with make_server('', d['port'], simple_app) as httpd:
        logging.info(f'Start serving at port {d["port"]}')
        print(f'Serving at port {d["port"]}...')
        httpd.serve_forever()

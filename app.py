# -*- encoding: utf-8 -*-

import os
from gevent import monkey
monkey.patch_all()

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

from src import create_app

app = create_app()
app_name = app.config['APPNAME'].upper()

if __name__ == '__main__':
    SERVER_NAME = app.config['COMPUTER_NAME']
    SERVER_IP = app.config['COMPUTER_IP']
    ROUTE_IP = SERVER_IP
    SERVER_PORT = 6004

    firstevent = 1
    SERVER_PORT = os.environ.get(f"{app_name}_PORT", SERVER_PORT)

    if type(SERVER_PORT) == str:
        SERVER_PORT = int(SERVER_PORT)

    print('app name => ', app_name)
    print(SERVER_NAME, f'em http://{ROUTE_IP}:{SERVER_PORT}')
    for i, bp in enumerate(app.config['BLUEPRINTS']):
        _SERVER_NAME = SERVER_NAME if i == -1 else ' ' * len(SERVER_NAME)
        status = ('/' if bp["url_prefix"] != '/' else '') + 'status'
        print(_SERVER_NAME, f'em http://{ROUTE_IP}:{SERVER_PORT}{bp["url_prefix"]}{status}')
        if bp["url_prefix"] == '/ws':
            print(_SERVER_NAME, f'     ws://{ROUTE_IP}:{SERVER_PORT}{bp["url_prefix"]}')

    print('\n')

    server = WSGIServer((SERVER_IP, SERVER_PORT), app, handler_class=WebSocketHandler)
    server.serve_forever()

from flask import request, current_app
from . import blueprint
from .. import sockets
from .realtime import ServerHandle


@sockets.route('/auth')
def websocket(ws):
    server = ServerHandle(ws, request.path)
    server.register()


@blueprint.route('/status')
def status():
    NICK_NAMES = current_app.config['NICK_NAMES']
    CONNECTIONS = current_app.config['CONNECTIONS']
    if NICK_NAMES or CONNECTIONS:
        usuarios = f' e numero de NICK_NAMES = {len(NICK_NAMES)}, CONNECTIONS = {len(CONNECTIONS)}'
    else:
        usuarios = ''

    return f'<h1>Servidor ({blueprint.name}) ativo!{usuarios}</h1>'

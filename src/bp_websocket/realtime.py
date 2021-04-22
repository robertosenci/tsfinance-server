import os
import uuid
import json
import logging
from flask import current_app


def obter_conn(token, context):
    NICK_NAMES = context['NICK_NAMES'] if context else current_app.config['NICK_NAMES']
    CONNECTIONS = context['CONNECTIONS'] if context else current_app.config['CONNECTIONS']
    _token_nick = NICK_NAMES.get(token, None)
    if _token_nick:
       token = _token_nick['token']
    conn = CONNECTIONS.get(token, None)
    return conn


def enviar_mensagem(message=None, token=None, context=None):
    CONNECTIONS = context['CONNECTIONS'] if context else current_app.config['CONNECTIONS']
    if message:
        if token:
            user = obter_conn(token, context)
            if user:
                user.send(message)
        else:
            for token, user in CONNECTIONS.items():
                user.send(message)


class ConnectionHandle:
    def __init__(self):
        self.ws = None
        self.nickname = None
        self.uri = None
        self.token = None
        self.state = "Disconnect"
        self.key = None
        self.server = None
        self.NICK_NAMES = None

    def secret(self):
        key = f'{uuid.uuid4().hex}'
        self.key = key[:20] + '.' + key[20:]

        server = f'{uuid.uuid4().int}'
        server = server[:16]
        server = server[:5] + '.' + server[5:]
        self.server = server[:14] + '-' + server[14:]

    @staticmethod
    def users_event():
        CONNECTIONS = current_app.config['CONNECTIONS']
        return {"type": "users", "count": len(CONNECTIONS)}

    def user_excluir_connection(self):
        CONNECTIONS = current_app.config['CONNECTIONS']
        NICK_NAMES = self.NICK_NAMES
        if self.token in CONNECTIONS:
            del(CONNECTIONS[self.token])
        try:
            if self.nickname in NICK_NAMES:
                del(NICK_NAMES[self.nickname])
        except:
            pass

    def notify_users(self, message=None):
        CONNECTIONS = current_app.config['CONNECTIONS']
        if CONNECTIONS:
            if not message: message = self.users_event()
            for token, user in CONNECTIONS.items():
                user.send(message)

    def notify_user(self, message=None, token=None):
        CONNECTIONS = current_app.config['CONNECTIONS']
        if CONNECTIONS:
            if not message:
                message = self.users_event()
            if token is None:
                token = self.token
            user = CONNECTIONS.get(token, None)
            if user:
                user.send(message)

    def trata_message(self, data):
        from .trata_mensagem import trata_mensagem
        trata_mensagem(self, data)

    def welcome(self) -> bool:
        from .welcome import welcome
        return welcome(self)


class ServerHandle(ConnectionHandle):
    def __init__(self, ws, path):
        self.ws = ws
        self.path = path
        self.timeout = 1
        self.NICK_NAMES = current_app.config['NICK_NAMES']

    def register(self):
        CONNECTIONS = current_app.config['CONNECTIONS']
        NICK_NAMES = self.NICK_NAMES
        connection = self
        connection.token = f'{uuid.uuid4()}'
        if connection.welcome():
            CONNECTIONS[connection.token] = connection
            NICK_NAMES[connection.nickname] = {'token': connection.token}
            connection.listener()

    def unregister(self):
        nickname = None
        try:
            nickname = self.nickname
        except Exception as e:
            error = f'Erro: nickname = {e}'
            logging.error(error)
        if nickname:
            print(f'Unregister connection from {nickname}')
            self.close()
            try:
                self.user_excluir_connection()
            except Exception as e:
                error = f'Erro: user_excluir_connection = {e}'
                logging.error(error)

    def close(self):
        self.state = 'Disconnected'
        try:
            self.ws.close()
        except Exception as e:
            error = f'Erro: Disconnected = {e}'
            logging.error(error)

    def listener(self):
        try:
            while not self.ws.closed:
                message = self.recv()
                if message:
                    self.trata_message(message)
                else:
                    self.unregister()

        except Exception as e:
            print(f'Error: ={e}')
            self.unregister()

    def send(self, message):
        connection = self.ws
        data = json.dumps(message)
        # print(f'mensagem send => {message}')
        try:
            connection.send(data)
        except Exception as e:
            print(f'Error enviar mensagem: ={e}')

    def recv(self, timeout=None):
        try:
            if timeout:
                import gevent
                message = gevent.with_timeout(self.timeout, self.ws.receive, timeout_value=None)
            else:
                message = self.ws.receive()
            if message:
                # print(f'mensagem receive <= {message}')
                try:
                    data = json.loads(message)
                except Exception as e:
                    print('erro convertendo mensagem para json')
                    raise
                return data
            return None

        except Exception as e:
            error = f'Erro websocket.recv() = {e}'
            logging.error(error)
            return None

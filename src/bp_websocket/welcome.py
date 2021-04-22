# funcoes do projeto
from .ws_utils import decript


def welcome(self) -> bool:
    """ inicia a autenticacao"""
    # print(f'inicia a autenticacao para a path {self.path} com o index')
    if self.path == '/auth':
        self.nickname = self.token
        self.state = 'Connected'
        from datetime import datetime
        now = datetime.now()
        print(now, f'New connection from {self.nickname}, with token {self.token}')
        return True
    return False

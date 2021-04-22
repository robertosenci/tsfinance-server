import logging

from src.bp_authserver.routes import license


def trata_mensagem(self, data):
    print(data)
    data['token'] = self.token
    if data.get('action'):
        if data["action"] == "LOGIN":
            register(self, license(data))
        if data["action"] == "NETCLI":
            set_netcli(self, data=data)

    else:
        error = f"unsupported event: {data}"
        logging.error(error)


def register(self, result):
    if result.get('command') == 'LIC_ADDED':
        dados = {'token': self.token}
        self.nickname = f"P{result.get('solicitation')}"
        self.NICK_NAMES[self.nickname] = dados
        del self.NICK_NAMES[self.token]
    elif result.get('command') == 'LIC_LOGGED' or result.get('command') == 'LIC_BLOCKED':
        dados = {'token': self.token, 'licenca': f"{result.get('licenca')}"}
        self.nickname = f"{result.get('licenca')}"
        self.NICK_NAMES[self.nickname] = dados
        del self.NICK_NAMES[self.token]
    self.notify_user(message=result)


def set_netcli(self, data):
    self.NICK_NAMES[self.nickname]['netcli'] = data.get('status')

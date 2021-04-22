import datetime
import jwt
from flask import jsonify, current_app
from src.v1_user.dbuser import UserDAO


class User:
    def __init__(self):
        pass

    def insert(self, user):
        dao = UserDAO()
        if user:
            if dao.get_by_cpf(cpf=user.get('cpf')):
                return jsonify(dict(result="error", message="Este CPF já está cadastrado")), 400
            if dao.get_by_email(email=user.get('email')):
                return jsonify(dict(result="error", message="Este email já está cadastrado")), 400
            if dao.insert(user=user):
                return jsonify(dict(result="sucess")), 201
        return jsonify(dict(result="error", message="Dados de usuário não informado")), 400

    def update(self, user):
        if user:
            if UserDAO().update(user=user):
                return jsonify(dict(result="sucess")), 201
        return jsonify(dict(result="error", message="Dados de usuário não informado")), 400

    def delete(self, codigo):
        if UserDAO().delete(codigo=codigo):
            return jsonify(dict(result="sucess")), 200
        return jsonify(dict(result="error", message="Falha ao excluir usuário")), 400

    def active(self, active, codigo):
        pass

    def login(self, user):
        if user:
            rs = UserDAO().get_by_email(user.get('email'))
            if not rs:
                return jsonify(dict(result="error", message="Usuário não cadastrado.")), 400
            else:
                current_user = rs[0]
                if current_user.get("senha") != user.get("password"):
                    return jsonify(dict(result="error", message="Senha inválida.")), 400
            token = self.auth_token(usuario=user.get('email'))
            token_refresh = self.auth_refresh(usuario=user.get('email'), token=token)
            current_user['senha'] = 'PASSWORD'
            return jsonify({
                "result": "success",
                "user": current_user,
                "token": token,
                "refresh-token": token_refresh
            }), 200
        return jsonify(dict(result="error", message="Dados de login não informado.")), 400

    def get_user(self, id_user):
        pass

    def get_by_email(self, email):
        rs = UserDAO().get_by_email(email=email)
        if rs:
            user = rs[0]
            user['password'] = "password"
            return jsonify(rs), 200
        else:
            return jsonify(dict(result="error")), 400

    def verifica_permissao(self, email):
        user = UserDAO().get_by_email(email=email)
        if not user:
            return jsonify(dict(result="error", message="Usuário inválido.")), 400
        if not user[0]['active'] == 1:
            return jsonify(dict(result="error", message="Usuário bloqueado.")), 400
        if not user[0]['office'] in ('1', '2'):
            return jsonify(dict(result="error", message="Usuário não possui permissão para esta ação.")), 400
        return None

    def auth_token(self, usuario):
        payload = {
            "id": usuario,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")
        return token.decode('UTF-8')

    def auth_refresh(self, usuario, token):
        payload = {
            "id": usuario,
            "token": token,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30)
        }
        token = jwt.encode(payload, current_app.config['SECRET_KEY'])
        return token.decode('UTF-8')

    def refresh_token(self, params):
        xtoken = str(params.get('refresh-token')).replace("Bearer", "").strip()
        try:
            decode = jwt.decode(xtoken, current_app.config['SECRET_KEY'], algorithm="HS256")
            print(decode)
        except Exception as e:
            if f"Signature has expired" == f'{e}':
                return jsonify({"message": f'{e}', "auth": "Authorization"}), 403
            return jsonify({"message": "Refresh-Token inválido", "auth": "Authorization"}), 401

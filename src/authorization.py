import json
import socket
import inspect
import jwt
from flask import jsonify, request, current_app
from functools import wraps

from src.v1_user.user import User


def authorization_key(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        reader = request.headers
        print(reader)
        if not request.headers.get("Api-Key") == current_app.config['APP_KEY']:
            return jsonify({"message": "Falha de autenticação", "auth": "App-Key"}), 401,
        return f(*args, **kwargs)
    return wrap


def authorization_jwt(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        token = request.headers.get("authorization")
        if not token:
            return jsonify({"message": "Falha de autenticação", "auth": "Authorization"}), 401
        if not "Bearer" in str(token):
            return jsonify({"message": "Autenticação inválida", "auth": "Authorization"}), 401
        try:
            xtoken = token.replace("Bearer", "").strip()
            print(xtoken)
            decode = jwt.decode(xtoken, current_app.config['SECRET_KEY'], algorithm="HS256")
            print(decode)
            current_user = decode['id']
        except Exception as e:
            print(f'Error: {e}')
            if f"Signature has expired" == f'{e}':
                return jsonify({"message": f'{e}', "auth": "Authorization"}), 403
            return jsonify({"message": "Falha de autenticação", "auth": "Authorization"}), 401
        return f(current_user=current_user, *args, **kwargs)
    return wrap


def authorization_user(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        current_user = kwargs.get('current_user')
        result = User().verifica_permissao(current_user)
        print(result)
        if result:
            return result
        return f(*args, **kwargs)
    return wrap

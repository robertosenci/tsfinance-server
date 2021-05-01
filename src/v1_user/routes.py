from . import blueprint
from flask import jsonify, request, current_app
from .user import User
from ..authorization import authorization_key, authorization_jwt, authorization_user

app = current_app


@blueprint.route('/status')
def status():
    print('[GET] /auth/status')
    return f'<h1>Servidor ({blueprint.name}) ativo!</h1>'


@blueprint.route('/login', methods=['POST'])
@authorization_key
def login():
    params = request.get_json()
    return User().login(params)


@blueprint.route('/', methods=['POST'])
@authorization_key
def insert():
    params = request.get_json()
    return User().insert(params)


@blueprint.route('/', methods=['PUT'])
@authorization_key
@authorization_jwt
@authorization_user
def update():
    params = request.get_json()
    return User().update(user=params)


@blueprint.route('/<codigo>', methods=['DELETE'])
@authorization_key
@authorization_jwt
@authorization_user
def delete(codigo):
    params = request.get_json()
    return User().delete(codigo=codigo)


@blueprint.route('/<active>/<codigo>', methods=['PATH'])
@authorization_key
@authorization_jwt
@authorization_user
def delete(active, codigo):
    params = request.get_json()
    return User().active(active=active, codigo=codigo)


@blueprint.route('/refresh-token', methods=['POST'])
@authorization_key
def refresh_token():
    params = request.get_json()
    return User().refresh_token(params)

#
# @blueprint.route('auth', methods=['POST'])
# @authorization_key
# def auth_user():
#     params = request.get_json()
#     return User().auth_user(params)
#
# @blueprint.route('protected', methods=['GET'])
# @authorization_jwt
# def protected(current_user):
#     print(current_user)
#     params = request.get_json()
#     return User().protected(params)
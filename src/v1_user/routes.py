from . import blueprint
from flask import jsonify, request, current_app
from .user import User
from ..authorization import authorization_key, authorization_jwt, authorization_user

app = current_app


@blueprint.route('/status')
def status():
    print('[GET] /user/status')
    return f'<h1>Servidor ({blueprint.name}) ativo!</h1>'


@blueprint.route('/me')
@authorization_key
@authorization_jwt
def get_me(current_user):
    print(f'[GET] /me')
    return User().get_by_email(email=current_user)


@blueprint.route('/login', methods=['POST'])
@authorization_key
def login():
    print('[POST] /user/login')
    params = request.get_json()
    return User().login(params)


@blueprint.route('', methods=['POST'])
@authorization_key
def insert():
    print('[POST] /user')
    params = request.get_json()
    print(params)
    return User().insert(params)


@blueprint.route('', methods=['PUT'])
@authorization_key
@authorization_jwt
@authorization_user
def update(current_user):
    print('[PUT] /user')
    params = request.get_json()
    print(params)
    return User().update(user=params)


@blueprint.route('/<codigo>', methods=['DELETE'])
@authorization_key
@authorization_jwt
@authorization_user
def delete(current_user, codigo):
    print(f'[DELETE] /user/{codigo}')
    params = request.get_json()
    return User().delete(codigo=codigo)


@blueprint.route('', methods=['GET'])
@authorization_key
@authorization_jwt
def list_user(current_user):
    print('[GET] /user')
    return User().list_user()


@blueprint.route('/<codigo>', methods=['GET'])
@authorization_key
@authorization_jwt
@authorization_user
def get_user(current_user, codigo):
    print('[GET] /user/codigo')
    return User().get_by_id(codigo=codigo)


@blueprint.route('/<active>/<codigo>', methods=['PATH'])
@authorization_key
@authorization_jwt
@authorization_user
def delete(active, codigo):
    print(f'[PATH] /user/{active}/{codigo}')
    params = request.get_json()
    return User().active(active=active, codigo=codigo)


@blueprint.route('/refresh-token', methods=['POST'])
@authorization_key
def refresh_token():
    print(f'[POST] /user/refresh-token')
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

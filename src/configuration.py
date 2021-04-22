# -*- encoding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SESSION_COOKIE_SECURE = False  # Tornar true quando estiver usando hhtps
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    CSRF_ENABLED = True
    SECRET_KEY = "77tgFCdrEEdv77554##@3"
    APP_TOKEN = "d6143c11e0fe96c176e9346d0ceadb2fe799463a26459c59bf16e74e374850bd"
    APP_KEY = "a60197348426ffe2c564d994795ce35dd3ea85a8e9345d24c0853636e4c571fb"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')

    SECRET_KEYS = {'key': 'value'}
    SQL_RECONNECTION = 2


class ProductionConfig(Config):
    PRODUCTION = True
    DEVELOPMENT = False
    DEBUG = False


class DevelopmentConfig(Config):
    PRODUCTION = False
    DEVELOPMENT = True
    DEBUG = True


CONFIGS = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}


class Credenciais:
    POSTGRESQL = ("DRIVER={PostgreSQL Unicode(x64)};"
                  "DATABASE=tsempreendimento;"
                  "UID=postgres;"
                  f"PWD=solution;"
                  "SERVER=localhost;"
                  "PORT=5434;")


class Constantes:
    MESES = [
        'Janeiro',
        'Fevereiro',
        'Março',
        'Abril',
        'Maio',
        'Junho',
        'Julho',
        'Agosto',
        'Setembro',
        'Outubro',
        'Novembro',
        'Dezembro'
    ]
    SEMANA = [
        'Segunda',
        'Terça',
        'Quarta',
        'Quinta',
        'Sexta',
        'Sabado',
        'Domingo',
    ]
    TIMEOUT = 30

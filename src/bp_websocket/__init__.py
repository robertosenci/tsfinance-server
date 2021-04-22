# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Blueprint, current_app

app_name = current_app.config['APPNAME'].lower()

blueprint = Blueprint(
    f"{app_name}_realtime",
    __name__,
    url_prefix=f'/{app_name}/auth',
    template_folder='templates',
    static_folder=''
)

from . import routes

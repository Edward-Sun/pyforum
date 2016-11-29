#!/usr/bin/env python
# -*- coding: utf-8 -*-
import string

import random
from enum import Enum

from config import SESSION_SALT, MYSQL, MYSQL_NAME
from flask import Flask, current_app, render_template,session
from flask_login import LoginManager
from flask_session import Session
from flask_session.sessions import RedisSessionInterface
from playhouse.pool import PooledMySQLDatabase

from website import blueprints
from flask_mail import Mail


__author__ = 'walker_lee'
"""应用初始化入口以及配置"""


mail = Mail()
db = PooledMySQLDatabase(database=MYSQL_NAME, max_connections=32, stale_timeout=300, **MYSQL)
login_manager = LoginManager()
# login_manager.session_protection = 'strong'
login_manager.session_protection = None
login_manager.login_view = 'backend.login'


class Server(Enum):
    all = -1
    backend = 1
    fronted = 2


def create_app(config=None, server=Server.all):
    """初始化flask相关配置"""
    app = Flask('pyforum')
    app.config.from_object(config)
    init_blueprint(app, server)
    _config_session(app)
    _config_sitemap(app)
    mail.init_app(app)
    login_manager.init_app(app)
    app.jinja_env.globals['csrf_token'] = _generate_csrf_token
    return app


def init_blueprint(app, server):
    if Server.backend == server:
        blueprints.init_backend(app, server=server)
    elif server == Server.all:
        blueprints.init_backend(app, server=server)


def _config_session(app):
    app.secret_key = SESSION_SALT
    app.config['SESSION_TYPE'] = 'redis'
    Session(app)
    # app.session_interface = RedisSessionInterface()

def _generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    return session['_csrf_token']




def _config_sitemap(app):
    """
    显示所有注册uri地址
    :param app:
    :return:
    """
    @app.route('/site_map')
    def site_map():
        if 'RELEASE' in current_app.config:
            return ''

        links = []
        for rule in app.url_map.iter_rules():
            f = app.view_functions[rule.endpoint]
            links.append({
                'methods': rule.methods,
                'rule': rule.rule,
                'endpoint': rule.endpoint,
                'function': f
            })
        links = sorted(links, key=lambda x: x['rule'])
        return render_template('backend/site_map.html', site_map=links)

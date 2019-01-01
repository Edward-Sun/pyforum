#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps

from flask import request, g

from website.http.main_exception import MainException
from website.models.module import Module
from flask_login import current_user

__author__ = 'walker_lee&edward_sun'


def check_permission(f):
    """
    后台初始化路由并进行权限检查
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        init_menus()
        return f(*args, **kwargs)

    return decorated_function

def init_menus():
    g.uri_path = request.path
    menus = Module.get_menus()
    g.menu = menus
    g.cur_menu = menus
    g.modules = Module.get_all_modules()

def get_user_id():
    """获取用户id,默认是登录态"""
    if not current_user.id:
        raise MainException.ACCOUNT_NOT_FOUND
    return current_user.id

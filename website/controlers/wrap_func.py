#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import url_for
from werkzeug.utils import redirect

__author__ = 'walker_lee'

"""装饰器方法"""
import  functools
from flask_login import current_user


def confirm_required(f):
    """
    登录权限拦截判断
    """

    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.confirmed:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('.unconfirmed'))

    return decorated_function
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_login import login_required

from website.controlers.backend.wrap_func import check_permission
from website.controlers.wrap_func import confirm_required
from flask import render_template,g
from ...blueprints import backend
from website.http.main_exception import MainException

__author__ = 'walker_lee&edward_sun'


@backend.route('/')
@login_required
@confirm_required
@check_permission
def index():
    return render_template('template.html', page_header={
        'title':'PKU Forum: Best Forum in Peking University',
        'content':'This forum is powered by mly, zjh, and szq.'})

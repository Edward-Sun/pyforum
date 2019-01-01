#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import abort, jsonify
from flask import request
from flask_paginate import Pagination, get_page_args
from peewee import JOIN, fn
from playhouse.flask_utils import object_list

from website.http.paginate import FlaskPagination
from website.http.request import Request
from website.http.response import Response
from website.models.post import Post

__author__ = 'walker_lee&edward_sun'

from flask_login import login_required

from website.controlers.backend.wrap_func import check_permission, get_user_id
from website.controlers.wrap_func import confirm_required
from flask import render_template, g
from ...blueprints import backend


@backend.route('/module/<int:id>', methods=['GET'])
@login_required
@confirm_required
@check_permission
def post_list(id):
    rows = Post.get_post_list_by_module(id)
    return object_list('post/list.html', paginate=FlaskPagination(query=rows), query=rows,
                       context_variable='rows', paginate_by=10, check_bounds=False, page_header={'title': '板块文章列表', 'id': id})

@backend.route('/posts/<int:id>/create', methods=['GET', 'POST'])
@login_required
@confirm_required
@check_permission
def create_post_page(id):
    #print('METHOD', request.method, request.method == 'POST')

    if request.method == 'POST':
        print('POST Info')
        print(request.form)
        print('POST Info')
        title = request.form['title']
        content = request.form['content']
        Post.create_post(user_id=get_user_id(), module_id=id, title=title, content=content)
        return post_list(id)
    else:
        return render_template('post/edit.html',
                               check_bounds=False,
                               page_header={'title': '创建文章', 'id':id, 'method':'create_post_page'},
                               data={'row': {'module_id':id}})

@backend.route('/posts/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@confirm_required
@check_permission
def update_post_page(id):
    #print('METHOD', request.method, request.method == 'POST')
    
    if request.method == 'POST':
        print('POST Info')
        print(request.form)
        print('POST Info')
        id = request.form['id']
        module_id = request.form['module_id']
        title = request.form['title']
        content = request.form['content']
        
        Post.update_post(post_id=id, title=title, content=content)
        return post_list(module_id)
    else:
        post = Post.get(Post.id == id)
        if not post:
            abort(404)
        return render_template('post/edit.html',
                               page_header={'title': '编辑文章', 'id':id, 'method':'update_post_page'},
                               data={'row': post})
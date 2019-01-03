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
from website.models.user import User
from website.models.post import Post
from website.models.module import Module
from website.models.reply import Reply

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
    
    module = Module.get(Module.id == id)
    if not module:
        abort(404)
    
    module_name = module.name
    
    return object_list('post/list.html', paginate=FlaskPagination(query=rows), query=rows,
                       context_variable='rows', paginate_by=10, check_bounds=False,
                       page_header={'title': module_name+' 帖子列表', 'id': id, 'current_user':get_user_id()})

@backend.route('/post/<int:id>/delete', methods=['GET'])
@login_required
@confirm_required
@check_permission
def delete_post(id):
    post = Post.get(Post.id == id)
    module_id = post.module_id
    post.delete_instance()
    return post_list(module_id)

@backend.route('/post/<int:id>/create', methods=['GET', 'POST'])
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
                               page_header={'title': '创建帖子', 'id':id, 'method':'create_post_page'},
                               data={'row': {'module_id':id}})

@backend.route('/post/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@confirm_required
@check_permission
def update_post_page(id):
    #print('METHOD', request.method, request.method == 'POST')
    
    if request.method == 'POST':
        print('POST Info')
        print(request.form)
        print('POST Info')
        
        post = Post.get(Post.id == id)
        if not post:
            abort(404)        
        
        module_id = request.form['module_id']
        title = request.form['title']
        content = request.form['content']
        
        module = Module.get(Module.id == module_id)
        if not module:
            abort(404)
        
        Post.update_post(post_id=id, title=title, content=content)
        return post_list(module_id)
    else:
        post = Post.get(Post.id == id)
        if not post:
            abort(404)
            
        return render_template('post/edit.html',
                               page_header={'title': '编辑帖子', 'id':id, 'method':'update_post_page'},
                               data={'row': post})
    

@backend.route('/post/<int:id>/view', methods=['GET'])
@login_required
@confirm_required
@check_permission
def view_post_page(id):
    rows = Reply.get_reply_list_by_post(id)
    
    post = Post.get(Post.id == id)
    
    if not post:
        abort(404)
    
    post.add_view()
    
    post_title = post.title
    user_id = post.user_id
    like_count = post.like_count
    posted_at = post.posted_at
    updated_at = post.updated_at
    content = post.content
    return object_list('post/view.html', paginate=FlaskPagination(query=rows), query=rows,
                       context_variable='rows', paginate_by=100, check_bounds=False,
                       page_header={'title': post_title, 'id': id,
                                    'user_id': user_id,
                                    'like_count': like_count,
                                    'posted_at': posted_at,
                                    'updated_at': updated_at,
                                    'content': content, 'current_user':get_user_id()})

@backend.route('/reply/<int:id>/delete', methods=['GET'])
@login_required
@confirm_required
@check_permission
def delete_reply(id):
    reply = Reply.get(Reply.id == id)
    post_id = reply.post_id
    reply.delete_instance()
    return view_post_page(post_id)

@backend.route('/reply/<int:id>/create', methods=['GET', 'POST'])
@login_required
@confirm_required
@check_permission
def create_reply_page(id):
    if request.method == 'POST':
        print('POST Info')
        print(request.form)
        print('POST Info')
        content = request.form['content']
        Reply.create_reply(user_id=get_user_id(), post_id=id, content=content)
        return view_post_page(id)
    else:
        return render_template('post/edit_reply.html',
                               check_bounds=False,
                               page_header={'title': '创建回复', 'id':id, 'method':'create_reply_page'},
                               data={'row': {'post_id':id}})
    
@backend.route('/reply/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@confirm_required
@check_permission
def update_reply_page(id):
    if request.method == 'POST':
        print('POST Info')
        print(request.form)
        print('POST Info')
        
        reply = Reply.get(Reply.id == id)
        if not reply:
            abort(404)
            
        post_id = request.form['post_id']
        
        post = Post.get(Post.id == post_id)
        if not post:
            abort(404)
        
        content = request.form['content']
        
        Reply.update_reply(reply_id=id, content=content)
        return view_post_page(post_id)
    else:
        reply = Reply.get(Reply.id == id)
        if not reply:
            abort(404)
        return render_template('post/edit_reply.html',
                               page_header={'title': '编辑回复', 'id':id, 'method':'update_reply_page'},
                               data={'row': reply})
    
    
@backend.route('/user/<int:id>', methods=['GET'])
@login_required
@confirm_required
@check_permission
def user_profile_page(id):
    if id == 0:
        id = get_user_id()
    user = User.get(User.id == id)
    print('User Info')
    print(user)
    print('User Info')
    if not user:
        abort(404)
    return render_template('user/profile.html',
                           page_header={'title': '用户信息: ' + user.username, 'id':id, 'current_user':get_user_id()}, 
                           data={'row': user})

@backend.route('/user/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@confirm_required
@check_permission
def update_user_page(id):
    if request.method == 'POST':
        print('POST Info')
        print(request.form)
        print('POST Info')
        id = request.form['id']
        birthday = request.form['birthday']
        gender = request.form['gender']
        User.update_profile(user_id=id, birthday=birthday, gender=gender)
        
        return user_profile_page(id)
    else:
        user = User.get(User.id == id)
        if not user:
            abort(404)
        return render_template('user/profile_edit.html',
                               page_header={'title': '编辑用户信息', 'id':id, 'method':'update_user_page'},
                               data={'row': user})
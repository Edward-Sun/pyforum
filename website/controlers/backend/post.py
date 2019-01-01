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
from website.models.post import Post, PostTag, PostTagRelate

__author__ = 'walker_lee'

from flask_login import login_required

from website.controlers.backend.wrap_func import check_permission, get_user_id
from website.controlers.wrap_func import confirm_required
from flask import render_template, g
from ...blueprints import backend


@backend.route('/posts', methods=['GET'])
@login_required
@confirm_required
@check_permission
def post_list():
    rows = Post.get_post_list_query()
    return object_list('post/post/list.html', paginate=FlaskPagination(query=rows), query=rows,
                       context_variable='rows', paginate_by=10, check_bounds=False, page_header={'title': '全部文章列表'})

@backend.route('/tags', methods=['GET'])
@login_required
@confirm_required
@check_permission
def post_tag_list():
    rows = PostTag.select()
    return object_list('post/tag/list.html', paginate=FlaskPagination(query=rows), query=rows,
                       context_variable='rows', paginate_by=10, check_bounds=False, page_header={'title': '全部版块列表'})

@backend.route('/posts/create', methods=['GET'])
@login_required
@confirm_required
@check_permission
def create_post_page():
    return render_template('post/post/post.html',
                           check_bounds=False,
                           page_header={'title': '创建文章'},
                           data={'row': {}})

@backend.route('/posts/create', methods=['POST'])
@login_required
@confirm_required
@check_permission
def create_post():
    data = Request(request).json()
    Post.create_post(user_id=get_user_id(), title=data['title'], content=data['content'], summary=data['summary'],tags=data['tags'])
    return Response()

@backend.route('/posts/<int:id>/edit', methods=['GET'])
@login_required
@confirm_required
@check_permission
def update_post_page(id):
    post = Post.get(Post.id == id)
    if not post:
        abort(404)
    tags = PostTagRelate.get_tags_by_post_id(post_id=post.id)
    post.tags = tags
    return render_template('post/post/post.html',
                           page_header={'title': '编辑文章'},
                           data={'row': post})

@backend.route('/posts/<int:id>/edit', methods=['POST'])
@login_required
@confirm_required
@check_permission
def update_post(id):
    data = Request(request).json()
    Post.update_post(post_id=id, title=data['title'], content=data['content'], summary=data['summary'],tags=data['tags'])
    return Response()
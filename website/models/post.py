#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from website.app import db_wrapper, db
from website.http.main_exception import MainException
from website.util.common_utils import filter_same_element

__author__ = 'walker_lee&edward_sun'

from peewee import IntegerField, CharField, PrimaryKeyField, Model, TextField, JOIN, fn
from website.models.user import User

class Post(db_wrapper.Model):
    id = PrimaryKeyField()
    title = CharField()
    user_id = IntegerField()
    module_id = IntegerField()
    content = TextField()
    created_at = IntegerField()
    updated_at = IntegerField()
    posted_at = IntegerField()
    read_count = IntegerField()
    like_count = IntegerField()
    comment_floor = IntegerField()

    class Meta:
        db_table = 'post'

    @staticmethod
    def get_post_list_by_module(module_id):
        return Post.select().where(Post.module_id == module_id)

    @staticmethod
    def create_post(user_id, module_id, title, content):
        now = time.time()
        with db.transaction():
            post = Post(title=title, user_id=user_id, module_id=module_id, content=content,
                        posted_at=now, updated_at=now)
            post.save()

    @staticmethod
    def update_post(post_id, title, content):
        now = time.time()
        with db.transaction():
            post = Post.get(Post.id == post_id)
            if not post:
                raise MainException.NOT_FOUND
            post.title = title
            post.content = content
            post.updated_at = now
            post.save()
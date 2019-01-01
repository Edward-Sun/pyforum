#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from website.app import db_wrapper, db
from website.http.main_exception import MainException
from website.util.common_utils import filter_same_element

__author__ = 'walker_lee&edward_sun'

from peewee import IntegerField, CharField, PrimaryKeyField, Model, TextField, JOIN, fn
from website.models.user import User
from website.models.post import Post

class Reply(db_wrapper.Model):
    id = PrimaryKeyField()
    user_id = IntegerField()
    post_id = IntegerField()
    content = TextField()
    created_at = IntegerField()
    updated_at = IntegerField()
    posted_at = IntegerField()
    read_count = IntegerField()
    like_count = IntegerField()
    comment_floor_num = IntegerField()

    class Meta:
        db_table = 'reply'

    @staticmethod
    def get_reply_list_by_post(post_id):
        return Reply.select().where(Reply.post_id == post_id)

    @staticmethod
    def create_reply(user_id, post_id, content):
        now = time.time()
        with db.transaction():
            comment_floor_num = Post.get_and_update_post_floor(post_id)
            reply = Reply(user_id=user_id, post_id=post_id, content=content,
                        created_at=now, posted_at=now, updated_at=now, comment_floor_num=comment_floor_num)
            reply.save()

    @staticmethod
    def update_reply(reply_id, content):
        now = time.time()
        with db.transaction():
            reply = Reply.get(Reply.id == reply_id)
            if not reply:
                raise MainException.NOT_FOUND
            reply.content = content
            reply.updated_at = now
            reply.save()
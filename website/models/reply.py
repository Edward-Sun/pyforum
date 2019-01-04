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
        return Reply.select().where(Reply.post_id == post_id).order_by(Reply.comment_floor_num)

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
            
    @staticmethod
    def get_users_with_module_orderby_replycount(module_id):
        return  User.select(User.id, User.username, User.gender, User.level, fn.COUNT(User.id).alias('count'))\
        .join(Reply, on=(Reply.user_id == User.id))\
        .join(Post, on=(Reply.post_id==Post.id))\
        .where(Post.module_id==module_id).group_by(User.id, Post.module_id).order_by(-fn.COUNT(User.id))

    @staticmethod
    def get_mostPopular_post_with_module(module_id):
        return Reply.select(Reply.post_id).group_by(Reply.post_id).oder_by(fn.Count())

    @staticmethod
    def get_users_with_post(post_id):
        return Reply.select(User.username).join(User, on=(Reply.user_id==User.id)).where(Reply.post_id==post_id)

    @staticmethod
    def get_user_over_avgReply(module_id):
        reply_num = Reply.select(fn.COUNT(Reply.id)).join(Post, on=(Reply.post_id==Post.id)).where(Post.module_id==module_id)
        user_num = Reply.select(Reply.user_id).join(Post, on=(Reply.post_id==Post.id)).where(Post.module_id==module_id).distinct().count()
        avg = reply_num/user_num
        return User.select(User.id, User.username, User.gender, User.level, fn.COUNT(Reply.id).alias('count'))\
        .join(Reply, on=(Reply.user_id==User.id))\
        .join(Post, on=(Reply.post_id==Post.id))\
        .group_by(Post.module_id, User.id)\
        .having((fn.COUNT(Reply.id)>avg)&(Post.module_id==module_id)).order_by(-fn.COUNT(Reply.id))

    @staticmethod
    def get_post_user(post_id):
        return User.select().join(Reply, on=(User.id==Reply.user_id)).where(Reply.post_id==post_id).distinct()

    @staticmethod
    def get_most_popular_post(module_id):
        mmax = Post.select(fn.MAX(Reply.created_at-Post.created_at)).join(Reply, on=(Post.id==Reply.post_id))\
        .where((Post.comment_floor==Reply.comment_floor_num)&(Post.module_id==module_id))
        return Post.select().join(Reply, on=(Post.id==Reply.post_id))\
        .where((Reply.created_at-Post.created_at==mmax)&((Post.module_id==module_id))).order_by(-Post.comment_floor).get()
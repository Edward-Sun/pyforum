#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from website.app import db_wrapper, db
from website.http.main_exception import MainException
from website.util.common_utils import filter_same_element

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
    def get_and_update_post_floor(post_id):
        with db.transaction():
            post = Post.get(Post.id == post_id)
            if not post:
                raise MainException.NOT_FOUND
            post.comment_floor = post.comment_floor + 1
            post.save()
            return post.comment_floor
            
    @staticmethod
    def get_post_list_by_module(module_id):
        return Post.select().where(Post.module_id == module_id).order_by(-Post.updated_at)

            
    @staticmethod
    def get_recent_posts_by_user(user_id):
        return Post.select().where(Post.user_id == user_id).order_by(-Post.updated_at).limit(5)
    
    @staticmethod
    def create_post(user_id, module_id, title, content):
        now = time.time()
        with db.transaction():
            post = Post(title=title, user_id=user_id, module_id=module_id, content=content,
                        created_at=now, posted_at=now, updated_at=now)
            post.save()
    
    def add_view(self):
        with db.transaction():
            self.read_count = self.read_count + 1
            self.save()
    
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
            
    @staticmethod
    def get_topten_read_post():
        return Post.select().order_by(-Post.read_count).limit(10)

    @staticmethod
    def get_topten_reply_post():
        return Post.select().order_by(-Post.comment_floor).limit(10)

    @staticmethod
    def get_users_with_module_orderby_postcount(module_id):
        return  User.select(User.id, User.username, User.gender, User.level, fn.COUNT(User.id).alias('count'))\
        .join(Post, on=(Post.user_id == User.id))\
        .where(Post.module_id==module_id).group_by(User.id).order_by(-fn.COUNT(User.id), User.id)

    @staticmethod
    def get_post_over_avgRead(module_id):
        return Post.select().where((Post.read_count>=Post.select(fn.AVG(Post.read_count)).where(Post.module_id==module_id))\
        &(Post.module_id==module_id)).order_by(-Post.read_count)
    
    @staticmethod
    def get_postnum_inTen(user_id):
        now = time.time()
        return Post.select().where((Post.user_id==user_id)&(now-Post.created_at<=600)).count()
    
    @staticmethod
    def moreActive(id1, id2):
        print(id1, id2)
        user_dict = {}
        tmp1 = User.select(User.id, User.username, User.gender, User.level, fn.COUNT(Post.id).alias('count')).join(Post, on=(User.id==Post.user_id)).group_by(User.id, Post.module_id).where(Post.module_id==id1)
        tmp2 = User.select(User.id, User.username, User.gender, User.level, fn.COUNT(Post.id).alias('count')).join(Post, on=(User.id==Post.user_id)).group_by(User.id, Post.module_id).where(Post.module_id==id2)
        for user in tmp2:
            print(dir(user))
            user_dict[user.id] = [user.count, 0, user]
        
        for user in tmp1:
            if user.id in user_dict:
                user_dict[user.id][1] = user.count
        
        ret = [(user_dict[userid][2], user_dict[userid][0], user_dict[userid][1]) for userid in user_dict if user_dict[userid][0] > user_dict[userid][1]]

        return ret


    
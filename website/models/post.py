#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from website.app import db_wrapper, db
from website.http.main_exception import MainException
from website.util.common_utils import filter_same_element

__author__ = 'walker_lee'

from peewee import IntegerField, CharField, PrimaryKeyField, Model, TextField, fn, JOIN


class Post(db_wrapper.Model):
    id = PrimaryKeyField()
    title = CharField()
    user_id = IntegerField()
    summary = TextField()
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
    def get_post_list_query():
        return Post.select(Post, 
                           fn.GROUP_CONCAT(PostTagRelate.tag_name).alias('tags')
                          ).join(PostTagRelate, 
                                 JOIN.LEFT_OUTER,
                                 on=(PostTagRelate.post_id == Post.id)
                                ).group_by(Post.id)

    @staticmethod
    def create_post(user_id, title, summary, content, tags=[]):
        now = time.time()
        tags = filter_same_element(tags)
        with db.transaction():
            PostTag.create_tags(tags=tags)
            post = Post(title=title, user_id=user_id, content=content, summary=summary,
                        created_at=now, updated_at=now)
            rs = post.save()
            PostTagRelate.create_tag_relate(tags=tags, post_id=post.id)
        return rs

    @staticmethod
    def update_post(post_id,title,summary,content,tags=[]):
        post = Post.get(Post.id == post_id)
        now = time.time()
        if not post:
            raise MainException.NOT_FOUND
        post.title = title
        post.summary = summary
        post.content = content
        post.updated_at = now
        with db.transaction():
            PostTag.create_tags(tags=tags)
            post.save()
            PostTagRelate.delete_tag_relate_by_post_id(post_id=post.id)
            PostTagRelate.create_tag_relate(tags=tags,post_id=post.id)




class PostTag(db_wrapper.Model):
    id = PrimaryKeyField()
    tag_name = CharField()
    visit_count = IntegerField()
    created_at = IntegerField(default=time.time())

    class Meta:
        db_table = 'post_tag'

    @staticmethod
    def create_tags(tags):
        """如果标签不存在,则创建标签"""
        for tag in tags:
            PostTag().get_or_create(tag_name=tag)





class PostTagRelate(db_wrapper.Model):
    id = PrimaryKeyField()
    post_id = IntegerField()
    tag_name = CharField()

    class Meta:
        db_table = 'post_tag_relate'

    @staticmethod
    def get_tags_by_post_id(post_id):
        return PostTagRelate.select().where(PostTagRelate.post_id == post_id).dicts().execute()

    @staticmethod
    def delete_tag_relate_by_post_id(post_id):
        PostTagRelate.delete().where(PostTagRelate.post_id == post_id).execute()


    @staticmethod
    def create_tag_relate(tags,post_id):
        data_source =[]
        for tag in tags:
            data_source.append({'post_id':post_id,
                                'tag_name':tag
                                })
        if not tags:
            return
        with db.atomic():
            PostTagRelate.insert_many(data_source).execute()







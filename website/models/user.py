#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

import peewee
from flask import current_app,abort
from flask.ext.login import AnonymousUserMixin, UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from peewee import Model, IntegerField, CharField,PrimaryKeyField
from website.app import db_wrapper, login_manager, db
from website.http.main_exception import MainException
from werkzeug.security import check_password_hash,generate_password_hash

__author__ = 'walker_lee&edward_sun'

class User(UserMixin, db_wrapper.Model):

    id = PrimaryKeyField()
    email = CharField(index=True)
    username = CharField(index=True)
    password_hash = CharField()
    role_id = IntegerField()
    confirmed = IntegerField()
    birthday = IntegerField()
    gender = CharField()
    level = IntegerField()
    register_date = IntegerField()
    
    class Meta:
        db_table = 'user'
    
    @staticmethod
    def update_profile(user_id, birthday, gender):
        with db.transaction():
            user = User.get(User.id == user_id)
            if not user:
                raise MainException.NOT_FOUND
            user.birthday = birthday
            user.gender = gender
            user.save()
    
    def register(self, email, password, username):
        now = time.time()
        user = User(email=email, username=username, password_hash=generate_password_hash(password), register_date=now)
        try:
            user.save()
        except peewee.IntegrityError as err:
            print(err.args)
            if  err.args[0] == 1062:
                if 'ix_users_email' in err.args[1]:
                    raise MainException.DUPLICATE_EMAIL
                if 'ix_users_username' in err.args[1]:
                    raise MainException.DUPLICATE_USERNAME
        return user


    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    def generate_confirmation_token(self, expiration=3600):
        """生成验证邮箱的token"""
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        """验证邮箱"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
            print(data)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        # 验证成功,写入数据库
        self.confirmed = True
        self.save()
        return True

    def generate_reset_token(self, expiration=3600):
        """生成重置密码的token"""
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        """重置密码"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        # 验证成功,写入数据库
        self.password = new_password
        self.save()
        return True


"""
匿名用户
"""
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    user = User.get(User.id == int(user_id))
    if not user:
        abort(404)
    else:
        return user




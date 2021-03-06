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
from datetime import datetime, timedelta, timezone

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
    def get_xml(user, posts):
        ret = ''
        ret += '<XML>\n'
        ret += '  <Users>\n'
        ret += '    <User>\n'
        ret += '      <Info>\n'
        ret += '        <BasicInfo>\n'
        ret += '          <UserID>'+str(user.id)+'</UserID>\n'
        ret += '          <UserName>'+str(user.username)+'</UserName>\n'
        ret += '          <Email>'+str(user.email)+'</Email>\n'
        ret += '          <Birthday>'+str(user.birthday)+'</Birthday>\n'
        ret += '          <Register>'+str(user.register_date)+'</Register>\n'
        ret += '          <Gender>'+str(user.gender)+'</Gender>\n'
        ret += '          <Level>'+str(user.level)+'</Level>\n'
        ret += '        </BasicInfo>\n'
        ret += '        <OtherInfo>\n'
        ret += '          <Posts>\n'
        for post in posts:
            ret += '            <Post>\n'
            ret += '              <Floor>'+str(post.comment_floor)+'</Floor>\n'
            ret += '              <Id>'+str(post.id)+'</Id>\n'
            ret += '              <Title>'+str(post.title)+'</Title>\n'
            ret += '              <ModuleId>'+str(post.module_id)+'</ModuleId>\n'
            ret += '              <ReadNum>'+str(post.read_count)+'</ReadNum>\n'
            ret += '              <LikeNum>'+str(post.like_count)+'</LikeNum>\n'
            ret += '              <Post_at>'+str(post.posted_at)+'</Post_at>\n'
            ret += '              <Update_at>'+str(post.updated_at)+'</Update_at>\n'
            ret += '            </Post>\n'
        ret += '          </Posts>\n'
        ret += '        <OtherInfo>\n'
        ret += '      </Info>\n'
        ret += '    </User>\n'
        ret += '  </Users>\n'
        ret += '</XML>'

        return ret    
    
    @staticmethod
    def update_profile(user_id, birthday, gender):
        with db.transaction():
            user = User.get(User.id == user_id)
            if not user:
                raise MainException.NOT_FOUND
            month, day, year = birthday.split('-')
            timestep = int(datetime(int(year), int(month), int(day), tzinfo=timezone.utc).timestamp())
            user.birthday = timestep
            user.gender = gender
            user.save()
    
    def register(self, email, password, username, confirmed=False):
        now = time.time()
        user = User(email=email, username=username, password_hash=generate_password_hash(password), register_date=now, confirmed=confirmed)
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




#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from website.app import db_wrapper, db
from website.http.main_exception import MainException
from website.util.common_utils import filter_same_element

from peewee import IntegerField, CharField, PrimaryKeyField, Model, TextField, JOIN, fn

class Role(db_wrapper.Model):
    role_id = IntegerField()
    user_id = IntegerField()
    module_id = IntegerField()

    class Meta:
        db_table = 'role'
        
    @staticmethod
    def get_role(user_id, module_id):
        with db.transaction():
            role = Role.select().where(Role.user_id == user_id, Role.module_id == module_id)
            
            if len(role) > 0:
                role = role[0]
            else:
                role = None
            
            admin_role = Role.select().where(Role.user_id == user_id, Role.module_id == 0)

            if len(admin_role) > 0:
                admin_role = admin_role[0]
            else:
                admin_role = None
            
            if not role and not admin_role:
                return 20
            elif admin_role and not role:
                return admin_role.role_id
            elif role and not admin_role:
                return role.role_id
            else:
                return max(role.role_id, admin_role.role_id)
    
    @staticmethod
    def get_banzhu(module_id):
        roles = Role.select().where(Role.role_id == 256, Role.module_id == module_id)
        ret = []
        for role in roles:
            ret.append(role.user_id)
        return ret
    
    @staticmethod
    def update_role(role_id, user_id, module_id):
        with db.transaction():
            role = Role.select().where(Role.user_id == user_id, Role.module_id == module_id)
            if len(role) == 0:
                role = Role.create(role_id=role_id, user_id=user_id, module_id=module_id)
            else:
                role = role[0]
                role.role_id = role_id
            role.save()
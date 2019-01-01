#!/usr/bin/env python
# -*- coding: utf-8 -*-
from playhouse.shortcuts import model_to_dict

from website.app import db_wrapper
from peewee import IntegerField, CharField, PrimaryKeyField, Model, SmallIntegerField, ForeignKeyField

__author__ = 'walker_lee&edward_sun'


class Module(db_wrapper.Model):
    id = PrimaryKeyField()
    parent_id = IntegerField()
    name = CharField()
    url = CharField()
    prefix = CharField()
    weight = SmallIntegerField()

    class Meta:
        db_table = 'module'
    
    @staticmethod
    def get_module_name(id):
        """获取板块名字"""
        x = [module.name for module in Module.select().where(Module.id == id)]
        if len(x) == 1:
            return x[0]   
        else:
            return 'None'
    
    @staticmethod
    def get_menus():
        """获取菜单"""
        menus = [model_to_dict(row) for row in
                Module.select().order_by(Module.parent_id.asc(), 
                                         Module.weight.desc())]
        return menus

    @staticmethod
    def get_all_modules():
        """获取所有模块id"""
        
        return [module.id for module in Module.select()]
    
class RoleUserModule(db_wrapper.Model):
    role_id = SmallIntegerField()
    user_id = IntegerField()
    module_id = IntegerField()

    class Meta:
        db_table = 'role_user_module'

    @staticmethod
    def get_role_id_by_module_and_user(module_id, user_id):
        role_id = [row.role_id for row in 
                   RoleUserModule.select().where(
                       RoleUserModule.module_id == module_id,
                       RoleUserModule.user_id == user_id
                   )]
        if len(role_id) > 0:
            return role_id[0]
        else:
            return 20

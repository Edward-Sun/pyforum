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
        module = Module.get(Module.id == id)
        if not module:
            raise MainException.NOT_FOUND
        return module.name
    
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
        role_user_module = RoleUserModule.get(RoleUserModule.module_id == module_id,
                                              RoleUserModule.user_id == user_id)
        if not role_user_module:
            return 20
        return role_user_module.role_id
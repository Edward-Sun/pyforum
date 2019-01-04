#!/usr/bin/env python
# -*- coding: utf-8 -*-
from playhouse.shortcuts import model_to_dict

from website.app import db_wrapper, db
from peewee import IntegerField, CharField, PrimaryKeyField, Model, SmallIntegerField, ForeignKeyField

__author__ = 'walker_lee&edward_sun'


class Module(db_wrapper.Model):
    id = PrimaryKeyField()
    parent_id = IntegerField()
    name = CharField()
    intro = CharField()
    url = CharField()
    prefix = CharField()
    weight = SmallIntegerField()

    class Meta:
        db_table = 'module'

    def update_info(self, name, intro):
        with db.transaction():
            self.name = name
            self.intro = intro
            self.save()
            
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
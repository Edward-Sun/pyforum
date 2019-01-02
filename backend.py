#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config
from website.app import  Server, create_app

__author__ = 'walker_lee'

"""后台入口"""


app = create_app(config, server=Server.backend)
if __name__ == '__main__':
    app.run(port=config.FLASK_PORT)
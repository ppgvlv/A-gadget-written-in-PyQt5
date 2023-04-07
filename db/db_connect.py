# !/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql

from pymysql import Connection


DB_HOST = '127.0.0.1'
DB_USER = 'root'
DB_PASSWORD = 'pp'
DB_NAME = 'mail_list_sys'
DB_PORT = 3306


def get_db_connect() -> Connection:
    return pymysql.connect(host=DB_HOST,
                           user=DB_USER,
                           password=DB_PASSWORD,
                           database=DB_NAME,
                           port=int(DB_PORT),
                           cursorclass=pymysql.cursors.DictCursor)

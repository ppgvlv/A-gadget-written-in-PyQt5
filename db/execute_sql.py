# !/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from pymysql import Connection
from typing import List, Dict, Tuple, Any
from functools import wraps

from .db_connect import get_db_connect

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

string_type = ['CHAR', 'VARCHAR', 'TINYBLOB', 'TINYTEXT', 'TEXT', 'MEDIUMTEXT', 'LONGTEXT']
number_type = ['TINYINT', 'SMALLINT', 'MEDIUMINT', 'INT', 'INTEGER', 'BIGINT', 'FLOAT', 'DOUBLE', 'DECIMAL']
datetime_type = ['DATE', 'TIME', 'YEAR', 'DATETIME', 'TIMESTAMP']

DB_CONN = get_db_connect()


def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        logging.debug(func.__name__ + " was called")
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(e)
            return []

    return with_logging


@logit
def get_all_mail_list(uid, conn: Connection = DB_CONN) -> List[Dict]:
    sql = f"select * from mail_list where uid={uid};"
    print('get mail list sql: ', sql)
    with conn.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result


@logit
def save_mail_list_data(data, conn: Connection = DB_CONN) -> bool:
    """
    存储数据
    """
    cols = ", ".join('`{}`'.format(k) for k in data.keys())
    print(cols)  # '`name`, `age`'

    val_cols = ', '.join('%({})s'.format(k) for k in data.keys())
    print(val_cols)  # '%(name)s, %(age)s'

    with conn.cursor() as cursor:
        sql = "insert into mail_list(%s) values(%s)"
        res_sql = sql % (cols, val_cols)
        print(res_sql)
        cursor.execute(res_sql, data)  # 将字典data传入

        conn.commit()
        return True


@logit
def update_mail_list(data, conn: Connection = DB_CONN) -> bool:
    if not data.get('id'):
        print('id can not be empty')
        return
    sql = f"""update mail_list set name='{data["name"]}', sex='{data["sex"]}', 
    phone='{data["phone"]}', qq='{data["qq"]}', address='{data["address"]}', relation='{data["relation"]}', photo='{data["photo"]}' where id={data['id']};"""
    with conn.cursor() as cursor:
        # print(sql)
        cursor.execute(sql)  # 将字典data传入

        conn.commit()
        return True


@logit
def delete_mail(mid, conn: Connection = DB_CONN):
    sql = f'delete from mail_list where id={mid};'
    print(sql)
    with conn.cursor() as cursor:
        cursor.execute(sql)
        conn.commit()
        return True


@logit
def save_account_book(data, conn: Connection = DB_CONN):
    """
    存储数据
    """
    cols = ", ".join('`{}`'.format(k) for k in data.keys())
    print(cols)  # '`name`, `age`'

    val_cols = ', '.join('%({})s'.format(k) for k in data.keys())
    print(val_cols)  # '%(name)s, %(age)s'

    with conn.cursor() as cursor:
        sql = "insert into account_book(%s) values(%s)"
        res_sql = sql % (cols, val_cols)
        print(res_sql)
        cursor.execute(res_sql, data)  # 将字典data传入

        conn.commit()
        return True


@logit
def update_account_book(data, conn: Connection = DB_CONN):
    if not data.get('id'):
        print('id can not be empty')
        return
    sql = f"""update account_book set a_type='{data["a_type"]}', record_time='{data["record_time"]}', 
    type='{data["type"]}', money='{data["money"]}', mark='{data["mark"]}' where id={data['id']};"""
    with conn.cursor() as cursor:
        print(sql)
        cursor.execute(sql)  # 将字典data传入

        conn.commit()
        return True


def get_all_account_book(uid, a_type='收入', conn: Connection = DB_CONN, start=None, end=None) -> List[Dict]:
    sql = f"select * from account_book where uid={uid} and a_type='{a_type}'"
    if start and end:
        sql += f" and record_time between '{start}' and '{end}';"
    print('get mail list sql: ', sql)
    with conn.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result


@logit
def delete_account_book(mid, conn: Connection = DB_CONN):
    sql = f'delete from account_book where id={mid};'
    print(sql)
    with conn.cursor() as cursor:
        cursor.execute(sql)
        conn.commit()
        return True


@logit
def update_user_info(data, conn: Connection = DB_CONN):
    if not data.get('id'):
        print('id can not be empty')
        return
    sql = f"""update user set username='{data["username"]}', password='{data["password"]}', 
    name='{data["name"]}', university='{data["university"]}', personal_profile='{data["personal_profile"]}' where id={data['id']};"""
    with conn.cursor() as cursor:
        print(sql)
        cursor.execute(sql)  # 将字典data传入

        conn.commit()
        return True


@logit
def add_account(data, conn: Connection = DB_CONN):
    cols = ", ".join('`{}`'.format(k) for k in data.keys())
    print(cols)  # '`name`, `age`'

    val_cols = ', '.join('%({})s'.format(k) for k in data.keys())
    print(val_cols)  # '%(name)s, %(age)s'

    with conn.cursor() as cursor:
        sql = "insert into user(%s) values(%s)"
        res_sql = sql % (cols, val_cols)
        print(res_sql)
        cursor.execute(res_sql, data)  # 将字典data传入

        conn.commit()
        return True


@logit
def get_my_info(uid, conn: Connection = DB_CONN):
    sql = f"select * from user where id={uid};"
    with conn.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result


@logit
def check_account(username, password, conn: Connection = DB_CONN) -> int:
    sql = f"select * from user where username='{username}' and password='{password}';"
    with conn.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        if result:
            return result[0]['id']
        return 0

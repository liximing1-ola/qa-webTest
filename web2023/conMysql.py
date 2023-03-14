#! /usr/bin/python
# coding=utf-8

import pymysql as MySQL
import time


class mysql:
    def __init__(self,
                 host='192.168.11.46',
                 user='root',
                 passwd='123456',
                 db='xianshi',
                 port=3306,
                 charset='utf8'):
        self.cursor = None
        self.host = host
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.port = port
        self.charset = charset
        self.conn = None
        self._conn()

    def _conn(self):
        try:
            self.conn = MySQL.Connection(host=self.host, user=self.user, passwd=self.passwd, db=self.db, port=self.port,
                                         charset=self.charset)
            print("数据库连接成功")
            return True
        except Exception as e:
            print("数据库连接失败:" + str(e))
            return False

    # 通过ping()实现数据库的长连接
    def _reConn(self, num=28800, stime=3):
        _number = 0
        _status = True
        while _status and _number <= num:
            try:
                # ping校验连接是否异常
                self.conn.ping()
                _status = False
            except:
                print("数据库断开连接，重连")
                if self._conn():
                    _status = False
                    break
                _number += 1
                time.sleep(stime)

    def close(self):
        self._reConn()
        self.conn.close()

    def querry(self, sql):
        try:
            self._reConn()
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            self.cursor.close()
            return results
        except Exception as e:
            print("querry异常:" + str(e))
            return None

    def insert(self, sql, param):
        try:
            self._reConn()
            self.cursor = self.conn.cursor()
            res = self.cursor.execute(sql, param)
            self.conn.commit()
            self.cursor.close()
            return res
        except Exception as e:
            self.conn.rollback()
            print("insert异常:" + str(e))
            return False

    # 更新用户账户余额
    def updateMoneySql(self, uid, money=0, money_cash=0, money_cash_b=0, money_b=0, gold_coin=0, money_debts=0):
        sql = "update xs_user_money set money={}, money_b={}, money_cash={}, money_cash_b={},gold_coin={}, money_debts={} " \
              "where uid={} limit 1".format(money, money_b, money_cash, money_cash_b, gold_coin, money_debts, uid)
        try:
            self._reConn()
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            self.conn.commit()
            self.cursor.close()
        except Exception as error:
            self.conn.rollback()
            print('update fail', error)

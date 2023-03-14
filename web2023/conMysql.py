#! /usr/bin/python
# coding=utf-8

import pymysql as MySQL
import time
import random


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

    def insertIdCard(self, uid):
        sql = 'select uid from xs_user_idcard order by id desc limit 1'
        try:
            self._reConn()
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            uuid = self.cursor.fetchone()
            print(uuid)
            sql = 'insert into xs_user_idcard(uid, app_id, cardname, cardnum, cardfront, cardback, cardin, state, dateline, update_time) ' \
                  'select {} as uid, app_id, cardname, cardnum, cardfront, cardback, cardin, state, dateline, update_time' \
                  ' from xs_user_idcard where uid = {}'.format(uid, uuid)
            self.cursor.execute(sql)
            self.conn.commit()
            self.cursor.close()
        except Exception as error:
            self.conn.rollback()
            print('insert fail', error)

    def insertPeople(self, rid):
        uids = {"0": 100287189, "1": 100010055, "9": 100010056, "3": 100010057, "4": 100010058, "5": 100010059,
                "6": 100010060, "7": 100010061, "8": 100010068, "2": 131565153, "10": 100010073, "11": 100010075}
        try:
            self._reConn()
            self.cursor = self.conn.cursor()
            for k, v in uids.items():
                sql = 'UPDATE xs_chatroom_config SET uid = {} WHERE rid = {} and position = {}'.format(v, rid, int(k))
                self.cursor.execute(sql)
            self.conn.commit()
            self.cursor.close()
        except Exception as error:
            self.conn.rollback()
            print(error)

    def sqlDemo(self, user_id):
        sql = "select username from qa_case.user where id={}".format(user_id)
        try:
            self._reConn()
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            return res
        except Exception as error:
            print(error)
            return 0

    def pay(self, uid, money):
        order_id = '281{}ad0dd8taa00{}'.format(str(random.randint(1, 50)),
                                               str(random.choice('abcdefghijklmnopqrstuvwxyz!@#$%^&*()')))
        sql = "INSERT INTO xs_pay (uid, order_id, money, transaction_id, platform, create_time, end_time, state, ip, type, todo_id, product_name, buyer_account, buyer_id, source, app) VALUES ({}, '{}', {}, '4200000160201809161783627131', 'wechat', 1635696000, 1635696000, 'success',613787442, 'recharge', 1737783, '充值', 'oDe8X0tcPpUATk248lcbbD9C6wV0', 'oDe8XX0tcPpUATk248lcbbD9C6wV0', 'h5', 'iamban')".format(
            uid, order_id, money)
        try:
            self._reConn()
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            self.conn.commit()
            self.cursor.close()
        except Exception as error:
            self.conn.rollback()
            print(error)

    def delCommodity(self, uid):
        sql1 = "DELETE FROM xs_user_commodity where uid = {}".format(uid)
        sql2 = 'SELECT * from xs_user_commodity where uid = {}'.format(uid)
        try:
            self._reConn()
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql1)
            self.cursor.execute(sql2)
            res = self.cursor.fetchone()
            self.conn.commit()
            self.cursor.close()
            if res is None:
                print('del success')
        except Exception as error:
            self.conn.rollback()
            print('del fail', error)

    def addCommodity(self, uid):
        cids = [2, 3, 4, 9, 12, 13, 14, 15, 16, 17, 18, 20, 38, 100, 174, 175, 176, 177, 23629, 23630, 23631, 20878]
        sql2 = 'select cid, name  from xs_commodity where cid in ({})'.format(cids)
        mysql().delCommodity(uid)
        try:
            self._reConn()
            self.cursor = self.conn.cursor()
            for cid in cids:
                dateline = str(int(time.time()))
                sql1 = 'INSERT into xs_user_commodity(uid, cid, state, num, period_end, used, in_use, dateline) ' \
                       'VALUES ({}, {}, 0,{},0,0,0,{})'.format(uid, cid, 3, dateline)
                self.cursor.execute(sql1)
            self.cursor.execute(sql2)
            res = self.cursor.fetchall()
            self.conn.commit()
            self.cursor.close()
            return res
        except Exception as error:
            self.conn.rollback()
            print(error)

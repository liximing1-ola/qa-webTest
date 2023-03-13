#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @author: WuBingBing

import pymysql
import random
import time


class conMysql:
    db_config = {"dev_46_db": '192.168.11.46',
                 "dev_46_user": 'root',
                 "dev_46_pas": '123456',
                 "ali_db": '',
                 "ali_user": '',
                 "ali_pas": ''}
    _dbUrl = db_config['dev_46_db']
    _user = db_config['dev_46_user']
    _password = db_config['dev_46_pas']
    _dbName = 'xianshi'
    _dbPort = 3306
    con = pymysql.connect(host=_dbUrl,
                          port=_dbPort,
                          user=_user,
                          passwd=_password,
                          charset='utf8',
                          autocommit=True)
    con.select_db(_dbName)
    con.ping(reconnect=True)
    cur = con.cursor()

    # 更新用户账户余额
    @staticmethod
    def updateMoneySql(uid, money=0, money_cash=0, money_cash_b=0, money_b=0, gold_coin=0, money_debts=0):
        sql = "update xs_user_money set money={}, money_b={}, money_cash={}, money_cash_b={},gold_coin={}, money_debts={} " \
              "where uid={} limit 1".format(money, money_b, money_cash, money_cash_b, gold_coin, money_debts, uid)
        try:
            conMysql.cur.execute(sql)
        except Exception as error:
            conMysql.con.rollback()
            print('update fail', error)
        finally:
            conMysql.con.commit()

    @staticmethod
    def insertIdCard(uid):
        sql = 'select uid from xs_user_idcard order by id desc limit 1'
        conMysql.cur.execute(sql)
        uuid = conMysql.cur.fetchone()
        sql = 'insert into xs_user_idcard(uid, app_id, cardname, cardnum, cardfront, cardback, cardin, state, dateline, update_time) ' \
              'select {} as uid, app_id, cardname, cardnum, cardfront, cardback, cardin, state, dateline, update_time' \
              ' from xs_user_idcard where uid = {}'.format(uid, uuid)
        try:
            conMysql.cur.execute(sql)
        except Exception as error:
            conMysql.con.rollback()
            print('insert fail', error)
        finally:
            conMysql.con.commit()

    @staticmethod
    def insertPeople(rid):
        uids = {"0": 100287189, "1": 100010055, "9": 100010056, "3": 100010057, "4": 100010058, "5": 100010059,
                "6": 100010060, "7": 100010061, "8": 100010068, "2": 131565153, "10": 100010073, "11": 100010075}
        try:
            for k, v in uids.items():
                sql = 'UPDATE xs_chatroom_config SET uid = {} WHERE rid = {} and position = {}'.format(v, rid, int(k))
                conMysql.cur.execute(sql)
        except Exception as error:
            conMysql.con.rollback()
            print(error)
        finally:
            conMysql.con.commit()
            print('insert success')
            conMysql.con.close()

    @staticmethod
    def sqlDemo(user_id):
        sql = "select username from qa_case.user where id={}".format(user_id)
        try:
            conMysql.cur.execute(sql)
            res = conMysql.cur.fetchall()
            if len(res) > 0:
                return res
        except Exception as error:
            print(error)

    @staticmethod
    def pay(uid, money):
        order_id = '281{}ad0dd8taa00{}'.format(str(random.randint(1, 50)),
                                               str(random.choice('abcdefghijklmnopqrstuvwxyz!@#$%^&*()')))
        sql = "INSERT INTO xs_pay (uid, order_id, money, transaction_id, platform, create_time, end_time, state, ip, type, todo_id, product_name, buyer_account, buyer_id, source, app) VALUES ({}, '{}', {}, '4200000160201809161783627131', 'wechat', 1635696000, 1635696000, 'success',613787442, 'recharge', 1737783, '充值', 'oDe8X0tcPpUATk248lcbbD9C6wV0', 'oDe8XX0tcPpUATk248lcbbD9C6wV0', 'h5', 'iamban')".format(
            uid, order_id, money)
        try:
            conMysql.cur.execute(sql)
        except Exception as error:
            conMysql.con.rollback()
            print(error)
        else:
            print('commodity insert success')
        finally:
            conMysql.con.commit()
            conMysql.con.close()

    @staticmethod
    def delCommodity(uid):
        sql1 = "DELETE FROM xs_user_commodity where uid = {}".format(uid)
        sql2 = 'SELECT * from xs_user_commodity where uid = {}'.format(uid)
        try:
            conMysql.cur.execute(sql1)
            conMysql.cur.execute(sql2)
            res = conMysql.cur.fetchone()
            if res is None:
                print('del success')
        except Exception as error:
            conMysql.con.rollback()
            print('del fail', error)
        finally:
            conMysql.con.commit()

    @staticmethod
    def addCommodity(uid):
        cids = [2, 3, 4, 9, 12, 13, 14, 15, 16, 17, 18, 20, 38, 100, 174, 175, 176, 177, 23629, 23630, 23631, 20878]
        sql2 = 'select cid, name  from xs_commodity where cid in ({})'.format(cids)
        conMysql.delCommodity(uid)
        try:
            for cid in cids:
                dateline = str(int(time.time()))
                sql1 = 'INSERT into xs_user_commodity(uid, cid, state, num, period_end, used, in_use, dateline) ' \
                       'VALUES ({}, {}, 0,{},0,0,0,{})'.format(uid, cid, 3, dateline)
                conMysql.cur.execute(sql1)
            conMysql.cur.execute(sql2)
            res = conMysql.cur.fetchall()
            if res is None:
                return 0
            return res
        except Exception as error:
            conMysql.con.rollback()
            print(error)
        finally:
            conMysql.con.commit()
            conMysql.con.close()





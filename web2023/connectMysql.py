#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @author: WuBingBing

import pymysql


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
        sql = "select username from qa_case.user where id='{}'".format(user_id)
        try:
            conMysql.cur.execute(sql)
            res = conMysql.cur.fetchall()
            if len(res) > 0:
                return res
        except Exception as error:
            print(error)



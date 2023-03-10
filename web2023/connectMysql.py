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

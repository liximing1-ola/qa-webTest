from flask import Flask, render_template, request
from conMysql import mysql
import requests

app = Flask(__name__)
mysql = mysql()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template("addMoney.html")
    else:
        uid = request.form['uid']
        money = request.form['money']
    if len(uid) == 9 and int(money) < 2000000000:
        mysql.updateMoneySql(uid, money)
        return '<h3>---------恭喜你，金额：{}钻 已到账！！！----------</h3>'.format(money)
    return '<h3>---------------打款失败!!!---------------</h3>'


@app.route('/idChange', methods=['GET', 'POST'])
def idChange():
    if request.method == 'GET':
        return render_template("idChange.html")
    else:
        uid = request.form['uid']
    if len(uid) == 9:
        mysql.insertIdCard(uid)
        return '<h3>---------恭喜你，身份信息修改成功！！！----------</h3>'
    return '<h3>--------------修改失败!!!---------------</h3>'


@app.route('/insertPerson', methods=['GET', 'POST'])
def insertPerson():
    if request.method == 'GET':
        return render_template("insertPerson.html")
    else:
        rid = request.form['rid']
    if len(rid) == 9:
        mysql.insertPeople(rid)
        return '<h3>---------恭喜你，加人成功，刷新下room.config即可！！！----------</h3>'
    return '<h3>--------------提交失败!!!---------------</h3>'


@app.route('/sqlDemo', methods=['GET', 'POST'])
def sqlDemo():
    if request.method == 'GET':
        return render_template('sqlDemo.html')
    else:
        user_id = request.form['id']
    user_name = mysql.sqlDemo(user_id)
    return '<h3>当前查询结果：{}</h3>'.format(user_name)


@app.route('/createRoom', methods=['GET', 'POST'])
def createRoom():
    if request.method == 'GET':
        return render_template('createRoom.html')
    else:
        uid = request.form['uid']
        factory_type = request.form['type']
    if len(uid) == 9:
        url = 'http://192.168.11.46/test/changeRoom?uid={}&factory_type={}&property=business'.\
            format(int(uid), factory_type)
        res = requests.get(url)
        if res.status_code == 200:
            return '<h3>---------创建成功：{}----------</h3>'.format(res.json())
    return '<h3>---------创建失败：{}----------</h3>'


@app.route('/pay', methods=['GET', 'POST'])
def pay():
    if request.method == 'GET':
        return render_template("pay.html")
    else:
        uid = request.form['uid']
        money = request.form['money']
    if len(uid) == 9 and int(money) < 100000000:
        mysql.pay(uid, int(money))
        return '<h3>---------恭喜你，充值成功（money不会到账）！！！----------</h3>'.format(money)
    return '<h3>---------------充值失败!!!---------------</h3>'


@app.route('/addCommodity', methods=['GET', 'POST'])
def addCommodity():
    if request.method == 'GET':
        return render_template("addCommodity.html")
    else:
        uid = request.form['uid']
    if len(uid) == 9:
        mysql.addCommodity(uid)
        return '<h3>---------恭喜你，背包请查收！！！----------</h3>'
    return '<h3>---------------加物品失败!!!---------------</h3>'


if __name__ == "__main__":
    app.run(port=2023, host="192.168.11.57", debug=False)
    # app.run(port=2020, host='127.0.0.1', debug=True)

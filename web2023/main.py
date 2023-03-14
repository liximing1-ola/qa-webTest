from flask import Flask, render_template, request
from conMysql import mysql
import requests

app = Flask(__name__)
mysql = mysql()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/add')
def addPage():
    return render_template("addMoney.html")


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        uid = request.form['uid']
        money = request.form['money']
    else:
        uid = request.args.get('uid')
        money = request.args.get('money')
    if len(uid) == 9 and int(money) < 2000000000:
        mysql.updateMoneySql(uid, money)
        return '<h3>---------恭喜你，金额：{}钻 已到账！！！----------</h3>'.format(money)
    return '<h3>---------------打款失败!!!---------------</h3>'


@app.route('/idChange')
def idChangePage():
    return render_template("idChange.html")


@app.route('/idChange', methods=['GET', 'POST'])
def idChange():
    if request.method == 'POST':
        uid = request.form['uid']
    else:
        uid = request.args.get('uid')
    if len(uid) == 9:
        mysql.insertIdCard(uid)
        return '<h3>---------恭喜你，身份信息修改成功！！！----------</h3>'
    return '<h3>--------------修改失败!!!---------------</h3>'


@app.route('/insertPerson')
def insertPersonPage():
    return render_template("insertPerson.html")


@app.route('/insertPerson', methods=['GET', 'POST'])
def insertPerson():
    if request.method == 'POST':
        rid = request.form['rid']
    else:
        rid = request.args.get('rid')
    if len(rid) == 9:
        mysql.insertPeople(rid)
        return '<h3>---------恭喜你，加人成功，刷新下room.config即可！！！----------</h3>'
    return '<h3>--------------提交失败!!!---------------</h3>'


@app.route('/sqlDemo')
def sqlDemoPage():
    return render_template('sqlDemo.html')


@app.route('/sqlDemo', methods=['GET', 'POST'])
def sqlDemo():
    if request.method == 'POST':
        user_id = request.form['id']
    else:
        user_id = request.args.get('id')
    user_name = mysql.sqlDemo(user_id)
    return '<h3>当前查询结果：{}</h3>'.format(user_name)


@app.route('/createRoom')
def createRoomPage():
    return render_template('createRoom.html')


@app.route('/createRoom', methods=['GET', 'POST'])
def createRoom():
    if request.method == 'POST':
        uid = request.form['uid']
        factory_type = request.form['type']
    else:
        uid = request.args.get('uid')
        factory_type = request.args.get('type')
    if len(uid) == 9:
        url = 'http://192.168.11.46/test/changeRoom?uid={}&factory_type={}&property=business'.format(int(uid),
                                                                                                     factory_type)
        res = requests.get(url)
        if res.status_code == 200:
            return '<h3>---------创建成功：{}----------</h3>'.format(res.json())
    return '<h3>---------创建失败：{}----------</h3>'


@app.route('/pay')
def payPage():
    return render_template("pay.html")


@app.route('/pay', methods=['GET', 'POST'])
def pay():
    if request.method == 'POST':
        uid = request.form['uid']
        money = request.form['money']
    else:
        uid = request.args.get('uid')
        money = request.args.get('money')
    if len(uid) == 9 and int(money) < 100000000:
        mysql.pay(uid, int(money))
        return '<h3>---------恭喜你，充值成功（money不会到账）！！！----------</h3>'.format(money)
    return '<h3>---------------充值失败!!!---------------</h3>'


@app.route('/addCommodity')
def addCommodityPage():
    return render_template("addCommodity.html")


@app.route('/addCommodity', methods=['GET', 'POST'])
def addCommodity():
    if request.method == 'POST':
        uid = request.form['uid']
    else:
        uid = request.args.get('uid')
    if len(uid) == 9:
        res = mysql.addCommodity(uid)
        return '<h3>---------恭喜你，背包请查收！！！物品明细 {}----------</h3>'.format(res)
    return '<h3>---------------加物品失败!!!---------------</h3>'


if __name__ == "__main__":
    app.run(port=2023, host="192.168.11.57", debug=False)
    # app.run(port=2020, host='127.0.0.1', debug=True)

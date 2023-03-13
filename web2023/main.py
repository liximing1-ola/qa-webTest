from flask import Flask, render_template, url_for, redirect, request
from connectMysql import conMysql

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/add')
def addPage():
    return render_template("addMoney.html")


@app.route('/idChange')
def idChangePage():
    return render_template("idChange.html")


@app.route('/insertPerson')
def insertPersonPage():
    return render_template("insertPerson.html")


@app.route('/sqlDemo')
def sqlDemoPage():
    return render_template('sqlDemo.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        uid = request.form['uid']
        money = request.form['money']
    else:
        uid = request.args.get('uid')
        money = request.args.get('money')
    if len(uid) == 9 and int(money) < 2000000000:
        conMysql.updateMoneySql(uid, money)
        return '<h3>---------恭喜你，充值成功！！！----------</h3>'
    return '<h3>---------------提交失败!!!---------------</h3>'


@app.route('/idChange', methods=['GET', 'POST'])
def idChange():
    if request.method == 'POST':
        uid = request.form['uid']
    else:
        uid = request.args.get('uid')
    if len(uid) == 9:
        conMysql.insertIdCard(uid)
        return '<h3>---------恭喜你，修改成功！！！----------</h3>'
    return '<h3>--------------提交失败!!!---------------</h3>'


@app.route('/insertPerson', methods=['GET', 'POST'])
def insertPerson():
    if request.method == 'POST':
        rid = request.form['rid']
    else:
        rid = request.args.get('rid')
    if len(rid) == 9:
        conMysql.insertPeople(rid)
        return '<h3>---------恭喜你，加人成功！！！----------</h3>'
    return '<h3>--------------提交失败!!!---------------</h3>'


@app.route('/sqlDemo', methods=['GET', 'POST'])
def sqlDemo():
    if request.method == 'POST':
        id = request.form['id']
    else:
        id = request.args.get('id')
    id = conMysql.sqlDemo(id)
    return '<h3>---------恭喜你，查询结果：{}----------</h3>'.format(id)


if __name__ == "__main__":
    app.run(port=2023, host="192.168.11.57", debug=False)
    # app.run(port=2020, host='127.0.0.1', debug=True)

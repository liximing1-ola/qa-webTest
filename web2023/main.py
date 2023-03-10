from flask import Flask, render_template, url_for, redirect, request
from connectMysql import conMysql
app = Flask(__name__)


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
        conMysql.updateMoneySql(uid, money)
        return '<h3>---------恭喜你，充值成功！！！----------</h3>'
    return '<h3>---------------提交失败!!!---------------</h3>'


if __name__ == "__main__":
    app.run(port=2020, host="192.168.11.57", debug=True)

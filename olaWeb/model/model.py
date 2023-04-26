from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)


class Config(object):
    """配置参数"""
    # 设置连接数据库的URL
    user = 'root'
    password = '123456'
    database = 'qa_case'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@192.168.11.46:3306/%s' % (user, password, database)

    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 查询时会显示原始SQL语句
    app.config['SQLALCHEMY_ECHO'] = True

    # 禁止自动提交数据处理
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False


app.config.from_object(Config)

# 创建数据库sqlalchemy工具对象
db = SQLAlchemy(app)


class Share(db.Model):
    __tablename__ = 'shareList'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    auther = db.Column(db.String(64))
    title = db.Column(db.String(128), unique=True)
    link = db.Column(db.Text())
    create_time = db.Column(db.Date)
    update_time = db.Column(db.Date)
    deleted = db.Column(db.Integer, default=0)


if __name__ == '__main__':
    # 删除所有表
    db.drop_all()
    # 创建所有表
    # db.create_all()

from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for, Flask
import time
import os
import sys
sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])
from olaWeb.model import model
share = Blueprint("share", __name__, url_prefix="/share")
app = Flask(__name__)


# 展示全部分享
# share.route("/shareList")
def shareAll():
    # order_by按照时间倒序
    blogList = model.Share.query.order_by(model.Share.create_time.desc()).all()
    print(blogList)
    return jsonify(blogList)


if __name__ == "__main__":
    shareAll()

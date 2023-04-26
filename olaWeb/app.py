from flask import *


app = Flask(__name__)
app.config.from_object(config)
app.secret_key = "flaskblog"
app.debug = True

# 注册蓝图
from view import *

#app.register_blueprint(index)
#app.register_blueprint(blog)


# 404页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# 500页面
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('404.html'), 500


if __name__ == '__main__':
    app.run()

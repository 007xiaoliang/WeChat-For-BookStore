import os

from flask import Flask, request, session, redirect, url_for

from bp.bp1 import login_bp
from bp.bp2 import index_bp
from bp.bp3 import book_bp
from bp.bp4 import profile_bp
from utils.config import DBUSER, DBPASSWORD, DBHOST, DBPORT, DB
from utils.models import db

app = Flask(__name__)
# 注册蓝图
app.register_blueprint(login_bp)
app.register_blueprint(index_bp)
app.register_blueprint(book_bp)
app.register_blueprint(profile_bp)
# session配置
app.config['SECRET_KEY'] = os.urandom(24)
# 数据库配置
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + DBUSER + ':' + DBPASSWORD + '@' + DBHOST + ':' + DBPORT + '/' + DB + '?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 设置日志
# TODO
db.init_app(app)
with app.app_context():
    db.create_all()


# 启动服务器时开启必要的服务器以及连接
@app.before_first_request
def open_server():
    pass


# 对所有请求进行拦截与预处理
@app.before_request
def url_validate():
    if request.path != '/login' and request.path != '/register' and request.path != '/login/' and request.path != '/register/' and request.path != '/lockscreen/' \
            and not request.path.startswith('/static/'):
        if 'lock' in session and session['lock']:
            return redirect(url_for('login_blueprint.login'))
        elif 'user' not in session:
            return redirect(url_for('login_blueprint.login'))


if __name__ == '__main__':
    app.run()

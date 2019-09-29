# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Blueprint, request, render_template, session, jsonify, url_for, redirect

from utils.config import SERVER_IP
from utils.md5AndSalt import data_to_md5
from utils.models import User, db

# 处理用户登陆注册等
login_bp = Blueprint('login_blueprint', __name__)


@login_bp.route('/login/', methods=['POST', 'GET'], endpoint='login')
def login_view():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        # 获取数据
        uname = request.values.get("uname")
        page_id = request.values.get("page_id")
        # 从数据库查询用户名
        user = User.query.filter_by(name=uname).first()
        if user:
            pwd = request.values.get("pwd")
            # 对密码进行MD5加密
            pwd = data_to_md5(pwd)
            if user.password == pwd:
                # 将信息存储到session
                session['user'] = user.name
                if not page_id:
                    session['page_id'] = '0_1'  # 记忆当前浏览页面
                else:
                    session['page_id'] = page_id
                if "lock" in session:
                    session['lock'] = False
                return jsonify({"info": 'ok'})
            else:
                return jsonify({"info": "密码错误"})
        else:
            return jsonify({"info": "用户名不存在"})


@login_bp.route('/register/', methods=['POST', 'GET'])
def register_view():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # 获取数据
        uname = request.values.get("uname")
        # 从数据库查询用户
        user = User.query.filter_by(name=uname).first()
        if not user:
            pwd = request.values.get("pwd")
            # 对密码进行MD5加密
            pwd = data_to_md5(pwd)
            # 储存用户信息到数据库
            user = User(name=uname, password=pwd, regis_date=datetime.now())
            db.session.add(user)
            db.session.commit()
            return jsonify({"info": 'ok'})

        else:
            return jsonify({"info": "用户名已存在"})


@login_bp.route('/login_out/')
def login_out_view():
    session.pop('user')
    return render_template('login.html')


# 锁定屏幕
@login_bp.route('/lockscreen/')
def lock_srceen_view():
    if 'user' in session and 'page_id' in session:
        uname = session['user']
        page_id = session['page_id']
        session['lock'] = True
        user = User.query.filter_by(name=uname).first()
        return render_template('lockscreen.html', user=user, server=SERVER_IP, page_id=page_id)
    else:
        return redirect(url_for('login_blueprint.login'))

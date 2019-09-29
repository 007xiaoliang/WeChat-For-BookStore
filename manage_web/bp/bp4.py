# -*- coding: utf-8 -*-
import os

from flask import Blueprint, request, session, jsonify

from utils import connectionLinux
from utils.config import ALLOWED_EXTENSIONS, SERVER_IP, LOCAL_ADDR
from utils.md5AndSalt import data_to_md5
from utils.models import User, db

# 处理用户个人信息
profile_bp = Blueprint('profile_blueprint', __name__)
linux = connectionLinux.LinuxConn()  # linux连接


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 修改用户信息（验证是否本人操作）
@profile_bp.route("/profile_validatepwd/", methods=['POST'])
def profile_validatepwd_view():
    pwd = request.values.get("pwd")
    uname = request.values.get("user")
    # 从数据库查询用户名
    user = User.query.filter_by(name=uname).first()
    # 对密码进行MD5加密
    pwd = data_to_md5(pwd)
    if pwd == user.password:
        return jsonify({'info': "ok"})
    else:
        return jsonify({'info': "no"})


# 修改用户信息（修改信息）
@profile_bp.route("/profile_updateinfo/", methods=['POST'])
def profile_updateinfo_view():
    username = request.values.get("username")  # 当前登陆的用户名
    user_name = request.values.get("user_name")  # 输入的新用户名
    if user_name == '':
        user_name = username
    new_pwd = request.values.get("new_pwd")  # 输入的新密码
    # 从数据库查询用户名
    user = User.query.filter_by(name=username).first()
    if new_pwd != '':
        # 对密码进行MD5加密
        new_pwd = data_to_md5(new_pwd)
        user.password = new_pwd
    user.name = user_name
    db.session.commit()
    # 更改session中登陆用户信息
    session['user'] = user_name
    return jsonify({'info': "ok"})


# 修改用户信息（接受上传文件）
@profile_bp.route("/file_upload/", methods=['POST'])
def file_upload_view():
    img = request.files['photo']
    if img and allowed_file(img.filename):
        username = session['user']
        user = User.query.filter_by(name=username).first()
        file_name = str(data_to_md5(username)) + '.' + img.filename.split('.')[-1]
        file_path = LOCAL_ADDR + file_name
        user.img_id = file_name
        img.save(file_path)
        linux.ssh_scp_put(file_path, file_name)
        os.remove(file_path)
        db.session.commit()
        return jsonify({'info': "ok"})
    else:
        return jsonify({'info': "no"})


# 加载图片
@profile_bp.route("/show_img/", methods=['POST'])
def show_img_view():
    username = session['user']
    user = User.query.filter_by(name=username).first()
    if not user.img_id:
        path = SERVER_IP + '未上传.jpg'
    else:
        path = SERVER_IP + user.img_id
    return jsonify({'info': path})

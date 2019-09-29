# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, session, jsonify

from utils import redisUtils
from utils.models import User, Role

# 处理页面加载
index_bp = Blueprint('index_blueprint', __name__)
redis_client = redisUtils.RedisClient()


@index_bp.route('/index/')
def index_view():
    uname = session['user']
    page_id = session['page_id']
    user = User.query.filter_by(name=uname).first()
    role = Role.query.filter_by(id=user.role_id).first()
    return render_template('index.html', user=user, role=role, page_id=page_id)


@index_bp.route('/sub_html/', methods=['POST'])
def sub_html_view():
    page_id = request.values.get("id")
    book_name = request.values.get("book_name")
    book_writer = request.values.get("book_writer")
    book_press = request.values.get("book_press")
    if book_name and book_writer and book_press:
        # 将要修改的书籍信息缓存到redis
        redis_client.insert("book_name", book_name)
        redis_client.insert("book_writer", book_writer)
        redis_client.insert("book_press", book_press)
    session['page_id'] = page_id
    with open('templates/sub_html/' + page_id + '.html', encoding='utf8') as f:
        html_content = f.read()
    if html_content:
        {"pageInfo": html_content}

    return jsonify({"pageInfo": html_content})

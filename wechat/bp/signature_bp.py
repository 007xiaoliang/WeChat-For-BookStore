import time

from flask import Blueprint, request, render_template, session, jsonify

# 个人信息与订单有关
from utils import CreateSign, mongodb
from utils.config import SERVER_IP
from utils.util import user_handler

signature_bp = Blueprint('signature_blueprint', __name__)
# 创建mongodb连接
mdb = mongodb.Mongodb()


# 进入商城主页
@signature_bp.route('/mine', methods=["GET", "POST"])
def mine_view():
    if request.method == "GET":
        # 从session取出当前微信用户openid，查询mongodb数据库获得用户信息
        openid = session["openid"]
        user = mdb.search_user(openid)
        return render_template("mine.html", user_info=user)


# 我的订单
@signature_bp.route('/my_order', methods=["GET", "POST"])
def my_order_view():
    return render_template("my_order.html")


# 我的地址
@signature_bp.route('/address', methods=["GET", "POST"])
def address_view():
    return render_template("address.html")


# 客服中心
@signature_bp.route('/link', methods=["GET", "POST"])
def link_view():
    return render_template("link.html", imageurl=SERVER_IP + "linkQR.jpg")


# 待付款
@signature_bp.route('/my_order_pay', methods=["GET", "POST"])
def my_order_pay_view():
    return render_template("my_order_pay.html")


# 待配送
@signature_bp.route('/my_order_delivery', methods=["GET", "POST"])
def my_order_delivery_view():
    return render_template("my_order_delivery.html")


# 退款/售后
@signature_bp.route('/order_back', methods=["GET", "POST"])
def order_back_view():
    return render_template("order_back.html")


# 留言
@signature_bp.route('/message', methods=["GET", "POST"])
def order_view():
    if request.method == "GET":
        return render_template("message.html")
    else:
        message = request.values.get("message")
        openid = session["openid"]
        t = time.strftime('%Y.%m.%d %H:%M:%S')
        # 保存至数据库
        mdb.insert_message({"openid": openid, "message": message, "date": t})
        return jsonify({"info": "ok"})

import time

from bson import ObjectId
from flask import Blueprint, request, render_template, session, jsonify, url_for, redirect

# 个人信息与订单有关
from utils import mongodb
from utils.config import SERVER_IP

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
    if request.method == "GET":
        # 从数据库查询所有订单
        orders = mdb.search_orders({"order_openid": session["openid"]})
        order_list = []
        for order in orders:
            order_list.append(order)
        return render_template("my_order.html", order_list=order_list)
    else:
        order_id = request.values.get("order_id")
        condition = {"_id": ObjectId(order_id), "order_openid": session["openid"]}
        mdb.delete_order_one(condition=condition)
        return jsonify({"info": "ok"})


# 我的地址
@signature_bp.route('/address', methods=["GET", "POST"])
def address_view():
    # 查询数据库获得所有地址
    address_list = []
    openid = session["openid"]
    addresses = mdb.search_addresses({"openid": openid})
    for address in addresses:
        address_list.append(address)
    return render_template("address.html", address_list=address_list)


# 添加地址
@signature_bp.route('/address/form', methods=["GET", "POST"])
def address_form_view():
    if request.method == "GET":
        # 接受参数判断是新增地址还是修改地址
        a_id = request.values.get("a_id", default="").strip()
        address = ""
        if a_id != "":
            openid = session["openid"]
            condition = {"openid": openid, "_id": ObjectId(a_id)}
            address = mdb.search_address(condition=condition)
        return render_template("address_form.html", address=address)

    else:
        openid = session["openid"]
        a_id = request.form.get("a_id").strip()  # 在Mongodb数据库中的id
        a_name = request.form.get("a_name")
        a_phone = request.form.get("a_phone")
        a_postcode = request.form.get("a_postcode")
        province = request.form.get("province")
        city = request.form.get("city")
        district = request.form.get("district")
        a_address = request.form.get("a_address")
        # 如果a_id不为空，则是修改地址，否则是新增地址
        if a_id == "":
            active = ""
            # 查看数据库是否有默认地址，没有则此条为默认地址
            active_address = mdb.search_address({"openid": openid, "active": "active"})
            if not active_address:
                active = "active"
            content = {"openid": openid,
                       "a_name": a_name,
                       "a_phone": a_phone,
                       "a_postcode": a_postcode,
                       "province": province,
                       "city": city,
                       "district": district,
                       "a_address": a_address,
                       "active": active}
            mdb.insert_address(content=content)
        else:
            condition = {"openid": openid, "_id": ObjectId(a_id)}
            edit = {"a_name": a_name,
                    "a_phone": a_phone,
                    "a_postcode": a_postcode,
                    "province": province,
                    "city": city,
                    "district": district,
                    "a_address": a_address}
            mdb.update_address(condition=condition, edit=edit)
        return jsonify({"info": "ok"})


# 删除地址
@signature_bp.route('/address/delete', methods=["GET", "POST"])
def address_delete_view():
    if request.method == "GET":
        a_id = request.values.get("a_id")
        openid = session["openid"]
        condition = {"_id": ObjectId(a_id), "openid": openid}
        mdb.delete_address_one(condition=condition)
        # 删除后如果数据库只有一条记录则默认为默认地址
        if mdb.address_count() == 1:
            mdb.update_address({"openid": openid}, {"active": "active"})
        return redirect("/address")


# 客服中心
@signature_bp.route('/link', methods=["GET", "POST"])
def link_view():
    return render_template("link.html", imageurl=SERVER_IP + "linkQR.jpg")


# 从数据库查询所有未付款订单

# 待付款
@signature_bp.route('/my_order_pay', methods=["GET", "POST"])
def my_order_pay_view():
    if request.method == "GET":
        orders = mdb.search_orders({"order_openid": session["openid"], "order_status": 0})
        order_list = []
        for order in orders:
            order_list.append(order)
        return render_template("my_order_pay.html", order_list=order_list)


# 待收货
@signature_bp.route('/my_order_delivery', methods=["GET", "POST"])
def my_order_delivery_view():
    if request.method == "GET":
        orders = mdb.search_orders({"order_openid": session["openid"], "order_status": 2})
        order_list = []
        for order in orders:
            order_list.append(order)
        return render_template("my_order_delivery.html", order_list=order_list)


# 退款/售后
@signature_bp.route('/order_back', methods=["GET", "POST"])
def order_back_view():
    # TODO 此功能暂不实现
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

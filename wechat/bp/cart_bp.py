from bson import ObjectId
from flask import Blueprint, request, render_template, jsonify, session

from utils import mongodb

# 购物车
from utils.util import check_image, get_order_code

cart_bp = Blueprint('cart_blueprint', __name__)
# 创建mongodb连接
mdb = mongodb.Mongodb()


# 进入购物车
@cart_bp.route('/cart', methods=["GET", "POST"])
def cart_view():
    if request.method == "GET":
        openid = session["openid"]
        carts = mdb.search_carts({"openid": openid})
        cart_list = []
        for cart in carts:
            cart_list.append(cart)
        return render_template("cart.html", cart_list=cart_list)
    else:
        # 处理购物车新增或修改数据
        book_name = request.values.get("book_name")
        book_writer = request.values.get("book_writer")
        book_press = request.values.get("book_press")
        book_image1 = request.values.get("book_image1", default="")
        book_price = request.values.get("book_price", default="")
        count = request.values.get("count")
        openid = session["openid"]
        # 看数据库是否存在此用户相同的订单，如果存在则更新数据即可
        condition = {"openid": openid, "book_name": book_name, "book_writer": book_writer,
                     "book_press": book_press}
        cart = mdb.search_cart(condition)
        if not cart:
            # 保存至数据库
            content = {"openid": openid, "book_name": book_name, "book_writer": book_writer, "book_price": book_price,
                       "book_press": book_press, "book_image1": book_image1, "count": count}

            mdb.insert_cart(content=content)
        else:  # 更新
            edit = {"count": count}
            mdb.update_cart(condition=condition, edit=edit)
        return jsonify({"info": "ok"})


@cart_bp.route('/cart/remove', methods=["GET", "POST"])
def cart_rm_view():
    openid = session["openid"]
    if request.method == "GET":
        book_name = request.values.get("book_name")
        book_writer = request.values.get("book_writer")
        book_press = request.values.get("book_press")
        condition = {"openid": openid, "book_name": book_name, "book_writer": book_writer,
                     "book_press": book_press}
        # 删除此条购物车信息
        mdb.delete_cart_one(condition)
    else:
        # 删除此用户所有购物车信息
        mdb.delete_cart_many({"openid": openid})
    return jsonify({"info": "ok"})


# 立即购买
@cart_bp.route('/order', methods=["GET", "POST"])
def order_view():
    # 从数据库查询所有地址信息返回
    addresses = mdb.search_addresses(condition={"openid": session["openid"]})
    address_list = []
    active_address = ""
    for address in addresses:
        if address["active"] == "active":
            active_address = address
        address_list.append(address)
    if request.method == "GET":
        book_name = request.values.get("book_name", default="").replace("*******", "+")
        book_writer = request.values.get("book_writer", default="").replace("*******", "+")
        book_press = request.values.get("book_press", default="").replace("*******", "+")
        # 查询书籍返回页面
        condition = {"book_name": book_name, "book_writer": book_writer, "book_press": book_press}
        book = mdb.search_one(condition)
        book_list = []
        if book:
            book = check_image(book)
            book["count"] = 1
            book_list.append(book)
            return render_template("order.html", book_list=book_list, active_address=active_address,
                                   address_list=address_list)
        else:
            return "书籍不存在或已从仓库移除"
    else:
        lis = request.form.get("list").split("&&&&")
        book_list = []
        for li in lis:
            if li != "":
                book_dict = {}
                arr = li.split("&$")
                book_dict["book_name"] = arr[0]
                book_dict["book_writer"] = arr[1]
                book_dict["book_press"] = arr[2]
                book_dict["book_image1"] = arr[3]
                book_dict["book_count"] = arr[4]
                book_dict["book_price"] = arr[5]
                book_dict["cart_id"] = arr[6]
                book_list.append(book_dict)
        return render_template("order.html", book_list=book_list, active_address=active_address,
                               address_list=address_list)


# 付款
@cart_bp.route('/pay', methods=["GET", "POST"])
def pay_view():
    if request.method == "GET":
        openid = session["openid"]
        address_id = request.values.get("address_info")
        book_info = eval(request.values.get("book_info"))
        message = request.values.get("message")
        order_code = request.values.get("order_code")
        submit = request.values.get("submit")
        # 计算总价格
        total_price = 0
        for book in book_info:
            book_name = book["book_name"].replace("*******", "+")
            book_writer = book["book_writer"].replace("*******", "+")
            book_press = book["book_press"].replace("*******", "+")
            book_count = int(book["book_count"])
            cart_id = book["cart_id"]
            # 根据信息查询数据库获取价格信息
            condition = {"book_name": book_name, "book_writer": book_writer, "book_press": book_press}
            book_price = float(mdb.search_one(condition=condition)["book_price"])
            total_price += book_count * book_price
            # 从购物车中删除此条信息
            if cart_id.strip() != "":
                condition = {"openid": openid, "_id": ObjectId(cart_id)}
                mdb.delete_cart_one(condition=condition)
        # 根据地址id查询订单地址详情
        condition = {"openid": openid, "_id": ObjectId(address_id)}
        address = mdb.search_address(condition=condition)
        if submit == "True":  # 判断是否需要提交订单
            # 将数据存储到mongodb数据库订单表
            # 生成订单号
            order_code = get_order_code()
            content = {"order_openid": openid,
                       "order_code": order_code,
                       "order_address": address,
                       "order_book": book_info,
                       "order_status": 0,
                       "order_message": message,
                       "order_price": total_price,
                       "order_image": book_info[0]["book_image"]}
            mdb.insert_order(content=content)
        return render_template("pay.html", address=address, price=total_price, order_code=order_code)

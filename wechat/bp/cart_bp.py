from flask import Blueprint, request, render_template

from utils import mongodb

# 购物车
cart_bp = Blueprint('cart_blueprint', __name__)
# 创建mongodb连接
mdb = mongodb.Mongodb()


# 进入购物车
@cart_bp.route('/cart', methods=["GET", "POST"])
def cart_view():
    if request.method == "GET":
        return render_template("cart.html")


# 立即购买
@cart_bp.route('/order', methods=["GET", "POST"])
def order_view():
    if request.method == "GET":
        return render_template("order.html")

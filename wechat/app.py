# -*- coding:utf-8 -*-
import os
from urllib.parse import quote

from flask import Flask, request, redirect, session
import hashlib
import xmltodict

from bp.bookinfo_bp import book_info_bp
from bp.cart_bp import cart_bp
from bp.signature_bp import signature_bp
from utils import reply, diy_menu, mongodb, CreateSign
from utils.config import APP_ID, ROOTURL, TOKENSTR
from utils.util import user_handler

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
# 注册蓝图
app.register_blueprint(book_info_bp)
app.register_blueprint(signature_bp)
app.register_blueprint(cart_bp)

# 更新自定义菜单
diy_menu.Menu().create(diy_menu.getMenu())
# 创建mongodb连接
mdb = mongodb.Mongodb()


# 自定义过滤器
def fileter_name(li):
    if li == "未知":
        return "随便看看"
    else:
        return li


def fileter_plus(li):
    return li.replace("+", "*******")

def fileter_plus1(li):
    return li.replace( "*******","+")


def fileter_char(li):
    return li.replace("&lt;", "<").replace("&gt;", ">")


def filter_data(li):
    return li[0:4] + "-" + li[4:6] + "-" + li[6:8]


def filter_status(li):
    if li == 0:
        return "未支付"
    elif li == 1:
        return "已支付"
    elif li == 2:
        return "配送中"
    elif li == 3:
        return "已完成"


def filter_status1(li):
    if li == 0:
        return "red"
    elif li == 1:
        return "green"
    elif li == 2:
        return "red"
    elif li == 3:
        return "green"


app.add_template_filter(fileter_name)
app.add_template_filter(fileter_plus)
app.add_template_filter(fileter_plus1)
app.add_template_filter(fileter_char)
app.add_template_filter(filter_data)
app.add_template_filter(filter_status)
app.add_template_filter(filter_status1)


# 对所有请求进行拦截与预处理
@app.before_request
def get_user_info():
    if request.path != '/user' and request.path != '/':
        if 'openid' not in session:
            ori_url = request.url
            # 你的回调路径
            back_url = quote(ROOTURL + "user")
            url = "http://open.weixin.qq.com/connect/oauth2/authorize?appid=" + APP_ID + "&redirect_uri=" + back_url + "&response_type=code&scope=snsapi_userinfo&state=" + ori_url + "#wechat_redirect"
            return redirect(url)


@app.route('/', methods=["GET", "POST"])
def getinput():
    if request.method == "GET":
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')
        token = TOKENSTR
        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        sha1.update(list[0].encode('utf-8'))
        sha1.update(list[1].encode('utf-8'))
        sha1.update(list[2].encode('utf-8'))
        hashcode = sha1.hexdigest()
        if hashcode == signature:
            print("*****************************************")
            return echostr
        else:
            return ""
    elif request.method == "POST":
        # 表示微信服务器转发消息过来
        xml_str = request.data
        if not xml_str:
            return ""
        # 对xml字符串进行解析
        xml_dict = xmltodict.parse(xml_str)
        xml_dict = xml_dict.get("xml")
        return reply.Reply(xml_dict, mdb).create_content()


@app.route('/user', methods=["GET", "POST"])
def user_view():
    if request.method == "GET":
        try:
            url = request.values.get("state")
            code = request.values.get("code")
            user_info = CreateSign.get_userInfo(code)
            # 将用户openid存储到session，方便每个页面可以调用
            session["openid"] = user_info["openid"]
            # 处理用户信息，若没有保存则保存到mongodb数据库
            user_handler(user_info, mdb)
            return redirect(url)
        except:
            return redirect("http://www.baidu.com")


# 内网穿透命令：1,sunny.exe --clientid=170302220842     2,d129dc91391dbb25    btphxlslrylwgaag
if __name__ == '__main__':
    app.run()

# -*- coding:utf-8 -*-
from urllib.parse import quote

from flask import Flask, request, render_template, jsonify, redirect
import hashlib
import xmltodict

from bp.bookinfo_bp import book_info_bp
from utils import reply, CreateSign, diy_menu, mongodb
from utils.config import APP_ID, ROOTURL, TOKENSTR

app = Flask(__name__)
# 注册蓝图
app.register_blueprint(book_info_bp)

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


app.add_template_filter(fileter_name)
app.add_template_filter(fileter_plus)


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


@app.route('/get_openid', methods=["GET", "POST"])
def get_code_view():
    # 接受参数确定是从哪发来的请求
    state = request.args.get("state")
    # 你的回调路径
    back_url = quote(ROOTURL + "user")
    url = "http://open.weixin.qq.com/connect/oauth2/authorize?appid=" + APP_ID + "&redirect_uri=" + back_url + "&response_type=code&scope=snsapi_userinfo&state=" + str(
        state) + "#wechat_redirect"
    return redirect(url)


# 内网穿透命令：1,sunny.exe --clientid=170302220842     2,d129dc91391dbb25
if __name__ == '__main__':
    app.run()

# -*- coding:utf-8 -*-
from urllib.parse import quote

from flask import Flask, request, render_template, jsonify, redirect
import hashlib
import xmltodict

from utils import reply, CreateSign, diy_menu
from utils.config import APP_ID, ROOTURL

app = Flask(__name__)
# 更新自定义菜单
diy_menu.Menu().create(diy_menu.getMenu())


@app.route('/', methods=["GET", "POST"])
def getinput():
    if request.method == "GET":
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')
        token = "maluguang"
        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        sha1.update(list[0].encode('utf-8'))
        sha1.update(list[1].encode('utf-8'))
        sha1.update(list[2].encode('utf-8'))
        hashcode = sha1.hexdigest()
        if hashcode == signature:
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
        return reply.Reply(xml_dict).create_content()


@app.route('/index', methods=["GET", "POST"], endpoint="index")
def index_view():
    if request.method == "GET":
        code = request.args.get('code')
        state = request.args.get('state')  # 可根据不同的state跳转到不同的页面
        user_info = CreateSign.get_userInfo(code)
        return render_template("index.html")
    else:
        local_url = request.values.get("link")
        appid, timestamp, signature, nonceStr = CreateSign.wx_config(url=local_url)
        return jsonify({'appid': appid, 'timestamp': timestamp, 'signature': signature, 'nonceStr': nonceStr})


@app.route('/get_openid', methods=["GET", "POST"])
def get_code_view():
    # 接受参数确定是从哪发来的请求
    state = request.args.get("state")
    # 你的回调路径
    back_url = quote(ROOTURL + "index")
    url = "http://open.weixin.qq.com/connect/oauth2/authorize?appid=" + APP_ID + "&redirect_uri=" + back_url + "&response_type=code&scope=snsapi_userinfo&state=" + str(
        state) + "#wechat_redirect"
    return redirect(url)


# 内网穿透命令：sunny.exe --clientid=170302220842
if __name__ == '__main__':
    app.run()

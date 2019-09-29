import json
import string
import hashlib
import random
import time
import urllib.request

import redis
import requests

from utils.config import APP_ID, SECRET, REDISIP, REDISPORT

r = redis.Redis(host=REDISIP, port=REDISPORT)  # 创建redis对象


class Sign:
    def __init__(self, jsapi_ticket, url):
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        self.ret['signature'] = hashlib.sha1(string.encode('utf-8')).hexdigest()
        return self.ret


def get__token():
    ACCESS_TOKEN = r.get('ACCESS_TOKEN')  # 从redis中获取ACCESS_TOKEN
    if ACCESS_TOKEN:
        return ACCESS_TOKEN
    try:
        token_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}".format(
            APP_ID, SECRET)  # 创建获取token的url
        response = urllib.request.urlopen(token_url)
        b = response.read().decode('utf-8')
        token = json.loads(b)
        ACCESS_TOKEN = token.get("access_token")
        r.set('ACCESS_TOKEN', ACCESS_TOKEN, ex=7200)  # 将获取到的 ACCESS_TOKEN 存入redis中并且设置过期时间为7200s
        return ACCESS_TOKEN

    except Exception as e:
        return e


def get_ticket():
    ticket = r.get('TICKET')  # 获取redis数据库中ticket
    if ticket:
        tic = str(ticket, encoding='utf-8')
        return tic

    else:
        try:
            token = get__token()
            ticket_url = " https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={}&type=jsapi".format(token)
            get_ticket = urllib.request.urlopen(ticket_url)
            c = get_ticket.read().decode("utf-8")
            js_ticket = json.loads(c)
            ticket = js_ticket.get("ticket")
            r.set('TICKET', ticket, ex=7200)
            return ticket
        except Exception as e:
            return e


def wx_config(url):
    ticket = get_ticket()
    sign = Sign(ticket, url).sign()

    return APP_ID, sign['timestamp'], sign['signature'], sign['nonceStr']


def get_openId(code):
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=' + APP_ID + '&secret=' + SECRET + '&code=' + code + '&grant_type=authorization_code'
    return json.loads(requests.get(url).text)


# 获取微信用户信息
def get_userInfo(code):
    info1 = get_openId(code)
    url = "https://api.weixin.qq.com/sns/userinfo?access_token=" + info1["access_token"] + "&openid=" + info1[
        "openid"] + "&lang=zh_CN"
    user_info = requests.get(url).content.decode("utf-8")
    return json.loads(user_info)

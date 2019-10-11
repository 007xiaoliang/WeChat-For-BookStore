import json
import time

import requests
from urllib import request as re

from utils.config import ROOTURL

WECHAT_APPID = "wx0f367628fac8067e"
WECHAT_APPSECRET = "c3a3d65bc5a7ad0273e3407aa678dfd6"
WECHAT_TOKEN = "maluguang"


class AccessToken(object):
    access_token = {
        "access_token": "",
        "update_time": time.time(),
        "expires_in": 7200
    }

    @classmethod
    def get_access_token(cls):
        if not cls.access_token.get('access_token') or (
                time.time() - cls.access_token.get('update_time') > cls.access_token.get('expires_in')):
            url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
                WECHAT_APPID, WECHAT_APPSECRET)
            response = re.urlopen(url).read()
            resp_json = json.loads(response)
            if 'errcode' in resp_json:
                raise Exception(resp_json.get('errmsg'))
            else:
                cls.access_token['access_token'] = resp_json.get('access_token')
                cls.access_token['expires_in'] = resp_json.get('expires_in')
                cls.access_token['update_time'] = time.time()
                return cls.access_token.get('access_token')
        else:
            return cls.access_token.get('access_token')


class Menu(object):
    def create(self, post_data):
        p = json.dumps(post_data, ensure_ascii=False)
        post_url = ' https://api.weixin.qq.com/cgi-bin/menu/create?access_token={}'.format(
            AccessToken.get_access_token())
        req = requests.post(post_url, p.encode('utf-8'))


def getMenu():
    postJson = {
        "button": [
            {
                "type": "click",
                "name": "历史",
                "key": "V1001_HISTORY"
            },
            {
                "name": "商城",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "商城主页",
                        "url": ROOTURL + "index"
                    },
                    {
                        "type": "view",
                        "name": "我的订单",
                        "url": ROOTURL + "my_order"
                    }
                ]
            },
            {
                "name": "联系我们",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "留言",
                        "url": ROOTURL + "message"
                    },
                    {
                        "type": "view",
                        "name": "联系方式",
                        "url": ROOTURL + "link"
                    }
                ]
            }
        ]
    }
    return postJson

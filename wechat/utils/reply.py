import time

import xmltodict

from utils import mongodb
from utils.config import ROOTURL


class Reply:
    def __init__(self, xml_dict):
        self.xml = xml_dict
        self.return_content = ''
        self.content = ""
        self.resp_dict = {
            "xml": {
                "ToUserName": self.xml.get("FromUserName"),
                "FromUserName": self.xml.get("ToUserName"),
                "CreateTime": int(time.time()),
                "MsgType": "text",
                "Content": "",
            }
        }
        # 创建mongodb连接
        self.mdb = mongodb.Mongodb()

    def create_content(self):
        # 提取消息类型
        msg_type = self.xml.get("MsgType")
        if msg_type == "text":
            # 表示发送的是文本消息
            # 去mongodb数据库查询相关书籍，并返回相关的内容
            self.content = self.mdb.search(self.xml.get("Content"))
        elif msg_type == "event":
            event_type = self.xml.get("Event")
            if event_type == "subscribe":
                self.content = "欢迎订阅,我们等您好久了\n回复 书名 可查询\n" \
                               "<a href='"+ROOTURL+"get_openid?state=1'>点击进入商城</a>"
            elif event_type == "unsubscribe":
                print("取消关注")
            else:
                eventkey = self.xml.get("EventKey")
                if eventkey == "V1001_HISTORY":
                    self.content = "查询历史入口"
        else:
            self.content = "回复 <a>书名</a> 可查询"
        self.resp_dict['xml']['Content'] = self.content
        return_content = xmltodict.unparse(self.resp_dict)
        # 返回消息数据给微信服务器
        return return_content

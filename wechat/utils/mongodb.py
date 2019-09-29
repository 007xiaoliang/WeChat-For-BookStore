from pymongo import MongoClient

# 开启linux中mongodb服务： ./mongod -f mongodb.conf
from utils.config import MONGOIP, MONGOPORT, MONGOUSER, MONGOPWD


class Mongodb:
    def __init__(self):
        self.conn = MongoClient(MONGOIP + ':' + MONGOPORT)
        self.db = self.conn.wechat  # 连接wechat数据库，没有则自动创建
        self.db.authenticate(MONGOUSER, MONGOPWD)
        self.collection = self.db.book_set  # 书籍信息存储到book_set表中

    # 根据书名查询
    def search(self, keyword):
        flag = True
        content = "查询结果如下:\n*****\n"
        for u in self.collection.find({'book_name': {'$regex': keyword}}, {"id": 0}):
            if flag:
                flag = False
            content += "书名:" + u["book_name"] + "\n" +\
                       "作者:" + u["book_writer"] + "\n" +\
                       "出版社:" + u["book_press"] + "\n*****\n"
        if flag:
            return "没有查询到与 " + keyword + " 有关的内容"
        return content

    # 关闭连接
    def close(self):
        self.conn.close()


if __name__ == '__main__':
    print(Mongodb().search("仙55"))

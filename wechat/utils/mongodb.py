from pymongo import MongoClient

# 开启linux中mongodb服务： ./mongod -f mongodb.conf
from utils.config import MONGOIP, MONGOPORT, MONGOUSER, MONGOPWD, SERVER_IP, ROOTURL


class Mongodb:
    def __init__(self):
        self.conn = MongoClient(MONGOIP + ':' + MONGOPORT)
        self.db = self.conn.wechat  # 连接wechat数据库，没有则自动创建
        self.db.authenticate(MONGOUSER, MONGOPWD)
        self.collection1 = self.db.book_set  # 操作book_set表
        self.collection2 = self.db.category_set  # 操作category_set表
        self.collection3 = self.db.lunbo_set  # 操作lunbo_set表

    # 根据书名查询
    def search_like(self, keyword):
        return self.collection1.find({'book_name': {'$regex': keyword}}, {"id": 0})

    # 查询所有分类信息并返回
    def search_category(self):
        return self.collection2.find({}, {"_id": 0})

    # 查询轮播图信息并返回
    def search_lunbo(self):
        lunbo_info = self.collection3.find_one({"id": 1}, {"_id": 0, "id": 0})
        lunbo_list = []
        for value in lunbo_info.values():
            if value is not "":
                lunbo_list.append(SERVER_IP + value)
        return lunbo_list

    # 关闭连接
    def close(self):
        self.conn.close()


if __name__ == '__main__':
    print(Mongodb().search("仙55"))

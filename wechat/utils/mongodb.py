import random

from pymongo import MongoClient

# 开启linux中mongodb服务： ./mongod -f mongodb.conf
from utils.config import MONGOIP, MONGOPORT, MONGOUSER, MONGOPWD, SERVER_IP, ROOTURL
from utils.util import check_image


class Mongodb:
    def __init__(self):
        self.conn = MongoClient(MONGOIP + ':' + MONGOPORT)
        self.db = self.conn.wechat  # 连接wechat数据库，没有则自动创建
        self.db.authenticate(MONGOUSER, MONGOPWD)
        self.collection1 = self.db.book_set  # 操作book_set表
        self.collection2 = self.db.category_set  # 操作category_set表
        self.collection3 = self.db.lunbo_set  # 操作lunbo_set表
        self.collection4 = self.db.user_set  # 操作user_set表
        self.collection5 = self.db.message_set  # 操作message_set表(留言表)
        self.collection6 = self.db.cart_set  # 操作cart_set表(购物车表)
        self.collection7 = self.db.address_set  # 操作address_set表(地址表)
        self.collection8 = self.db.order_set  # 操作order_set表(订单表，分为(未付款/0，已付款/1，配送中/2，已完成/3)几种状态)

    # 计数
    def count(self):
        count = self.collection1.count_documents({})
        return count

    # 根据条件查询
    def search(self, condition):
        return self.collection1.find(condition)

    # 根据条件查询一条
    def search_one(self, condition):
        return self.collection1.find_one(condition, {"_id": 0})

    # 随机查询某类型下五条数据
    def search_one_random(self, query_filter=None):
        if self.count() >= 5:
            limit = 5
            skip = random.randint(0, self.count() - 5)
        else:
            skip, limit = self.count()
        return self.collection1.find(query_filter, {"_id": 0}).limit(limit).skip(skip)

    # 分页查询
    def query_search(self, query_filter=None, limit=7, skip=1):
        return self.collection1.find(query_filter, {"_id": 0}).limit(limit).skip((skip - 1) * limit)

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

    # 查询展示页面需要的信息
    def main_search(self):
        cate_info = []
        try:
            for cate in self.search_one_random():
                cate = check_image(cate)
                cate_info.append(cate)
        except Exception as e:
            print(e)
            cate_info = ["数据丢失"]
        finally:
            return cate_info

    # 关键字搜索
    def search_in_keyword(self, keyword):
        query_filter = {"$or": [{"book_name": {'$regex': keyword}}, {"book_writer": {'$regex': keyword}},
                                {"book_press": {'$regex': keyword}}, {"book_induction": {'$regex': keyword}},
                                {"book_type1": {'$regex': keyword}}, {"book_type2": {'$regex': keyword}},
                                {"book_press_time": {'$regex': keyword}}, {"book_image1": {'$regex': keyword}}]}
        search_info = self.collection1.find(query_filter, {"_id": 0})
        info_list = []
        count = 0
        for info in search_info:
            count += 1
            info_list.append(check_image(info))
        return count, info_list

    # 查询user_set表
    def search_user(self, openid):
        return self.collection4.find_one({"openid": openid}, {"_id": 0})

    # 插入用户信息
    def insert_user(self, content):
        self.collection4.insert_one(content)

    # 查询message_set表
    def search_message(self, condition):
        return self.collection5.find_one(condition, {"_id": 0})

    # 插入留言信息
    def insert_message(self, content):
        self.collection5.insert_one(content)

    # 查询cart_set表一条
    def search_cart(self, condition):
        return self.collection6.find_one(condition, {"_id": 0})

    # 查询cart_set表多条
    def search_carts(self, condition):
        return self.collection6.find(condition)

    # 插入cart信息
    def insert_cart(self, content):
        self.collection6.insert_one(content)

    # 更新cart数据
    def update_cart(self, condition, edit):
        self.collection6.update_one(condition, {'$set': edit})

    # 删除购物车一条数据
    def delete_cart_one(self, condition):
        self.collection6.delete_one(condition)

    # 删除购物车多条数据
    def delete_cart_many(self, condition):
        self.collection6.delete_many(condition)

    # 查询address_set表一条
    def search_address(self, condition):
        return self.collection7.find_one(condition)

    # 查询address_set表多条
    def search_addresses(self, condition):
        return self.collection7.find(condition)

    # 插入address信息
    def insert_address(self, content):
        self.collection7.insert_one(content)

    # 更新address数据
    def update_address(self, condition, edit):
        self.collection7.update_one(condition, {'$set': edit})

    # 删除address一条数据
    def delete_address_one(self, condition):
        self.collection7.delete_one(condition)

    # 计数
    def address_count(self):
        count = self.collection7.count_documents({})
        return count

    # 插入订单表信息
    def insert_order(self, content):
        self.collection8.insert_one(content)

    # 删除订单一条数据
    def delete_order_one(self, condition):
        self.collection8.delete_one(condition)

    # 查询order_set表多条
    def search_orders(self, condition):
        return self.collection8.find(condition)


if __name__ == '__main__':
    print(Mongodb().delete_cart_one({"_id":"5da1e2fa91ed8bc750660bd5","openid": "oXjxxwiTZnOBGxNi2Z5PTMw0Pe5I"}))

from pymongo import MongoClient

# 开启linux中mongodb服务： ./mongod -f mongodb.conf
from utils.config import MONGOIP, MONGOPORT, MONGOUSER, MONGOPWD


class Mongodb:
    def __init__(self):
        self.conn = MongoClient(MONGOIP + ':' + MONGOPORT)
        self.db = self.conn.wechat  # 连接wechat数据库，没有则自动创建
        self.db.authenticate(MONGOUSER, MONGOPWD)
        self.collection1 = self.db.book_set  # 操作book_set表
        self.collection2 = self.db.lunbo_set  # 操作lunbo_set表】
        self.collection3 = self.db.category_set  # 操作category_set表
        self.collection4 = self.db.user_set  # 操作user_set表
        self.collection5 = self.db.message_set  # 操作message_set表(留言表)
        self.collection6 = self.db.cart_set  # 操作cart_set表(购物车表)
        self.collection7 = self.db.address_set  # 操作address_set表(地址表)
        self.collection8 = self.db.order_set  # 操作order_set表(订单表，分为(未付款/0，已付款/1，配送中/2，已完成/3)几种状态)

    # 插入数据 insert_many(items,ordered=False)
    def insert(self, content):
        ret = self.collection1.insert_one(content)
        return ret.inserted_id

    # 插入多条
    def insert_many(self, content):
        self.collection1.insert_many(content, ordered=False)

    # 更新数据
    def update(self, condition, edit):
        self.collection1.update_one(condition, {'$set': edit})

    # 查询所有(book_set)
    def search(self, condition1, conditon2=None):
        info = self.collection1.find(condition1, conditon2)
        return info

    def search_like(self, keyword):
        info = self.collection1.find({'book_name': {'$regex': keyword}}, {"id": 0})
        return info

    # 查询一条(book_set)
    def search_one(self, condition1, conditon2=None):
        info = self.collection1.find_one(condition1, conditon2)
        return info

    # 查询（lunbo_set）
    def search_lunbo_set(self, condition1, conditon2=None):
        info = self.collection2.find_one(condition1, conditon2)
        return info

    # 查询(category_set)
    def search_category_set(self):
        info = self.collection3.find({}, {"_id": 0})
        return info

    # 计数
    def count(self):
        count = self.collection1.count_documents({})
        return count

    # 计数(order_set)
    def count_order(self, condition):
        count = self.collection8.count_documents(condition)
        return count

    # 分页查询
    def page_query(self, query_filter=None, page_size=10, page_now=1):
        skip = page_size * (page_now - 1)
        return self.collection1.find(query_filter).limit(page_size).skip(skip)

    # 删除数据
    def delete(self, condition):
        ret = self.collection1.delete_one(condition)

    # 更新轮播图信息
    def update_lunbo(self, condition, edit):
        res = self.collection2.find_one(condition)
        if res is None:  # 第一次插入轮播图信息
            self.collection2.insert_one(edit)
        else:  # 后期修改轮播图信息
            self.collection2.update_one(condition, {'$set': edit})

    # 书籍分类信息插入
    def insert_category(self, content):
        ret = self.collection3.insert_one(content)

    # 清空表
    def drop_category_set(self):
        self.collection3.drop()

    # 查询所有(order_set)
    def search_orders(self, condition):
        return self.collection8.find(condition, {"_id": 0})

    # 查询一条(order_set)
    def search_order(self, condition):
        return self.collection8.find_one(condition)

    # 分页查询(order_set)
    def page_query_order(self, query_filter=None, page_size=10, page_now=1):
        skip = page_size * (page_now - 1)
        return self.collection8.find(query_filter).limit(page_size).skip(skip)

    # 更新order状态
    def update_order(self, condition, edit):
        self.collection8.update_one(condition, {'$set': edit})

    # 关闭连接
    def close(self):
        self.conn.close()


if __name__ == '__main__':
    print(Mongodb().search_order({"order_code":'201610151700422943994'}))
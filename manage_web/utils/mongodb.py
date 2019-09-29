from pymongo import MongoClient

# 开启linux中mongodb服务： ./mongod -f mongodb.conf
from utils.config import MONGOIP, MONGOPORT, MONGOUSER, MONGOPWD


class Mongodb:
    def __init__(self):
        self.conn = MongoClient(MONGOIP + ':' + MONGOPORT)
        self.db = self.conn.wechat  # 连接wechat数据库，没有则自动创建
        self.db.authenticate(MONGOUSER, MONGOPWD)
        self.collection1 = self.db.book_set  # 书籍信息存储到book_set表中
        self.collection2 = self.db.lunbo_set  # 轮播图存储到lunbo_set表中
        self.collection3 = self.db.category_set  # 书籍分类信息存储到category_set表中

    # 插入数据
    def insert(self, content):
        ret = self.collection1.insert_one(content)
        return ret.inserted_id

    # 更新数据
    def update(self, condition, edit):
        self.collection1.update_one(condition, {'$set': edit})

    # 查询所有(book_set)
    def search(self, condition1, conditon2=None):
        info = self.collection1.find(condition1, conditon2)
        return info
        # 查询(book_set)

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
        info = self.collection3.find({},{"_id":0 })
        return info

    # 计数
    def count(self):
        count = self.collection1.count_documents({})
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

    # 关闭连接
    def close(self):
        self.conn.close()

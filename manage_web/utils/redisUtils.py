import redis

# linux开启redis服务  redis-server redis.conf
from utils.config import LINUXIP


class RedisClient:
    def __init__(self):
        self.r = redis.Redis(host=LINUXIP, port=6379, db=2)  # 创建redis对象,使用redis第二个数据库

    # 插入数据
    def insert(self, key, value):
        self.r.set(key, value, ex=3600)

    # 查询数据,没有返回None
    def search(self, key):
        return self.r.get(key)

    # 删除数据
    def delete(self, key):
        self.r.delete(key)


if __name__ == '__main__':  # ./sunny --clientid=170302220842
    print(RedisClient().search("haha"))

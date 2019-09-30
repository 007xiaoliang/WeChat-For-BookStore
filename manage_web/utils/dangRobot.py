import random

from lxml import etree

import requests

from utils import mongodb


class Robot:
    def __init__(self, id, url):
        self.book_info = []
        self.id = id
        self.url = url
        self.mdb = mongodb.Mongodb()

    # 根据传入参数从当当网爬取相关数据
    def search_info(self):
        if self.id == 1:
            html = self.request_dandan(self.url)
            self.parse_result1(html)
        elif self.id == 2:
            for i in range(3, 8):
                html = self.request_dandan(self.url + str(i))
                self.parse_result2(html)  # 解析过滤我们想要的信息
        return self.book_info

    def request_dandan(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
        except requests.RequestException:
            return None

    def parse_result1(self, html):
        # 建立html的树
        tree = etree.HTML(html)
        # 提取节点
        pic = "//div[@id='search_nature_rg']/ul/li/a/img/@data-original"
        name = "//div[@id='search_nature_rg']/ul/li/a/@title"
        writer = "//p[@class='search_book_author']/span[1]/a/@title"
        press = "//p[@class='search_book_author']/span[3]/a/text()"
        press_time = "//p[@class='search_book_author']/span[2]/text()"
        induction = "//p[@class='detail']/text()"
        price = "///span[@class='search_now_price']/text()"
        book_image1 = tree.xpath(pic)
        book_name = tree.xpath(name)
        book_writer = tree.xpath(writer)
        book_press = tree.xpath(press)
        book_press_time = tree.xpath(press_time)
        book_induction = tree.xpath(induction)
        book_price = tree.xpath(price)
        les = 5 if len(book_name) > 5 else len(book_name)  # 默认显示搜索前五条结果
        for x in range(les):
            boo_dict = {"book_name": book_name[x],
                        "book_writer": book_writer[x],
                        "book_press": book_press[x],
                        "book_press_time": book_press_time[x].replace("/", ""),
                        "book_induction": book_induction[x],
                        "book_price": book_price[x].replace("¥", ""),
                        "book_type1": "未知",
                        "book_type2": "",
                        "book_image1": book_image1[x]
                        }
            self.book_info.append(boo_dict)

    def parse_result2(self, html):
        # 获取分类信息
        cate_list = self.get_cate_info()
        # 建立html的树
        tree = etree.HTML(html)
        # 提取节点
        pic = "//ul[@class='bang_list clearfix bang_list_mode']/li/div[@class='pic']/a/img/@src"
        name = "//ul[@class='bang_list clearfix bang_list_mode']/li/div[@class='name']/a/text()"
        writer = "//ul[@class='bang_list clearfix bang_list_mode']/li/div[@class='publisher_info'][1]/a[1]/@title"
        press = "//ul[@class='bang_list clearfix bang_list_mode']/li/div[@class='publisher_info'][2]/a/text()"
        press_time = "//ul[@class='bang_list clearfix bang_list_mode']/li/div[@class='publisher_info'][2]/span/text()"
        price = "//span[@class='price_n']/text()"
        book_image1 = tree.xpath(pic)
        book_name = tree.xpath(name)
        book_writer = tree.xpath(writer)
        book_press = tree.xpath(press)
        book_press_time = tree.xpath(press_time)
        book_price = tree.xpath(price)
        for x in range(20):
            t1 = random.randint(0, len(cate_list) - 1)  # 一级类名坐标
            book_type1 = cate_list[t1][0]
            if t1 != 0:
                t2 = random.randint(1, len(cate_list[t1]) - 1)  # 二级类名坐标
                book_type2 = cate_list[t1][t2]
            else:
                book_type2 = ""
            boo_dict = {"book_name": book_name[x].split('（')[0].split("(")[0],
                        "book_writer": book_writer[x],
                        "book_press": book_press[x],
                        "book_press_time": book_press_time[x],
                        "book_induction": "暂无介绍",
                        "book_price": book_price[x].replace("¥", ""),
                        "book_type1": book_type1,
                        "book_type2": book_type2,
                        "book_image1": book_image1[x]
                        }
            self.book_info.append(boo_dict)

    def get_cate_info(self):
        cate_list = []
        for cate in self.mdb.search_category_set():
            arr = []
            for value in cate.values():
                arr.append(value)
            cate_list.append(arr)
        return cate_list


if __name__ == '__main__':
    info = Robot(1, "http://search.dangdang.com/?key=诛仙&act=input").search_info()
    print(info)

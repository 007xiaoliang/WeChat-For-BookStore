import time

from utils.config import SERVER_IP


# 检查图片路径
def check_image(cate):
    if "book_image1" in cate.keys() and cate['book_image1'] != "":
        if "http" not in cate['book_image1']:
            cate['book_image1'] = SERVER_IP + cate['book_image1']
    else:
        cate['book_image1'] = SERVER_IP + "未上传.jpg"
    return cate


# 处理用户信息
def user_handler(user_info, mdb):
    # 根据openid查询数据库，如果没有相关用户则保存信息，有的话将数据返回
    user = mdb.search_user(user_info["openid"])
    if not user:
        content = {'openid': user_info["openid"],
                   'nickname': user_info["nickname"],
                   'sex': user_info["sex"],
                   'language': user_info["language"],
                   'city': user_info["city"],
                   'province': user_info["province"],
                   'country': user_info["country"],
                   'headimgurl': user_info["headimgurl"]}
        mdb.insert_user(content)


# 生成订单号
def get_order_code():
    order_no = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))) + str(time.time()).replace('.', '')[-7:]
    return order_no


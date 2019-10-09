from utils.config import SERVER_IP


# 检查图片路径
def check_image(cate):
    if "book_image1" in cate.keys() and cate['book_image1'] != "":
        if "http" not in cate['book_image1']:
            cate['book_image1'] = SERVER_IP + cate['book_image1']
    else:
        cate['book_image1'] = SERVER_IP + "未上传.jpg"
    return cate

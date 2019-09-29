import os

from utils import connectionLinux
from utils.config import LOCAL_ADDR
from utils.md5AndSalt import data_to_md5

linux = connectionLinux.LinuxConn()  # linux连接


# 存储图片到服务器
def save_image(book_image_id, book_image):
    """
    :param book_image_id:图片唯一性标志，轮播图为book_image_id,图书为书名+作者+出版社
    :param book_image: 上传的图片对象
    :return: 返回生成的文件名
    """
    image_name = str(data_to_md5(book_image_id)) + '.' + book_image.filename.split('.')[-1]
    local_image_url = LOCAL_ADDR + image_name
    book_image.save(local_image_url)
    linux.ssh_scp_put(local_image_url, image_name)
    os.remove(local_image_url)
    return image_name

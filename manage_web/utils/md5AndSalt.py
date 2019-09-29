import hashlib


# 对密码进行MD5加密
def data_to_md5(password):
    salt = 'qweasd'.encode()
    password = password.encode() + salt
    result = hashlib.md5(password)
    return result.hexdigest()

import os

# 同步两个文件夹里内容
from utils import md5AndSalt


def sync_file(paths, patht):
    copy_file(paths, patht)
    copy_file(patht, paths)


def copy_file(paths, patht):
    for filename in os.listdir(paths):
        filename_s = paths + os.sep + filename
        filename_t = patht + os.sep + filename
        if os.path.isdir(filename_s):
            if not os.path.exists(filename_t):
                os.mkdir(filename_t)
            copy_file(filename_s, filename_t)
        else:
            if not os.path.exists(filename_t):
                with open(filename_s, 'rb') as f_s:
                    with open(filename_t, 'wb') as f_t:
                        f_t.write(f_s.read())

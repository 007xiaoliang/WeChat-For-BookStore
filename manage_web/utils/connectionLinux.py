# coding utf-8

import paramiko

# 创建SSHClient实例对象
from utils.config import LINUXIP, LINUXU, LINUXP, NGIX_ADDR


class LinuxConn:
    def __init__(self):
        self.ssh = paramiko.SSHClient()
        # 调用方法，标识没有远程机器的公钥，允许访问
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接远程机器 地址端口用户名密码
        self.ssh.connect(LINUXIP, 22, LINUXU, LINUXP)

    # 创建目录
    def delete_img(self, dic, key, remote_file=NGIX_ADDR):
        if dic is not None and key in dic.keys():
            filename = dic[key]
            if filename is not None and filename is not "" and filename is not "未上传.jpg":
                self.ssh.exec_command("rm " + remote_file + filename)

    def ssh_scp_put(self, local_file, filename, remote_file=NGIX_ADDR):
        """
        :param local_file:
        :param remote_file: 要上传的文件地址（例：/test.txt）
        :return:
        """
        sftp = self.ssh.open_sftp()
        sftp.put(local_file, remote_file + filename)

    # 关闭连接
    def close(self):
        self.ssh.close()


if __name__ == '__main__':
    file = "C:/Users/MY/Pictures/Saved Pictures/桌面4.jpg"
    des = "/software/nginx-1.12.0/html/static/img/2.jpg"

    LinuxConn().ssh_scp_put(file, des)

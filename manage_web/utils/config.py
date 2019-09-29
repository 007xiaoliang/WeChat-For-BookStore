import os

# linux查看防火墙对外开放了哪些端口：iptables -L -n      firewall-cmd --list-ports
# linux查看某端口是否开放：firewall-cmd --query-port=8080/tcp
# linux永久开放端口：firewall-cmd --zone=public --add-port=8080/tcp --permanent
# linux重启防火墙： firewall-cmd --reload
# 移除开放的8080端口： firewall - cmd - -permanent - -zone = public - -remove - port = 8080 / tcp
# 移除开放端口后也应重启防火墙。
# 查看防火墙状态： systemctl status firewalld.service
# 启动 | 关闭 | 重启防火墙 ： systemctl[start | stop | restart] firewalld.service
# 查看nginx进程号：ps -ef | grep nginx
# 关闭nginx：kill -QUIT 3502 // nginx -s stop
# 启动MySQL数据库：systemctl start  mysqld.service
# 重启MySQL数据库：systemctl restart mysqld


# 项目配置参数信息
# ----------------------------------------------------------
# linux服务器地址,用户名，密码
LINUXIP = "192.168.30.135"
LINUXU = "root"
LINUXP = "123456"
# mysql数据库配置信息
DBUSER = 'root'
DBPASSWORD = 'root'
DBHOST = LINUXIP
DBPORT = '3306'
DB = 'weChat'
# mongodb数据库配置信息
MONGOUSER = "root"
MONGOPWD = "123456"
MONGOIP = LINUXIP
MONGOPORT = "27017"
# 上传图片类型配置
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF', 'jpeg'])

# 图片存储服务器(ngix远程部署)
SERVER_IP_NGIX = 'http://' + LINUXIP + ':5002/static/img/'

# 图片存储地址
NGIX_ADDR = "/software/nginx-1.12.0/html/static/img/"
LOCAL_ADDR = os.getcwd() + "/static/img/"  # 临时本地存储地址

# 配置图片存储服务器
SERVER_IP = SERVER_IP_NGIX

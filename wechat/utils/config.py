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
# redis数据库配置信息
REDISIP = LINUXIP
REDISPORT = "6379"
APP_ID = 'wx0f367628fac8067e'
SECRET = 'c3a3d65bc5a7ad0273e3407aa678dfd6'
TOKENSTR = "maluguang" #与微信公众号后台填写保持一致
# 图片存储服务器(ngix远程部署)
SERVER_IP_NGIX = 'http://' + LINUXIP + ':5002/static/img/'
# 配置图片存储服务器
SERVER_IP = SERVER_IP_NGIX
# 域名
ROOTURL = "http://wxxl.frpgz1.idcfengye.com/"

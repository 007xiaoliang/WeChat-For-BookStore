#!/bin/sh
#启动
/usr/local/mongodb/bin/mongod -f /usr/local/mongodb/bin/mongodb.conf
#启动mysql
systemctl start  mysqld.service
#启动nginx
/usr/local/nginx/sbin/nginx -c /usr/local/nginx/conf/nginx.conf
#启动redis
/software/redis-4.0.6/src/redis-server /software/redis-4.0.6/src/redis.conf
# -*- coding: UTF-8 -*-

# 以下数据库配置信息根据实际需要进行设置
# 参数为:1.mysql 2.redis 3.mongodb
SQLNAME = "mongodb"

# 配置mysql信息
MYSQLHOST = "127.0.0.1"
MYSQLPORT = 3306
USERNAME = "root"
PASSWORD = "123456"
DATABASE = "proxy_db"
TABLENAME = "proxy"
CHARSET = "utf8"

# 配置mongodb信息
MONGODBHOST = "127.0.0.1"
MONGODBPORT = 27017
MONGODATABASE = "proxy_db"
MONGOTABLE = "proxy"

# 配置redis信息
REDISHOST = "127.0.0.1"
REDISPORT = 6379
REDISDB = 0
REDISKEY = "proxy"


# 配置url
XICIURL = "https://www.xicidaili.com/nn/{}"  # 西刺代理
KUAIDAILIURL = "https://www.kuaidaili.com/ops/proxylist/{}/"  # 快代理
DAILI66URL = "http://www.66ip.cn/{}.html"  # 代理66
GOUBANJIAURL = "http://www.goubanjia.com/"  # goubanjia主页
WUYOUURL = "http://www.data5u.com/"  # 无忧代理主页



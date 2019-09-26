# -*- coding: UTF-8 -*-
import hashlib

import pymongo
import pymysql
import redis
import six

import settings


class SaveData(object):
    def __init__(self, data_list):
        self.data_list = data_list
        if settings.SQLNAME == "mysql":
            self.conn = pymysql.connect(
                host=settings.MYSQLHOST,
                port=settings.MYSQLPORT,
                user=settings.USERNAME,
                password=settings.PASSWORD,
                database=settings.DATABASE,
                charset=settings.CHARSET
            )
            self.cursor = self.conn.cursor()
        elif settings.SQLNAME == "redis":
            self.redis_client = redis.Redis(
                host=settings.REDISHOST,
                port=settings.REDISPORT,
                db=settings.REDISDB
            )
        elif settings.SQLNAME == "mongodb":
            self.mongodb_client = pymongo.MongoClient(
                host=settings.MONGODBHOST,
                port=settings.MONGODBPORT
            )
            self.collection = self.mongodb_client[settings.MONGODATABASE][settings.MONGOTABLE]
        else:
            raise Exception("没有其他数据库保存类型")

    def _change_column(self, item_dict):
        """
        将字典数据转换成mysql字段
        :param item_dict: {"ip":xxx, "port": xxx, "agent_form":xxx}
        :return: http://+ ip + port
        """
        ip = item_dict["agent_form"].lower() + "://" + item_dict["ip"] + ":" + item_dict["port"]
        # 生成 {"http": "http://xxxx:xxxx"}
        proxy_str = str({item_dict["agent_form"].lower(): ip})
        # 生成主键id，防止重复
        sql_id = self.gen_fp_id(proxy_str)
        return sql_id, proxy_str

    def _save_to_mysql(self, values):
        """
        插入到mysql数据库中
        :param values: 保存到数据库中的值
        :return:
        """
        try:
            sql = "insert into {} (id, ip) value {}".format(settings.TABLENAME, values)
            self.cursor.execute(sql)
            self.conn.commit()
            print(sql, "保存成功")
        except Exception as e:
            self._close_mysql()
            print("mysql插入数据发生异常，关闭mysql连接")

    def _save_to_redis(self, values):
        """
        将数据保存到redis中
        :return:
        """
        try:
            self.redis_client.sadd(settings.REDISKEY, values)
            print(values, ":保存成功")
        except Exception as e:
            print("redis保存数据发生异常")

    def _save_to_mongodb(self, id, values):
        """
        将数据保存到mongodb中
        :param id:
        :param values:
        :return:
        """
        insert_dict = {"_id": id, "proxy": values}
        try:
            self.collection.insert_one(insert_dict)
            print(values, ":保存成功")
        except Exception as e:
            print("mongodb插入的数据已经保存过了")
            pass

    def _close_mysql(self):
        """关闭mysql操作"""
        self.cursor.close()
        self.conn.close()

    def gen_fp_id(self, param):
        '''
        对数据进行sha1处理，生成字段作为id主键
        :param params: 获取相应处理之后的字典数据
        :return: 返回带有id主键的字典数据''
        '''

        fp = hashlib.sha1()
        fp.update(SaveData._to_byte(param))
        id = fp.hexdigest()
        return id

    def _filter(self, select_column):
        '''
        对数据进行查询过滤
        :param table_name: 查询表
        :param select_column: 查询的id字段
        :return: True or False
        '''

        sql = "select id from " + settings.TABLENAME + " where id=%s;"
        params = [select_column]
        self.cursor.execute(sql, params)
        result = self.cursor.fetchone()
        if result is not None:
            print('数据已保存过')
            return False
        return True

    @staticmethod
    def _to_byte(string):
        if six.PY2:  # 当环境是python2
            if isinstance(string, str):
                return string
            else:
                return string.encode("utf-8")  # unicode类型转化为字节类型
        elif six.PY3:  # 当环境是python3
            if isinstance(string, str):
                return string.encode("utf-8")
            else:
                return string

    def _save(self):
        if settings.SQLNAME == "mysql":
            for temp in self.data_list:
                id, ip_str = self._change_column(temp)
                # 对数据进行查询操作是否重复
                if self._filter(id):
                    self._save_to_mysql(str((id, ip_str)))

        elif settings.SQLNAME == "redis":
            for temp in self.data_list:
                id, ip_str = self._change_column(temp)
                self._save_to_redis(ip_str)
        elif settings.SQLNAME == "mongodb":
            for temp in self.data_list:
                id, ip_str = self._change_column(temp)
                self._save_to_mongodb(id, ip_str)
        else:
            raise Exception("无法指定你要保存到哪个数据库")

    def save(self):
        """执行保存操作"""
        self._save()


if __name__ == '__main__':
    pass

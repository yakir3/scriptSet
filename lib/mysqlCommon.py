#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.get_config import get_config
from lib.get_mylogger import mylogger
from models.dnspod_models import *


class Mysql_common(object):

    config_data = get_config('mysql')
    _m_database = config_data['db']
    _m_user = config_data['user']
    _m_passwd = config_data['password']
    _m_ip = config_data['ip']
    _m_port = config_data['port']

    def __init__(self):
        self._engine = create_engine(f"mysql+pymysql://{self._m_user}:{self._m_passwd}@{self._m_ip}:{self._m_port}/{self._m_database}", max_overflow=5)
        self._Session = sessionmaker(bind=self._engine)
        self._session = self._Session()


    def insert(self, table_class, table_data):
        try:
            insertdata = table_class(**table_data)
            self._session.add(insertdata)
            self._session.commit()
            print(f"\033[32m数据入库成功，入库数据{table_data}\033[0m")
        except Exception as e:
            print("\033[31m数据入库失败!!!检查日志：logs/operate.log\033[0m")
            mylogger.error(f"插入数据失败，失败原因：{e.__str__()}")


    def delete(self, table_class, table_data):
        pass


    def update(self):
        pass


    def get(self, table_class, condition=None):
        try:
            result = self._session.query(table_class).all()
            if condition:
                res = result
            else:
                res = result
                return res
        except Exception as e:
            print("\033[31m查询数据失败!!!检查日志：logs/operate.log\033[0m")
            mylogger.error(f"查询数据失败，失败原因：{e.__str__()}")





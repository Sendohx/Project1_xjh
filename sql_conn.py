# -*- coding = utf-8 -*-
# @Time: 2023/11/21 9:50
# @Author: Jiahao Xu
# @File：sql_conn.py
# @Software: PyCharm

import pandas as pd
import pymysql

# 定义数据库连接信息
db_wind = {
            'host': '192.168.7.93',
            'port': 3306,
            'username': 'quantchina',
            'password': 'zMxq7VNYJljTFIQ8',
            'database': 'wind'
            }


# 链接数据库
def connect_mysql(db_info):
    """
        连接到数据库
        :param db_info: 数据库连接信息
        :return: 数据库连接对象
        """
    host = db_info['host']
    port = db_info['port']
    username = db_info['username']
    password = db_info['password']
    database = db_info['database']

    try:
        # 连接到MySQL数据库
        conn = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database
            )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")


def fetch_data(connection, table_name, columns='*', condition_1='1=1', condition_2='1=1'):
    """
    连接 wind 数据库  获取金融数据
    :param connection: 数据库链接
    :param columns: 列名，默认取全部列
    :param table_name:需要获取的表名
    :param condition_1: 动态筛选条件，默认‘1=1’始终为真
    :param condition_2: 动态筛选条件，默认‘1=1’始终为真
    :return: Data: 所需数据的dataframe
    """
    with connection.cursor() as cursor:
        data_sql = ''' 
                           SELECT %s 
                             FROM %s
                            WHERE %s
                              AND %s
                            ''' % (columns, table_name, condition_1, condition_2)

        cursor.execute(data_sql)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        data = pd.DataFrame(list(data), columns=columns)
        if data.empty:
            return data
    return data

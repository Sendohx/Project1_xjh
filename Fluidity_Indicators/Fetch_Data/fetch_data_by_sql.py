# -*- coding = utf-8 -*-
# @Time: 2023/11/24 10:20
# @Author: Jiahao Xu
# @File：main_2.py
# @Software: PyCharm

import pandas as pd

from sql_conn import db_wind, connect_mysql


conn = connect_mysql(db_wind)

with conn.cursor() as cursor:
    data_sql = '''
            SELECT A.*
            FROM ASHAREEODDERIVATIVEINDICATOR A
            WHERE A.TRADE_DT > '20190501' AND A.S_INFO_WINDCODE IN (
                SELECT B.S_CON_WINDCODE
                FROM AINDEXMEMBERS B
                WHERE B.S_INFO_WINDCODE = '000985.CSI'
                    AND (
                        (B.S_CON_INDATE <= A.TRADE_DT AND B.S_CON_OUTDATE > A.TRADE_DT)
                    OR (B.S_CON_INDATE <= A.TRADE_DT AND B.S_CON_OUTDATE IS NULL)
                    )
                )
            '''
    cursor.execute(data_sql)
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    data = pd.DataFrame(list(data), columns=columns)

# 指定保存的文件路径
Directory_path = '/Fluidity_Indicators/Data'

# 指定csv文件名
csv = f'csi_share_eod_deriv.csv'

# 将DataFrame保存为CSV格式文件
data.to_csv(Directory_path+csv, index=False)

print('CSV文件保存成功:', Directory_path)

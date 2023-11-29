# -*- coding = utf-8 -*-
# @Time: 2023/11/23 9:50
# @Author: Jiahao Xu
# @File：fetch_data_by_py.py
# @Software: PyCharm

from sql_conn import db_wind, connect_mysql, fetch_data


table_name_1 = 'AINDEXEODPRICES'
columns_1 = 'S_INFO_WINDCODE, TRADE_DT, S_DQ_PCTCHANGE, S_DQ_VOLUME'
condition_1_1 = "S_INFO_WINDCODE = '000985.CSI'"
condition_2_1 = "TRADE_DT >= '20180501'"

table_name_2 = 'ASHAREEODDERIVATIVEINDICATOR'  # A股日衍生行情
columns_2 = 'S_INFO_WINDCODE, TRADE_DT, FLOAT_A_SHR_TODAY'
condition_1_2 = "TRADE_DT >= '20180501'"

table_name_3 = 'AINDEXMEMBERS'  # A股指数成分股
condition_1_3 = "S_INFO_WINDCODE = '000985.CSI'"
condition_2_3 = "TRADE_DT >= '20180501'"

# 获取所需数据dataframe
conn = connect_mysql(db_wind)
csi_eod_price = fetch_data(conn, table_name_1, columns_1, condition_1_1)
a_eod_drv = fetch_data(conn, table_name_2, columns_2)
csi_mem = fetch_data(conn, table_name_3)


# 指定保存的文件路径
Directory_path = '/Data/'

# 指定csv文件名
csv_1 = f'csi_eod_price.csv'
csv_2 = f'a_eod_drv.csv'
csv_3 = f'csi_mem.csv'

# 将DataFrame保存为CSV格式文件
csi_eod_price.sort_values('TRADE_DT').to_csv(Directory_path+csv_1, index=False)
a_eod_drv.to_csv(Directory_path+csv_2, index=False)
csi_mem.to_csv(Directory_path+csv_3, index=False)

print('CSV文件保存成功:', Directory_path)

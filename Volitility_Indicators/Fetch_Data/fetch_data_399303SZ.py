# -*- coding = utf-8 -*-
# @Time: 2023/11/23 12:45
# @Author: Jiahao Xu
# @File：fetch_data_399303SZ.py
# @Software: PyCharm

import pandas as pd

from sql_conn import db_wind, connect_mysql, fetch_data


def fetch_data_399303():
    conn = connect_mysql(db_wind)

    # 中证全指成分股日行情
    with conn.cursor() as cursor:
        data_sql = '''
                SELECT A.S_INFO_WINDCODE, A.TRADE_DT, A.S_DQ_ADJPRECLOSE, A.S_DQ_ADJOPEN, 
                A.S_DQ_ADJHIGH, A.S_DQ_ADJLOW, A.S_DQ_ADJCLOSE
                FROM ASHAREEODPRICES A
                WHERE A.TRADE_DT > '20191001' AND A.S_INFO_WINDCODE IN (
                    SELECT B.S_CON_WINDCODE
                    FROM AINDEXMEMBERS B
                    WHERE B.S_INFO_WINDCODE = '399303.SZ'
                        AND (
                            (B.S_CON_INDATE <= A.TRADE_DT AND B.S_CON_OUTDATE > A.TRADE_DT)
                        OR (B.S_CON_INDATE <= A.TRADE_DT AND B.S_CON_OUTDATE IS NULL)
                        )
                    )
                '''
        cursor.execute(data_sql)
        price_data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        price_data = pd.DataFrame(list(price_data), columns=columns)
        price_data = price_data.rename(
            columns={'S_INFO_WINDCODE': 'symbol', 'TRADE_DT': 'Date', 'S_DQ_ADJPRECLOSE': 'pre_close',
                     'S_DQ_ADJOPEN': 'open', 'S_DQ_ADJHIGH': 'high', 'S_DQ_ADJLOW': 'low', 'S_DQ_ADJCLOSE': 'close'})
        price_data[price_data.columns[2:]] = price_data[price_data.columns[2:]].apply(pd.to_numeric, errors='coerce')
        price_data = price_data.sort_values(['symbol', 'Date'])

    # 中证全指日行情
    table_name_1 = 'AINDEXEODPRICES'
    columns_1 = 'S_INFO_WINDCODE, TRADE_DT, S_DQ_PRECLOSE, S_DQ_OPEN, S_DQ_HIGH, S_DQ_LOW, S_DQ_CLOSE'
    condition_1 = "S_INFO_WINDCODE = '399303.SZ'"
    condition_2 = "TRADE_DT >= '20191001'"

    index_price_data = fetch_data(conn, table_name_1, columns_1, condition_1, condition_2)
    index_price_data = index_price_data.rename(
        columns={'S_INFO_WINDCODE': 'symbol', 'TRADE_DT': 'Date', 'S_DQ_PRECLOSE': 'pre_close', 'S_DQ_OPEN': 'open',
                 'S_DQ_HIGH': 'high', 'S_DQ_LOW': 'low', 'S_DQ_CLOSE': 'close'})
    index_price_data[index_price_data.columns[2:]] = (index_price_data[index_price_data.columns[2:]]
                                                      .apply(pd.to_numeric, errors='coerce'))
    index_price_data = index_price_data.sort_values(['symbol', 'Date'])

    # 指数日内收益和当日收益
    index_price_data['inday_pct'] = index_price_data['close'] / index_price_data['open'] - 1
    index_price_data['day_pct'] = index_price_data['close'] / index_price_data['pre_close'] - 1

    return price_data, index_price_data

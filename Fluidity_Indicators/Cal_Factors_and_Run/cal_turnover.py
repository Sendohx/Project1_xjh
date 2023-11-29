# -*- coding = utf-8 -*-
# @Time: 2023/11/23 16:11
# @Author: Jiahao Xu
# @File：cal_turnover.py
# @Software: PyCharm

import pandas as pd


def cal_day_float(a_eod_drv, csi_mem):
    """
    筛选中证全指成分股，计算指数日自由流通股
    :param a_eod_drv:A股日估值行情
    :param csi_mem:中证全指成分股信息
    :return: 中证全指各交易日自由流通股
    """
    fliter_data = []
    for index, row in csi_mem.iterrows():
        stock_code = row['S_CON_WINDCODE']
        stock_indate = row['S_CON_INDATE']
        stock_outdate = row['S_CON_OUTDATE']
        stock_cur_sign = row['CUR_SIGN']
        if stock_cur_sign == 0:
            temp_data = a_eod_drv.loc[(a_eod_drv.S_INFO_WINDCODE == stock_code)
                                      & (a_eod_drv.TRADE_DT >= stock_indate)
                                      & (a_eod_drv.TRADE_DT <= stock_outdate)]
        else:
            temp_data = a_eod_drv.loc[(a_eod_drv.S_INFO_WINDCODE == stock_code)
                                      & (a_eod_drv.TRADE_DT >= stock_indate)]
        fliter_data.append(temp_data)

    csi_share_eod_drv = pd.concat(fliter_data)

    return csi_share_eod_drv


def cal_turnover(csi_eod_price, csi_share_eod_drv):
    """
   筛选中证全指成分股，计算指数日自由流通股
   :param csi_eod_price: 中证全指日行情数据
   :param csi_share_eod_drv: 中证全指成分股日流通股数据
   :return: 中证全指各交易日自由流通股
   """
    csi_eod_float = (csi_share_eod_drv[['TRADE_DT', 'FLOAT_A_SHR_TODAY']].groupby('TRADE_DT').sum().reset_index().
                     rename(columns={'FLOAT_A_SHR_TODAY': 'FLOAT_SUM_TODAY'}))

    csi_eod_price = csi_eod_price.merge(csi_eod_float, on='TRADE_DT', how='left')
    csi_eod_price['S_DQ_TURNOVER'] = csi_eod_price.S_DQ_VOLUME / csi_eod_price.FLOAT_SUM_TODAY

    return csi_eod_price

# -*- coding = utf-8 -*-
# @Time: 2023/11/28 13:11
# @Author: Jiahao Xu
# @File：yang_zhang_sigma.py
# @Software: PyCharm

import numpy as np


def yang_zhang_sigma(data, window, alpha):
    """
    计算yang_zhang_sigma
    :param data: 成分股日价格数据
    :param window: 窗口值
    :param alpha:
    :return: 成分股日sigma数据
    """
    data = data.copy()

    data['c2c'] = data.groupby('symbol')['close'].apply(lambda x: x.pct_change()).values + 1
    data['ln_c2c'] = np.log(data['c2c'])
    data['c2c_sigma'] = data.groupby('symbol')['ln_c2c'].rolling(window).std(ddof=1).values

    # open to open volatility
    data['o2o'] = data.groupby('symbol')['open'].apply(lambda x: x.pct_change()).values + 1
    data['ln_o2o'] = np.log(data['o2o'])
    data['o2o_sigma'] = data.groupby('symbol')['ln_o2o'].rolling(window).std(ddof=1).values

    data['h_c'] = np.log(data['high'] / data['close'])
    data['h_o'] = np.log(data['high'] / data['open'])
    data['l_c'] = np.log(data['low'] / data['close'])
    data['l_o'] = np.log(data['low'] / data['open'])

    data['rsy'] = data['h_c'] * data['h_o'] + data['l_c'] * data['l_o']
    data['rsy_sigma'] = data.groupby('symbol')['rsy'].rolling(window).mean().values
    data['rsy_sigma'] = np.sqrt(data['rsy_sigma'])

    # weighted average
    k = alpha / ((1 + alpha) + (window + 1) / (window - 1))
    data['yang_zhang_sigma'] = np.sqrt(
        pow(data['o2o_sigma'], 2) + k * pow(data['c2c_sigma'], 2) + (1 - k) * pow(data['rsy_sigma'], 2))

    return data[['symbol', 'Date', 'yang_zhang_sigma']]

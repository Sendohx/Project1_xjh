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

    data['o'] = data['open']/data['pre_close']
    data['ln_o'] = np.log(data['o'])
    data['o_sigma'] = data.groupby('symbol')['ln_o'].rolling(window).std(ddof=1).values

    data['c'] = data['close']/data['open']
    data['ln_c'] = np.log(data['c'])
    data['c_sigma'] = data.groupby('symbol')['ln_c'].rolling(window).std(ddof=1).values

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

    return data[['symbol', 'date', 'yang_zhang_sigma']]

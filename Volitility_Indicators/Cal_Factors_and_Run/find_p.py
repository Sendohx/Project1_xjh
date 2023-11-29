# -*- coding = utf-8 -*-
# @Time: 2023/11/28 12:52
# @Author: Jiahao Xu
# @File：find_p.py
# @Software: PyCharm

import pandas as pd


def find_p(numbers):
    """
    计算indicators的p分位值（0，20，40，60，80）
    :param numbers: indicators序列
    :return: p分位值序列
    """
    if pd.isna(numbers):
        return None
    values = [0, 20, 40, 60, 80]
    p_value = max(val for val in values if val < numbers)

    return p_value

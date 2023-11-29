# -*- coding = utf-8 -*-
# @Time: 2023/11/28 13:08
# @Author: Jiahao Xu
# @File：rolling_cov_mean.py
# @Software: PyCharm

import pandas as pd
import numpy as np
from tqdm import tqdm


def rolling_cov_mean(data, window_size):
    """
    计算成分股滚动协方差均值
    :param data: 成分股价格日数据
    :param window_size: 窗口值
    :return:
    """
    data['return'] = data['close']/data['pre_close'] - 1
    data = data[['symbol', 'Date', 'return']]
    p_data = data.pivot(index='Date', columns='symbol', values='return')
    num_windows = len(p_data) - window_size + 1

    rolling_results = []
    for i in tqdm(range(num_windows)):
        window_data = p_data.iloc[i:i + window_size, :]
        rolling_cov = window_data.cov()  # 设置min_periods参数或许可以提高准确率
        upper_triangle_mean = np.nanmean(np.triu(rolling_cov, k=1))
        rolling_results.append(upper_triangle_mean)

    # Create a DataFrame with results
    result_df = pd.DataFrame({'date': p_data.index[window_size - 1:], 'rolling_cov_mean': rolling_results})

    print(result_df)

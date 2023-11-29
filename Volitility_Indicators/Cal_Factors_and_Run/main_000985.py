# -*- coding = utf-8 -*-
# @Time: 2023/11/28 13:01
# @Author: Jiahao Xu
# @File：main_000985.py
# @Software: PyCharm

import pandas as pd

from Volitility_Indicators.Fetch_Data import fetch_data_000985CSI
from find_p import find_p
from yang_zhang_sigma import yang_zhang_sigma
from rolling_cov_mean import rolling_cov_mean


if __name__ == '__main__':
    window = 20
    alpha: float = 0.34

    price_data, index_price_data = fetch_data_000985CSI.fetch_data_000985()
    share_sigma_data = yang_zhang_sigma(price_data, window, alpha)
    index_sigma_data = yang_zhang_sigma(index_price_data, window, alpha)

    index_price_data = pd.merge(index_price_data, index_sigma_data, on=['Date', 'symbol'], how='left')
    index_price_data = index_price_data.rename(columns={'yang_zhang_sigma': 'index_sigma'})

    share_sigma_mean_data = (share_sigma_data[['Date', 'yang_zhang_sigma']].groupby('Date').mean().reset_index()
                             .rename(columns={'yang_zhang_sigma': 'share_sigma_mean'}))  # 成分股波动率平均值
    index_price_data = index_price_data.merge(share_sigma_mean_data, on='Date', how='left')

    rolling_cov_mean_data = rolling_cov_mean(price_data)
    index_price_data = index_price_data.merge(rolling_cov_mean_data, on='Date', how='left')

    index_price_data['index_sigma_rank'] = index_price_data['index_sigma'].rolling(242).apply(
        lambda x: pd.Series(x).rank(pct=True).iloc[-1] * 100)
    index_price_data['share_sigma_mean_rank'] = index_price_data['share_sigma_mean'].rolling(242).apply(
        lambda x: pd.Series(x).rank(pct=True).iloc[-1] * 100)
    index_price_data['rolling_cov_mean_rank'] = index_price_data['rolling_cov_mean'].rolling(242).apply(
        lambda x: pd.Series(x).rank(pct=True).iloc[-1] * 100)

    index_price_data['index_sigma_p'] = index_price_data['index_sigma_rank'].apply(
        lambda x: find_p(x) if not pd.isna(x) else None)
    index_price_data['share_sigma_mean_p'] = index_price_data['share_sigma_mean_rank'].apply(
        lambda x: find_p(x) if not pd.isna(x) else None)
    index_price_data['rolling_cov_mean_p'] = index_price_data['rolling_cov_mean_rank'].apply(
        lambda x: find_p(x) if not pd.isna(x) else None)

    print(index_price_data[index_price_data['date'] >= '20210101'])

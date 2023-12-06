# -*- coding = utf-8 -*-
# @Time: 2023/12/6 8:52
# @Author: Jiahao Xu
# @File：cal_factor.py
# @Software: PyCharm

import pandas as pd


   def flu_factors(df, deriv):
    """
    计算非流动性指标
    :param df:指数信息dataframe
    :param deriv:成分股日衍生dataframe
    :return: 返回添加因子列后的dataframe
    """
    df = df.sort_values('date')
    
    index_deriv = deriv.groupby('date')['market_value'].sum().reset_index(level=0)
    df = df.merge(index_deriv, on='date', how='left')
    df['turnover'] = df['amount'] / df['market_value'] * 100
    
    df.loc[:, 'stdvol'] = df['amount'].rolling(20).std()
    # 指数日行情表中无换手率数据，需自行构建
    df.loc[:, 'abturnover'] = (df['turnover'].rolling(20).mean())/(df['turnover'].rolling(120).mean())
    df.loc[:, 'stdturnover'] = df['turnover'].rolling(20).std()
    df.loc[:, 'ILLIQ'] = (df['day_pct'].abs()/df['amount']*100*1000000*10000).rolling(20).mean()
    df.loc[:, 'ABILLIQ'] = df['ILLIQ'] - (df['ILLIQ'].rolling(120).mean())

    df1 = df.loc[df['day_pct'] < 0].copy()
    df1.loc[:, 'NEILLIQ'] = (df1['day_pct'].abs()/df1['amount']*100*1000000*10000).rolling(20).mean()
    df2 = pd.merge(df, df1, on=list(df.columns), how='left')

    return df2


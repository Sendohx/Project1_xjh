# -*- coding = utf-8 -*-
# @Time: 2023/11/27 8:52
# @Author: Jiahao Xu
# @File：cal_factor.py
# @Software: PyCharm

import pandas as pd


def cal_factors(df):
    """
    计算非流动性指标
    :param df:指数信息dataframe
    :return: 返回添加因子列后的dataframe
    """
    df = df.sort_values('TRADE_DT')
    df.loc[:, 'ILLIQ'] = (df['S_DQ_PCTCHANGE'].abs()/df['S_DQ_VOLUME']).rolling(20).mean()
    df.loc[:, 'ABILLIQ'] = df['ILLIQ'] - df['ILLIQ'].rolling(120).mean()

    df1 = df.loc[df['S_DQ_PCTCHANGE'] < 0].copy()
    df1.reset_index(drop=True, inplace=True)
    df1.loc[:, 'NEILLIQ'] = (df1['S_DQ_PCTCHANGE'].abs() / df1['S_DQ_VOLUME']).rolling(20).mean()
    df2 = pd.merge(df, df1, on=list(df.columns), how='left')

    df.loc[:, 'stdvol'] = df['S_DQ_VOLUME'].rolling(20).std()
    # 指数日行情表中无换手率数据，需自行构建
    df.loc[:, 'abturnover'] = df['S_DQ_TURNOVER'].rolling(20).mean()/df['S_DQ_TURNOVER'].rolling(120).mean()
    df.loc[:, 'stdturnover'] = df['S_DQ_TURNOVER'].rolling(20).std()

    df2 = df2[df2['TRADE_DT'] >= 20191201]

    return df2


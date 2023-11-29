# -*- coding = utf-8 -*-
# @Time: 2023/11/27 10:11
# @Author: Jiahao Xu
# @File：main_000985.py
# @Software: PyCharm

import pandas as pd
import glob

from cal_factor import cal_factors
from cal_turnover import cal_turnover


# 获取文件夹下所有的 CSV 文件路径
folder_path = '/Fluidity_Indicators/Data/csi_share_eod_deriv'
csv_files = glob.glob(folder_path + '/*.csv')

csi_share_eod_deriv_20_to_23 = pd.DataFrame()

for file in csv_files:
    df = pd.read_csv(file)
    csi_share_eod_deriv_20_to_23 = csi_share_eod_deriv_20_to_23._append(df, ignore_index=True)

csi_eod_price = pd.read_csv('/Fluidity_Indicators/Data/csi_eod_price.csv')


if __name__ == '__main__':

    csi_eod_price_new = cal_turnover(csi_eod_price, csi_share_eod_deriv_20_to_23)

    csi_eod_price_new = cal_factors(csi_eod_price_new)

    results_path = '/Fluidity_Indicators/Results'
    result_4years = f'project1_results_4years_JiahaoXu.xlsx'
    result_2023_11 = f'project1_2023.11_JiahaoXu.xlsx'

    csi_eod_price_new.to_excel(results_path + result_4years, index=False)

    csi_eod_price_new[csi_eod_price_new['TRADE_DT'] >= 20231101].to_excel(results_path + result_2023_11, index=False)

# -*- coding: utf-8 -*-

import numpy as np
import pdb
import os
import pandas as pd

from atrader import *
from utils import load_data, get_codes_list

# set global params
top_cor_path = "top_corr"
begin_date = "2018-01-01"
end_date = "2018-03-01"

def find_n_top_corr(code,code_list,top_n=3):
    """Given target code and candidate code list,
    find the top n pairs based on Spearsman Rank Correlation
    """
    error_tag = False
    df_pair = None

    for i,c_code in enumerate(code_list):
        if c_code == code:
            continue
        try:    
            df_1 = load_data(code,begin_date,end_date)
            df_2 = load_data(c_code,begin_date,end_date)

            ts_1 = df_1["close"].diff(1).dropna()
            ts_2 = df_2["close"].diff(1).dropna()

            rank_1 = np.argsort(ts_1)
            rank_2 = np.argsort(ts_2)

            rank_corr = np.corrcoef(rank_1,rank_2)[0,1]

        except:
            print("[Warning] Something went wrong, skip this pair {} and {}".format(c_code,code))
            rank_corr = - 9999.0

        if df_pair is None:
            df_pair = pd.DataFrame({"s1":[code],"s2":[c_code],"corr":[rank_corr]})
        
        else:
            df_pair = df_pair.append({"s1":code,"s2":c_code,"corr":rank_corr},ignore_index=True)
        
        print("Pair {}, {}::{} Rank Corr {}".format(i,code,c_code,rank_corr))

    df_pair = df_pair.sort_values(by="corr",ascending=False).reset_index(drop=True)
    df_top_n = df_pair[:top_n]
    print(df_top_n)
    df_pair.to_csv("{}/{}_corr_result.csv".format(top_cor_path,code),index=False,encoding="utf-8")
    return df_top_n

if __name__ == '__main__':
    # get target codes list
    targets = get_codes_list()
    codes_dict = dict().fromkeys(targets,False)
    for r in os.listdir(top_cor_path):
        e_code = r.split("_")[0]
        codes_dict[e_code] = True

    for code in targets:
        print("Now {}".format(code))
        if codes_dict[code]:
            print("{} has already been calculated !".format(code))
            continue
        else:
            find_n_top_corr(code,targets,3)

    


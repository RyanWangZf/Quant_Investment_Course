# -*- coding: utf-8 -*-
import numpy as np
import pdb
import os
import pandas as pd

from atrader import *
from utils import load_data, get_codes_list

import matplotlib.pyplot as plt
import seaborn as sns

import statsmodels.api as sm

top_cor_path = "top_corr"
rule_path = "rule"
begin_date = "2018-01-01"
end_date = "2018-03-01"

def align_series(ts_1,ts_2):
    ts_2 = ts_2.loc[ts_1.index]
    ts_2 = ts_2.loc[ts_2.notnull()]
    ts_1 = ts_1.loc[ts_2.index]
    return ts_1,ts_2

def find_n_top_pvalue(code,n=3):
    """Mining cointegrated pairs from top-n correlated pairs.c
    """
    df = pd.read_csv("{}/{}_corr_result.csv".format(top_cor_path,code))
    df = df[:n]

    codes_list = [str(s) for s in df.s2.values.tolist()]
    codes_list.append(code)
    n = len(codes_list)

    pairs = []
    pvalue_matrix = np.ones((n,n))
    for i in range(n):
        for j in range(i+1,n):
            try:
                s1 = load_data(codes_list[i],begin_date,end_date)
                s2 = load_data(codes_list[j],begin_date,end_date)
                ts_1 = s1["close"]
                ts_2 = s2["close"]
                ts_1,ts_2 = align_series(ts_1,ts_2)
                res = sm.tsa.stattools.coint(ts_1,ts_2)
                pvalue = res[1]
                pvalue_matrix[i,j] = pvalue
            except:
                print("[Warning] Something went wrong.")
                pvalue = 1
                pvalue_matrix[i,j] = pvalue

            print("{} :: {}, pvalue {}".format(codes_list[i],codes_list[j],pvalue))
            if pvalue < 0.05:
                pairs.append((codes_list[i],codes_list[j],pvalue))

        # sns.heatmap(1-pvalue_matrix,xticklabels=codes_list,
        #     cmap="RdYlGn_r",yticklabels=codes_list,mask=(pvalue_matrix==1))
        # plt.savefig("image/{}_pvalue_mat.png".format(codes_list[i]))
    # plt.show()
    print(pairs)
    return pvalue_matrix, pairs

def mine_pairs(codes_list,n=3):
    """Mining pairs for stats arbitrage
    """
    pairs = []

    top_corr_list = os.listdir(top_cor_path)
    existed_codes = [r.split("_")[0] for r in top_corr_list]
    existed_code_dict = dict().fromkeys(existed_codes,False)
    for code in codes_list:
        existed_code_dict[code] = True

    for code in codes_list:
        if existed_code_dict[code]:
            # find precomputed correlation results
            _, this_pairs = find_n_top_pvalue(code,n=3)
            pairs.extend(this_pairs)
        else:
            print("[Warning] Cannot find {}'s correlation file".format(code))
            continue


    # post processing pairs
    s1_list,s2_list,p_list = [],[],[]
    for s1,s2,pv in pairs:
        s1_list.append(s1)
        s2_list.append(s2)
        p_list.append(pv)

    df_p = pd.DataFrame({"s1":s1_list,"s2":s2_list,"pvalue":p_list})
    df_p.to_csv("{}/pairs.csv".format(rule_path),encoding="utf-8",index=False)
    print("Pairs saved in",rule_path)
    return

def build_rule(pair_path):
    # "build trading rules with p-value"
    df_pair = pd.read_csv(pair_path) # cols=[S1,S2,pvalue]
    up_list,down_list,w_list,s1_s2 = [],[],[],[]
    mean_list, std_list = [], []
    for idx in df_pair.index:
        code1,code2 = str(df_pair.loc[idx].s1),str(df_pair.loc[idx].s2)
        s1_s2.append(str(set([code1,code2])))
        print("{}/{} {}/{}".format(idx+1,df_pair.shape[0],code1,code2))
        try:
            s1 = load_data(code1,begin_date,end_date)["close"]
            s2 = load_data(code2,begin_date,end_date)["close"]
        except:
            print("[Warning] Something went wrong.")
            continue

        ts1,ts2 = align_series(s1,s2)
        x = ts1.values
        Y = ts2.values
        X = sm.add_constant(x)
        res = sm.OLS(Y,X).fit()
        w1 = res.params[1]
        diff = ts2 - w1 * ts1
        diff_mean = diff.mean()
        diff_std  = diff.std()
        up_line = diff_mean + 0.7 * diff_std
        down_line = diff_mean - 0.7 * diff_std
        up_list.append(up_line)
        down_list.append(down_line)
        w_list.append(w1)
        std_list.append(diff_std)
        mean_list.append(diff_mean)
    

    df_rule = pd.DataFrame({"up":up_list,"down":down_list,"w":w_list,"mean":mean_list,"std":std_list,"name":s1_s2,},index=df_pair.index)
    df_rule = pd.concat([df_pair,df_rule],axis=1).reset_index(drop=True)
    df_rule.drop_duplicates(subset="name",inplace=True)
    df_rule = df_rule.sort_values(by="pvalue").reset_index(drop=True)
    df_rule.to_csv("./{}/trade_rule.csv".format(rule_path),index=False,encoding="utf-8")

if __name__ == '__main__':
    
    targets = get_codes_list()
    # mine_pairs(targets,n=3)
    build_rule("rule/pairs.csv")


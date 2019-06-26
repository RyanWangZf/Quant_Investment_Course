# -*- coding: utf-8 -*-
from atrader import *

import numpy as np
import pandas as pd
import pdb
from utils import read_rule

def init(context: 'ContextBackReal'):
    """用户初始化函数"""
    set_backtest(initial_cash=10000000.0)
    reg_kdata("day",1)
    context.pair_df = read_rule()
    context.join_scale = 0.7
    context.stop_scale = 3.0
    context.order_value = 2000000

    # build target dict
    map_dict = {}
    for i,target in enumerate(context.target_list):
        map_dict[target.lower()] = i
    context.map_dict = map_dict


def on_data(context: 'ContextBackReal'):
    """刷新bar函数"""
    data = get_reg_kdata(reg_idx=context.reg_kdata[0],length=20,fill_up=True,df=True,)
    if data["close"].isna().any():
        return

    long_positions = context.account().positions['volume_long']
    short_positions = context.account().positions['volume_short']
    datalist = [data[data['target_idx'] == x] for x in pd.unique(data.target_idx)]

    for idx in context.pair_df.index:
        # check every pair
        pair = context.pair_df.iloc[idx]

        # s2 - w * s1 ~ N(u,v)
        pair_w = pair["w"]

        # compute five bounds
        join_up_bound = pair["mean"] + context.join_scale * pair["std"]
        join_low_bound = pair["mean"] - context.join_scale * pair["std"]
        stop_up_bound = pair["mean"] + context.stop_scale * pair["std"]
        stop_low_bound = pair["mean"] - context.stop_scale * pair["std"]
        median_bound = pair["mean"]

        # get pair diff price
        s1_idx = context.map_dict[pair["s1"].lower()]
        s2_idx = context.map_dict[pair["s2"].lower()]
        s1_close = datalist[s1_idx].close.values
        s2_close = datalist[s2_idx].close.values
        s2_diff_s1 = s2_close - pair_w * s1_close

        # open condition
        open_long_s1_short_s2 = False
        open_long_s2_short_s1 = False
        if long_positions[s1_idx] == 0 and long_positions[s1_idx] == 0 and short_positions[s1_idx] == 0 and short_positions[s2_idx] == 0:
            if s2_diff_s1[-1] >= join_up_bound:
                # open long s1, short s2
                open_long_s1_short_s2 = True
            elif s2_diff_s1[-1] <= join_low_bound:
                # open long s2, short s1
                open_long_s2_short_s1 = True

        # stop profit
        stop_long_s1_short_s2 = False
        stop_long_s2_short_s1 = False
        if long_positions[s1_idx] > 0 or short_positions[s2_idx] > 0:
            if s2_diff_s1[-1] <= median_bound:
                # clean s1 long and s2 short positions
                stop_long_s1_short_s2 = True

        elif long_positions[s2_idx] > 0 or short_positions[s1_idx] > 0:
            if s2_diff_s1[-1] >= median_bound:
                # clean s2 long and s1 short positions
                stop_long_s2_short_s1 = True

        # stop loss condition
        if long_positions[s1_idx] > 0 or short_positions[s2_idx] > 0:
            if s2_diff_s1[-1] >= stop_up_bound:
                # clean s1 long and s2 short positions
                stop_long_s1_short_s2 = True

        elif long_positions[s2_idx] > 0 or short_positions[s1_idx] > 0:
            if s2_diff_s1[-1] <= stop_low_bound:
                # clean s2 long and s1 short positions
                stop_long_s2_short_s1 = True


        # transactions
        if open_long_s1_short_s2:
            # long s1
            order_target_value(account_idx=0, target_idx=s1_idx, 
                target_value=context.order_value,
                side=1,order_type=2)
            # short s2
            order_target_value(account_idx=0, target_idx=s2_idx, 
                target_value=context.order_value,
                side=2,order_type=2)
            print("开仓, long {}, short {}".format(pair["s1"], pair["s2"]))

        if open_long_s2_short_s1:
            # long s2
            order_target_value(account_idx=0, target_idx=s2_idx, 
                target_value=context.order_value,
                side=1,order_type=2)
            # short s1
            order_target_value(account_idx=0, target_idx=s1_idx, 
                target_value=context.order_value,
                side=2,order_type=2)
            print("开仓, long {}, short {}".format(pair["s2"], pair["s1"]))

        if stop_long_s1_short_s2:
            # clean s1 long positions
            order_target_volume(account_idx=0, target_idx=s1_idx, target_volume=0, side=1, order_type=2)
            # clean s2 short positions
            order_target_volume(account_idx=0, target_idx=s2_idx, target_volume=0, side=1, order_type=2)
            print("平仓, {} and {}".format(pair["s1"],pair["s2"]))


        if stop_long_s2_short_s1:
            # clean s1 long positions
            order_target_volume(account_idx=0, target_idx=s1_idx, target_volume=0, side=1, order_type=2)
            # clean s2 short positions
            order_target_volume(account_idx=0, target_idx=s2_idx, target_volume=0, side=1, order_type=2)
            print("平仓, {} and {}".format(pair["s1"],pair["s2"]))


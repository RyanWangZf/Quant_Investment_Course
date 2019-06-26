# -*- coding: utf-8 -*-
# 创建时间:2019/06/26 19:22:58
from atrader import *

if __name__ == '__main__':
	begin_date = '2018-06-01'
	end_date = '2018-12-31'
	target_list = []
	target_list.extend(['shfe.ag0000'])
	target_list.extend(['shfe.al0000'])
	target_list.extend(['shfe.au0000'])
	target_list.extend(['shfe.bu0000'])
	target_list.extend(['shfe.cu0000'])
	target_list.extend(['shfe.fu0000'])
	target_list.extend(['shfe.hc0000'])
	target_list.extend(['shfe.ni0000'])
	target_list.extend(['shfe.pb0000'])
	target_list.extend(['shfe.rb0000'])
	target_list.extend(['shfe.ru0000'])
	target_list.extend(['shfe.sn0000'])
	target_list.extend(['shfe.sp0000'])
	target_list.extend(['shfe.wr0000'])
	target_list.extend(['shfe.zn0000'])
	target_list.extend(['dce.a0000'])
	target_list.extend(['dce.b0000'])
	target_list.extend(['dce.bb0000'])
	target_list.extend(['dce.c0000'])
	target_list.extend(['dce.cs0000'])
	target_list.extend(['dce.eg0000'])
	target_list.extend(['dce.fb0000'])
	target_list.extend(['dce.i0000'])
	target_list.extend(['dce.j0000'])
	target_list.extend(['dce.jd0000'])
	target_list.extend(['dce.jm0000'])
	target_list.extend(['dce.l0000'])
	target_list.extend(['dce.m0000'])
	target_list.extend(['dce.p0000'])
	target_list.extend(['dce.pp0000'])
	target_list.extend(['dce.v0000'])
	target_list.extend(['dce.y0000'])
	target_list.extend(['czce.AP000'])
	target_list.extend(['czce.CF000'])
	target_list.extend(['czce.CJ000'])
	target_list.extend(['czce.CY000'])
	target_list.extend(['czce.FG000'])
	target_list.extend(['czce.JR000'])
	target_list.extend(['czce.LR000'])
	target_list.extend(['czce.MA000'])
	target_list.extend(['czce.OI000'])
	target_list.extend(['czce.PM000'])
	target_list.extend(['czce.RI000'])
	target_list.extend(['czce.RM000'])
	target_list.extend(['czce.RS000'])
	target_list.extend(['czce.SF000'])
	target_list.extend(['czce.SM000'])
	target_list.extend(['czce.SR000'])
	target_list.extend(['czce.TA000'])
	target_list.extend(['czce.WH000'])
	target_list.extend(['czce.ZC000'])
	target_list.extend(['cffex.IC0000'])
	target_list.extend(['cffex.IF0000'])
	target_list.extend(['cffex.IH0000'])
	target_list.extend(['cffex.T0000'])
	target_list.extend(['cffex.TF0000'])
	target_list.extend(['cffex.TS0000'])
	target_list.extend(['ine.sc0000'])

	run_backtest(strategy_name='Future_Arbitrage',
				file_path='Future_Arbitrage_Stratey.py',
				target_list=target_list,
				frequency='day',
				fre_num=1,
				begin_date=begin_date,
				end_date=end_date,
				fq=enums.FQ_NA)


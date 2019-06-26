# Introduction to Quant Investment

The project code for the course *Introduction to Quant Investment* by Professor Jianwu Lin in Tsinghua Berkeley Shenzhen Institute.



# How to demo

```shell
# Find the top correlated futures
python run_top_corr.py
# Find the cointegration between the futures
python run_cointeg.py
# Run backtest, need Autotrder
python Future_Arbitrage_Runbacktest.py
```



## The Cointegrated Pairs

| s1           | s2           | pvalue   | mean     | std      | name                           |
| ------------ | ------------ | -------- | -------- | -------- | ------------------------------ |
| dce.l0000    | shfe.ag0000  | 0.000658 | 163.7115 | 35.03875 | {'shfe.ag0000', 'dce.l0000'}   |
| dce.a0000    | dce.i0000    | 0.001603 | -69.2647 | 7.716843 | {'dce.i0000', 'dce.a0000'}     |
| cffex.IC0000 | dce.b0000    | 0.00857  | 4667.7   | 66.45967 | {'cffex.IC0000', 'dce.b0000'}  |
| shfe.ag0000  | dce.pp0000   | 0.01245  | 3968.687 | 75.56486 | {'dce.pp0000', 'shfe.ag0000'}  |
| shfe.al0000  | shfe.cu0000  | 0.013388 | 15462.4  | 495.4003 | {'shfe.al0000', 'shfe.cu0000'} |
| czce.RM000   | shfe.ag0000  | 0.014852 | 6094.289 | 52.97036 | {'czce.RM000', 'shfe.ag0000'}  |
| czce.FG000   | czce.MA000   | 0.020226 | 753.3168 | 87.89455 | {'czce.FG000', 'czce.MA000'}   |
| shfe.bu0000  | dce.a0000    | 0.031783 | 5172.432 | 53.89991 | {'shfe.bu0000', 'dce.a0000'}   |
| czce.SR000   | shfe.rb0000  | 0.032455 | 9328.147 | 56.20987 | {'czce.SR000', 'shfe.rb0000'}  |
| shfe.al0000  | czce.OI000   | 0.033396 | 2428.19  | 45.25371 | {'czce.OI000', 'shfe.al0000'}  |
| cffex.IC0000 | czce.AP000   | 0.036005 | -1599.01 | 201.9003 | {'czce.AP000', 'cffex.IC0000'} |
| shfe.pb0000  | dce.c0000    | 0.043072 | 2461.587 | 15.93895 | {'dce.c0000', 'shfe.pb0000'}   |
| shfe.ru0000  | shfe.au0000  | 0.047359 | 220.7161 | 1.474282 | {'shfe.au0000', 'shfe.ru0000'} |
| shfe.au0000  | dce.l0000    | 0.048739 | -5984.3  | 100.5566 | {'shfe.au0000', 'dce.l0000'}   |
| shfe.zn0000  | shfe.ni0000  | 0.049059 | -73456.4 | 1836.178 | {'shfe.zn0000', 'shfe.ni0000'} |
| czce.OI000   | cffex.IC0000 | 0.04996  | -9661.04 | 126.899  | {'czce.OI000', 'cffex.IC0000'} |

- **s1, s2**: the code of the future
- **pvalue**: the significance value of the cointegration test
- **mean, std**: the mean and standard deviation of the diff price between future s1 and s2



## The Backtest result

![](image/backtest_result.png)
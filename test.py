# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 20:52:40 2024

@author: Hogan
"""
 
import datetime as dt
import pandas as pd
from tongubako import htfred
from tongubako.PCA import RPPCA
from tongubako.data_sample import sp500_close_price
from tongubako import plotify
from tongubako.alpha_vantage import AlphaVantage
from tongubako.technical_analysis import IchimokuCloud
from tongubako.technical_analysis import TDSequential

fred = htfred.FRED(apikey = "75d754e2105704e2fbb857cfc31db71b")

test1 = fred.get_series_info(sid='AMXTNO')
test2 = fred.get_series_data(sid='AMXTNO', freq='m', aggregate='eop', units='pc1', bound_type='last', start_date=dt.date(1995,1,1))
test3 = fred.get_series_data(sid='AMXTTI', freq='m', aggregate='eop', units='pc1', bound_type='last', start_date=dt.date(1995,1,1))
test4 = fred.get_series_data(sid='PPIACO', freq='m', aggregate='eop', units='pc1', bound_type='last', start_date=dt.date(1995,1,1))
data = test2.to_frame().join(test3, how='outer').join(test4, how='outer')


aplha_vantage = AlphaVantage(apikey='FMY7LTQMB0NZ4BPH')
sample = aplha_vantage.get_daily_time_series(symbol='AAPL', start_date=dt.date(2021,1,1), full_size=True, adjusted=True)




ichimoku = IchimokuCloud()
test1 = ichimoku.fit(sample['close'])
fig = ichimoku.plot(period=500)

td = TDSequential()
test1 = td.fit(O=sample['open'], H=sample['high'], L=sample['low'], C=sample['close'])

test = plotify.Constructor()

test.make_figure(x=data.index, y=data, labels=['Industrial New Orders YoY','Industrial Inventories YoY','PPI YoY'], axis=['L1','R1','R2'], figsize=(10,4), axis_shift=50, style=['-','--','-.'])
test1 = plotify.line(test)

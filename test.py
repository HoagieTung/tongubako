# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 20:52:40 2024

@author: Hogan
"""
 
import datetime as dt
import pandas as pd
from tongubako import htfred
from tongubako.PCA import RPPCA
from tongubako.data_sample import sp500_close_price, msft_ohlc
from tongubako import plotify
from tongubako.alpha_vantage import AlphaVantage
from tongubako.technical_analysis import IchimokuCloud
from tongubako.technical_analysis import TDSequential


fred = htfred.FRED(apikey = "75d754e2105704e2fbb857cfc31db71b")

test1 = fred.get_series_info(sid='PPIACO')
test2 = fred.get_series_data(sid='AMXTNO', freq='m', aggregate='eop', units='pc1', bound_type='last', start_date=dt.date(1995,1,1))
test3 = fred.get_series_data(sid='AMXTTI', freq='m', aggregate='eop', units='pc1', bound_type='last', start_date=dt.date(1995,1,1))
test4 = fred.get_series_data(sid='PPIACO', freq='m', aggregate='eop', units='pc1', bound_type='last', start_date=dt.date(1995,1,1))
data = test2.to_frame().join(test3, how='outer').join(test4, how='outer')


aplha_vantage = AlphaVantage(apikey='FMY7LTQMB0NZ4BPH')
sample = aplha_vantage.get_daily_time_series(symbol='MSFT', start_date=dt.date(2021,1,1), full_size=True, adjusted=False)




ichimoku = IchimokuCloud()
test1 = ichimoku.fit(sample['close'])
fig = ichimoku.plot(period=500)

td = TDSequential()
test1 = td.fit(O=sample['open'], H=sample['high'], L=sample['low'], C=sample['close'])

test = plotify.Constructor()

test.make_figure(x=data.index, y=data, labels=['Industrial New Orders YoY','Industrial Inventories YoY','PPI YoY'], axis=['L1','R1','R2'], figsize=(10,4), axis_shift=50, style=['-','--','-.'])
test1 = plotify.line(test)


from tongubako.dbmanager import SQL
test = SQL()
test.connect(user='admin', password='83I35jM8pAWSo6BekIa8v805',host='mistakenly-distinct-anchovy.a1.pgedge.io', dbname='htdb',port='5432')

testdata = pd.DataFrame(columns=['ID','Date','Value'])
testdata.loc[0] = ['Test', dt.date(2024,1,1),10.789]

test.insert_df_to_table(df=testdata, table_name='econdata', schema_name='datanexus', if_exists='replace', delete_whereclause='"ID"=\'Test\'')
test1 = test.get_data_from_table(table_name='econdata', schema_name='datanexus') 

 
from tongubako.dbnomics import DBnomics
test = DBnomics()
test1 = test.get_series_data(sid='ISM/pmi', details=True)
test2 = test.get_series_info(sid='ISM/pmi')
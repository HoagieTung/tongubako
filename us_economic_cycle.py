# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 18:50:39 2024

@author: homoi
"""

import datetime as dt
import pandas as pd
from tongubako import htfred
import statsmodels.api as sm
from tongubako.data_sample import sp500_close_price, msft_ohlc
from tongubako import plotify
from tongubako.alpha_vantage import AlphaVantage
from statsmodels.tsa.filters.cf_filter import cffilter
from tongubako.technical_analysis import IchimokuCloud
from tongubako.technical_analysis import TDSequential
fred = htfred.FRED(apikey = "75d754e2105704e2fbb857cfc31db71b")
grapher = plotify.Constructor()
def bema_filter(data, halflife=None, alpha=None):
    foward = data.ewm(halflife=halflife, alpha=alpha).mean()
    backward = data.sort_index(ascending=False).ewm(halflife=halflife, alpha=alpha).mean()
    return (foward+backward)/2


start_date = dt.date(1995,1,1)

new_order_ex_trans = fred.get_series_data(sid='AMXTNO', units='pc1', start_date=start_date)
inventory_ex_trans = fred.get_series_data(sid='AMXTTI', units='pc1', start_date=start_date)
ppi = fred.get_series_data(sid='PPIACO', units='pc1', start_date=start_date)
industrial_production = fred.get_series_data(sid='INDPRO', units='pc1', start_date=start_date)
durable_goods_sales = fred.get_series_data(sid='S423SMM144SCEN', units='pc1', start_date=start_date)
durable_goods_inventories = fred.get_series_data(sid='I423IMM144SCEN', units='pc1', start_date=start_date)

manufacture_demand = (new_order_ex_trans - inventory_ex_trans).rename('Manufacturing Demand YoY')
durable_goods_demand = (durable_goods_sales - durable_goods_inventories).rename('Durable Goods Demand YoY')
produciton = (ppi + industrial_production).rename('Nominal Industrial Production YoY')

original_data = manufacture_demand.to_frame().join(produciton, how='outer').join(inventory_ex_trans, how='outer')

data = original_data.apply(lambda x: bema_filter(x, alpha=0.25)).dropna()

cycle, trend = cffilter(data, 48-12, 48+12*2)



grapher.make_figure(x=data.index, y=data, labels=['Demand','Production','Inventory'], axis=['L1','R1','R2'], figsize=(10,4), axis_shift=50, style=['-','--','-.'])
test1 = plotify.line(grapher)


grapher.make_figure(x=data.index, y=cycle, labels=['Demand','Production','Inventory'], axis=['L1','R1','R2'], figsize=(10,4), axis_shift=50, style=['-','--','-.'])
test1 = plotify.line(grapher)


markov_data = data.iloc[:,0].dropna()
model = sm.tsa.MarkovRegression(markov_data.iloc[1:], k_regimes=2, exog=markov_data.iloc[:-1])
result = model.fit()
fuck = result.smoothed_marginal_probabilities[0]
fuck.plot()
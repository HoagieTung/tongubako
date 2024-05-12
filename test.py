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

from tongubako.technical_analysis import IchimokuCloud
fred = htfred.FRED(apikey = "75d754e2105704e2fbb857cfc31db71b")


test1 = fred.get_series_info(sid='AMXTNO')
test2 = fred.get_series_data(sid='AMXTNO', freq='m', aggregate='eop', units='pc1', bound_type='last', start_date=dt.date(1990,1,1))
test3 = fred.get_series_data(sid='AMXTTI', freq='m', aggregate='eop', units='pc1', bound_type='last', start_date=dt.date(1990,1,1))
data = test2.to_frame().join(test3, how='outer')

sample = sp500_close_price['A US Equity']

ichimoku = IchimokuCloud()
test1 = ichimoku.fit(sample)
ichimoku.plot(period=500)


test = plotify.Constructor()
test.add_data(x=data.index, y=data)
test.add_labels(['Industrial_New_Orders_YoY','Industrial_Inventories_Orders_YoY'])
test.set_axis(['L1','R1'])
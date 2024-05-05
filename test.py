# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 20:52:40 2024

@author: Hogan
"""

import datetime as dt
import pandas as pd
from tongubako.htfred import FRED
from tongubako.PCA import RPPCA
from tongubako.data_sample import sp500_close_price

from tongubako.technical_analysis import IchimokuCloud


test = FRED(apikey = "75d754e2105704e2fbb857cfc31db71b")
test1 = test.get_series_info(sid='GDP')
test2 = test.get_series_data(sid='PPIACO', freq='m', aggregate='eop', units='pc1', bound_type='last', start_date=dt.date(2021,1,1))


sample = sp500_close_price['AAPL US Equity']

test = IchimokuCloud()
test1 = test.fit(sample)
test.plot(period=500)

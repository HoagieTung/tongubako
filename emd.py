# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 21:19:32 2024

@author: Hogan
"""

import datetime as dt
import matplotlib.pyplot as plt
from tongubako.htfred import FRED

fred = FRED(apikey = "75d754e2105704e2fbb857cfc31db71b")
data = fred.get_series_data(sid='PPIACO', freq='m', aggregate='eop', units='yoy', bound_type='last', start_date=dt.date(1995,1,1))



def bema_filter(data, halflife=None, alpha=None):
    foward = data.ewm(halflife=halflife, alpha=alpha).mean()
    backward = data.sort_index(ascending=False).ewm(halflife=halflife, alpha=alpha).mean()
    return (foward+backward)/2

def find_extrema(data, extrema_type='max', fuzzy_span=None):
    
    return

data.plot()
mean = bema_filter(data, alpha=0.2)
mean.plot()
plt.show()

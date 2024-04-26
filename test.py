# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 20:52:40 2024

@author: Hogan
"""

import datetime as dt

from tongubako.htfred import FRED
from tongubako.PCA import RPPCA


test = FRED(apikey = "75d754e2105704e2fbb857cfc31db71b")
test1 = test.get_series_info(sid='GDP')
test2 = test.get_series_data(sid='PPIACO', freq='m', aggregate='eop', units='pc1', bound_type='last', start_date=dt.date(2021,1,1))
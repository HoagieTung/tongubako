# -*- coding: utf-8 -*-
"""
Created on Fri May 31 17:46:16 2024

@author: homoi
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import requests
import json
import datetime as dt

from . import settings

def process_time_series_daily(data, start_date=None, end_date=dt.datetime.now().date()):
    meta_data = pd.DataFrame.from_dict(data['Meta Data'], orient='index')
    time_series = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
    
    "Clean Meta Data"
    meta_data.index = ['Information', 'Symbol', 'Last Refreshed', 'Output Size','Time Zone']
    meta_data.loc['Last Refreshed',0] = dt.datetime.strptime(meta_data.loc['Last Refreshed',0], '%Y-%m-%d')
    
    "Clean Time Series"
    time_series.columns = ['open', 'high', 'low', 'close', 'volume']
    time_series.index = pd.Series(time_series.index).apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d').date())
    for col in ['open', 'high', 'low', 'close']:
        time_series[col] = time_series[col].apply(lambda x: float(x))
    time_series['volume'] = time_series['volume'].apply(lambda x: int(x))
    
    time_series = time_series[time_series.index<=end_date]
    if start_date is not None:
        time_series = time_series[time_series.index>=start_date]
    
    return {'Meta Data':meta_data, 'Time Series':time_series.sort_index()}

def process_time_series_daily_adjusted(data, start_date=None, end_date=dt.datetime.now().date()):
    meta_data = pd.DataFrame.from_dict(data['Meta Data'], orient='index')
    time_series = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
    
    "Clean Meta Data"
    meta_data.index = ['Information', 'Symbol', 'Last Refreshed', 'Output Size','Time Zone']
    meta_data.loc['Last Refreshed',0] = dt.datetime.strptime(meta_data.loc['Last Refreshed',0], '%Y-%m-%d')
    
    "Clean Time Series"
    time_series.columns = ['open', 'high', 'low', 'close', 'volume','dividend','adjusted_close','split_coef']
    time_series.index = pd.Series(time_series.index).apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d').date())
    for col in ['open', 'high', 'low', 'close','dividend','adjusted_close','split_coef']:
        time_series[col] = time_series[col].apply(lambda x: float(x))
    time_series['volume'] = time_series['volume'].apply(lambda x: int(x))
    
    time_series = time_series[time_series.index<=end_date]
    if start_date is not None:
        time_series = time_series[time_series.index>=start_date]
    
    return {'Meta Data':meta_data, 'Time Series':time_series.sort_index()}
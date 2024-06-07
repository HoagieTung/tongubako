# -*- coding: utf-8 -*-
"""
Created on Fri May 31 17:45:43 2024

@author: homoi
"""


import numpy as np
import pandas as pd
import datetime as dt
import requests
import json
from tongubako.utils import guess_frequency

from . import fetch_data, process_data

class AlphaVantage():
    def __init__(self, apikey, proxies=None):
        self.apikey = apikey
        self.proxies = proxies
        return
    
    def get_daily_time_series(self, symbol, start_date=None, end_date=dt.datetime.now().date(), meta_data=False, full_size=False):
        raw_data = fetch_data.get_time_series_daily(symbol=symbol, apikey=self.apikey, proxies=self.proxies)
        cleaned_data = process_data.process_time_series_daily(raw_data, start_date=start_date, end_date=end_date)
        if meta_data:
            return cleaned_data
        else:
            return cleaned_data['Time Series']
        
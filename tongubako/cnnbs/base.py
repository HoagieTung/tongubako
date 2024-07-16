# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 23:56:44 2024

@author: Hogan
"""

import numpy as np
import pandas as pd
import datetime as dt
import requests
from tongubako.utils import guess_frequency

from . import fetch_data, process_data

class CNNBS():
    def __init__(self, proxies=None):
        self.proxies = proxies
        self.data_list = pd.read_excel('tongubako//cnnbs//master_data.xlsx','data_list')
        self.data_dictionary = self.data_list.set_index('sid').to_dict(orient='index')
        return
    
    def search_sid(self, text):    
        return self.data_list[self.data_list['name'].str.contains(text)].reset_index(drop=True)
    
    def get_category_tree(self, category_id='zb', freq='M'):
        output = fetch_data.get_child_indicators(category_id=category_id, freq=freq, proxies=self.proxies)
        return output
    
    def get_series_data(self, sid, bound_type='last', start_date=dt.date(1990,1,1), end_date=dt.datetime.now().date(), details=True):
        info = self.data_dictionary[sid]
        category_id = info['category_id']
        nbs_name = info['nbs_name']
        freq = info['freq']
        category_data = self.get_category_data(category_id=category_id, freq=freq, start_date=start_date, end_date=end_date)
        category_data = category_data[category_data.index>=info['from'].date()]
        return category_data[nbs_name].rename(info['name'])
    
    def get_category_data(self, category_id, freq='M', bound_type='last', start_date=None, end_date=None, details=True):
        raw_data = fetch_data.fetch_category_data(category_id, freq=freq, proxies=self.proxies, period="1990-")
        cleaned_data = process_data.process_series_data(raw_data, freq, bound_type)
        if start_date is not None:
            cleaned_data = cleaned_data[cleaned_data.index>=start_date]
        if end_date is not None:
            cleaned_data = cleaned_data[cleaned_data.index<=end_date]
        return cleaned_data


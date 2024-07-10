# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 16:50:48 2024

@author: Hogan
"""


import numpy as np
import pandas as pd
import datetime as dt
import requests
from tongubako.utils import guess_frequency

from . import fetch_data, process_data, settings

class MacroIQ():
    def __init__(self, proxies=None):
        self.proxies = proxies
        self.data_list = pd.read_excel('tongubako//MacroIQ//dictionary.xlsx','data_list')
        self.data_dictionary = self.data_list.set_index('SID').to_dict(orient='index')
        return
    
    def get_function(self, sid):
        func = getattr(fetch_data, self.data_dictionary[sid]['Function'])
        return func
    
    
    def get_series_data(self, sid, units='default', bound_type='last', start_date=None, end_date=None, details=True):
        
        func = settings.FUNCTIONS[sid.upper()]
        func = self.get_function(sid)
        
        "get observations"
        data = func(sid=sid, units=units, proxies=self.proxies)
        freq = guess_frequency(pd.Series(data.index))
        observations = process_data.adjust_series_observation_bound(data, freq=freq, bound_type=bound_type)
        if start_date is not None:
            observations = observations[observations.index>=start_date]
        if end_date is not None:
            observations = observations[observations.index<=end_date]
        
        
        "get info"
        info = {}
        info['name'] = self.data_dictionary[sid]['Name']
        info['country'] = self.data_dictionary[sid]['Country']
        info['frequency'] = freq
        info['units'] = units
        
        if details:
            return {'info':info, 'observations':observations}
        else:
            return observations

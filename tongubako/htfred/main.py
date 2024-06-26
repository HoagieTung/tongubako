# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 22:45:20 2024

@author: Hogan
"""


import numpy as np
import pandas as pd
import datetime as dt
import requests
import json
from tongubako.utils import guess_frequency

from . import fetch_data, process_data

class FRED():
    def __init__(self, apikey, proxies=None):
        self.apikey = apikey
        self.proxies = proxies
        return
    
    def get_series_info(self, sid):
        return  fetch_data.get_series_info(sid, self.apikey, file_type='json', proxies=self.proxies)
    
    def get_series_data(self, sid, freq=None, aggregate='eop', units=None, bound_type='last', start_date=None, end_date=None, realtime_start=None, realtime_end=None, details=False):
        raw_data = fetch_data.get_series_observations(sid=sid, freq=freq , aggregate=aggregate, units=units, apikey=self.apikey, realtime_start=realtime_start, realtime_end=realtime_end, proxies=self.proxies)
        series_info = fetch_data.get_series_info(sid=sid, apikey=self.apikey, file_type='json', proxies=self.proxies)
        observations = process_data.process_series_observation(data=raw_data, point_in_time='last', drop_realtime=True).rename(columns={'value':sid+'_'+units if units is not None else sid})
        
        info = {}
        freq = guess_frequency(observations.index)
        info['frequency'] =  freq if freq != 'unknown' else series_info['frequency_short']
        info['sid'], info['name'] = series_info['id'], series_info['title']
        info['units'] = raw_data['units']
        info['last_update'] = dt.datetime.strptime(series_info['last_updated'].split(' ')[0],'%Y-%m-%d').date()
        info['seasonal_adjustment'] = series_info['seasonal_adjustment']
        
        observations = process_data.adjust_series_observation_bound(observations, info['frequency'], bound_type).squeeze()
        if start_date is not None:
            observations = observations[observations.index>=start_date]
        if end_date is not None:
            observations = observations[observations.index<=end_date]
        
        output = {}
        output['observations'] = observations
        output['info'] = info
        
        return output if details else observations
    



if __name__ =="__main__":
    test = FRED(apikey = "75d754e2105704e2fbb857cfc31db71b")
    test1 = test.get_series_info(sid='GDP')
    test2 = test.get_series_data(sid='PPIACO', freq='q', aggregate='eop', units='pc1', bound_type='last', start_date=dt.date(2021,1,1))
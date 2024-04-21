# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 22:45:20 2024

@author: Hogan
"""


import numpy as np
import pandas as pd
from datetime import datetime, timezone, timedelta, date
import requests
import json
from tongubako.utils import guess_frequency

import fetch_data, process_data

class FRED():
    def __init__(self, apikey):
        self.apikey = apikey
        return
    
    def get_series_info(self, sid):
        return  fetch_data.get_series_info(sid, self.apikey, file_type='json')
    
    def get_series_data(self, sid, freq=None, aggregate='eop', units=None, bound_type='last', realtime_start=None, realtime_end=None):
        raw_data = fetch_data.get_series_observations(sid=sid, freq=freq , aggregate=aggregate, units=units, apikey=self.apikey, realtime_start=realtime_start, realtime_end=realtime_end)
        series_info = fetch_data.get_series_info(sid=sid, apikey=self.apikey, file_type='json')
        observations = process_data.process_series_observation(data=raw_data, point_in_time='last', drop_realtime=True)
        
        output = {}
        freq = guess_frequency(observations.index)
        output['freq'] =  freq if freq != 'unknown' else series_info['frequency_short']
        output['sid'], output['title'] = series_info['id'], series_info['title']
        output['units'] = raw_data['units']
        
        observations = process_data.adjust_series_observation_bound(observations, output['freq'], bound_type)
        
        output['observations'] = observations.squeeze().rename(output['sid'])
        
        return output


if __name__ =="__main__":
    test = FRED(apikey = "75d754e2105704e2fbb857cfc31db71b")
    test1 = test.get_series_info(sid='GDP')
    test2 = test.get_series_data(sid='PPIACO', freq='q', aggregate='eop', units='pc1', bound_type='last')
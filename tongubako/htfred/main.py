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

import fetch_data, process_data

class FRED():
    def __init__(self, apikey):
        self.apikey = apikey
        return
    
    def get_series_data(self, sid, units='index', bound_type='default', realtime_start=None, realtime_end=None):
        raw_data = fetch_data.get_series_observations(sid=sid, apikey=self.apikey, realtime_start=realtime_start, realtime_end=realtime_end)
        info = fetch_data.get_series_info(sid=sid, apikey=self.apikey, file_type='json')
        raw_observation = process_data.process_series_observation(data=raw_data, point_in_time='last', drop_realtime=True)
        observation = process_data.adjust_series_observation_units(observation=raw_observation, info=info, units=units, bound_type=bound_type)
        return observation


if __name__ =="__main__":
    test = FRED(apikey = "75d754e2105704e2fbb857cfc31db71b")
    
    test1 = test.get_series_data(sid='NFCI', bound_type='first')
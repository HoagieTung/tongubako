# -*- coding: utf-8 -*-
"""
Created on Tue May 21 23:56:49 2024

@author: Hogan
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timezone, timedelta, date
import requests
import json 
from tongubako.utils import timeseries
from tongubako.utils import change_frequency, calculate_change, period_bound, align_dates, guess_frequency


def process_series_observations(data, bound_type='Last'):
    temp = data['series']['docs'][0]
    dates = pd.Series(temp['period_start_day']).apply(lambda x: datetime.strptime(x,'%Y-%m-%d').date())
    observations = pd.Series(index=dates, data=temp['value'], name=temp['series_name'])
    
    if bound_type.upper() in ['LAST']:
        observations = adjust_series_observation_bound(observations, temp['@frequency'], bound_type).squeeze()
    
    return observations

def process_series_info(data):
    series = data['series']['docs'][0]
    provider = data['provider']
    dataset = data['dataset']
    info = {}
    info['frequency'] = series['@frequency']
    info['name'] = series['dataset_name']
    info['provider'] = provider['name']
    info['last_update'] = datetime.strptime(dataset['indexed_at'].split('T')[0],'%Y-%m-%d').date()
    return info    
    

def adjust_series_observation_bound(observation, freq, bound_type='last'):
    if bound_type.upper() in ['DEFAULT','ORIGINAL']:
        pass
    else:
        observation.index = pd.Series(observation.index).apply(lambda x: period_bound(x, freq, bound_type=bound_type))
    
    return observation
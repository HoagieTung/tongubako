# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 17:06:10 2024

@author: Hogan
"""
import numpy as np
import pandas as pd
import datetime as dt

from tongubako.utils import timeseries
from tongubako.utils import change_frequency, calculate_change, period_bound

def process_series_observation(data, point_in_time='last', drop_realtime=True):
    observations = pd.DataFrame(data['observations'])
    observations['realtime_start'] = observations['realtime_start'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d').date())
    observations['realtime_end'] = observations['realtime_end'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d').date())
    observations['date'] = observations['date'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d').date())
    observations = observations.sort_values(by=['date','realtime_end','realtime_start'], ascending=[True, True, True])
    
    if point_in_time.upper() in ['LAST']:
        observations = observations.groupby('date').last()
    elif point_in_time.upper() in ['FIRST']:
        observations = observations.groupby('date').first()

    if drop_realtime:
        observations = observations.drop(['realtime_start','realtime_end'], axis=1)
    
    return observations

def adjust_series_observation_units(observation, info, units='index', bound_type='default'):
    
    observation = observation.rename(columns={'value':info['id']})
    
    "Adjust bound type"
    if bound_type.upper() in ['DEFAULT']:
        pass
    else:
        observation.index = pd.Series(observation.index).apply(lambda x: period_bound(x, info['frequency_short'], bound_type=bound_type))
    
    return observation
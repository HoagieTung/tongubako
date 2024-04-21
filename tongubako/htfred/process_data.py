# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 17:06:10 2024

@author: Hogan
"""
import numpy as np
import pandas as pd
import datetime as dt

from tongubako.utils import timeseries
from tongubako.utils import change_frequency, calculate_change, period_bound, align_dates, guess_frequency

def process_series_observation(data, point_in_time='last', drop_realtime=True):
    observations = pd.DataFrame(data['observations'])
    observations['realtime_start'] = observations['realtime_start'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d').date())
    observations['realtime_end'] = observations['realtime_end'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d').date())
    observations['date'] = observations['date'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d').date())
    observations = observations.sort_values(by=['date','realtime_end','realtime_start'], ascending=[True, True, True])
    observations = observations.replace('.',np.nan).dropna()
    
    if point_in_time.upper() in ['LAST']:
        observations = observations.groupby('date').last()
    elif point_in_time.upper() in ['FIRST']:
        observations = observations.groupby('date').first()

    if drop_realtime:
        observations = observations.drop(['realtime_start','realtime_end'], axis=1)
    
    return observations

def process_series_info_with_observation(info, observation):

    return


def adjust_series_observation_bound(observation, freq, bound_type='last'):
    
    if bound_type.upper() in ['DEFAULT']:
        pass
    else:
        observation.index = pd.Series(observation.index).apply(lambda x: period_bound(x, freq, bound_type=bound_type))
    
    return observation
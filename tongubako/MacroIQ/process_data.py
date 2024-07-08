# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 14:15:42 2024

@author: Hogan
"""

import numpy as np
import pandas as pd
import datetime as dt

from tongubako.utils import timeseries
from tongubako.utils import change_frequency, calculate_change, period_bound, align_dates, guess_frequency


def adjust_series_observation_bound(observation, freq, bound_type='last'):
    
    if bound_type.upper() in ['DEFAULT','ORIGINAL']:
        pass
    else:
        observation.index = pd.Series(observation.index).apply(lambda x: period_bound(x, freq, bound_type=bound_type))
    
    return observation
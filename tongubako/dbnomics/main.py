# -*- coding: utf-8 -*-
"""
Created on Tue May 21 21:48:42 2024

@author: Hogan
"""

import numpy as np
import pandas as pd
import datetime as dt
import requests
import json
from tongubako.utils import guess_frequency
from . import fetch_data, process_data

class DBnomics():
    def __init__(self, proxies=None):
        self.proxies = proxies
        return
    
    def get_series_data(self, sid, freq=None, aggregate='eop', units=None, bound_type='last', start_date=None, end_date=None, realtime_start=None, realtime_end=None, details=False):
        raw_data = fetch_data.get_series_observations(sid=sid)
        return raw_data


if __name__ =="__main__":
    
    test = DBnomics()
    
    test1 = test.get_series_data(sid=)
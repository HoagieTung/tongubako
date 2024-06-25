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
from . import fetch_data, process_data

class DBnomics():
    def __init__(self, proxies=None):
        self.proxies = proxies
        return
    
    def get_series_data(self, sid, bound_type='last', start_date=None, end_date=None, details=False):
        raw_data = fetch_data.get_series_observations(sid=sid)
        observations = process_data.process_series_observations(raw_data, bound_type=bound_type)
        
        if start_date is not None:
            observations = observations[observations.index>=start_date]
        if end_date is not None:
            observations = observations[observations.index<=end_date]
        
        if details:
            output = {}
            output['info'] = process_data.process_series_info(raw_data)
            output['observations'] = observations
            return output
        else:
            return observations
    
    def get_series_info(self, sid):
        raw_data = fetch_data.get_series_observations(sid=sid)
        info = process_data.process_series_info(raw_data)
        return info


if __name__ =="__main__":
    
    test = DBnomics()
    
    test1 = test.get_series_data(sid='ISM/pmi')
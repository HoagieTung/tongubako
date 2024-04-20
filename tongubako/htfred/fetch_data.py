# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 22:46:01 2024

@author: Hogan
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import requests
import json

import settings



def get_series_info(sid, apikey, file_type='json'):
    x = requests.get(settings.URL_SERIES_INFO.format(sid=sid, apikey=apikey, file_type=file_type))
    data = json.loads(x.content)['seriess'][0]
    if 'WEEKLY, ENDING FRIDAY' in data['frequency'].upper():
        data['frequency_short'] = 'BW'
    return data

def search_series(search_text, apikey, file_type='json'):
    x = requests.get(settings.URL_SERIES_SEARCH.format(search_text=search_text.replace(' ','+'), apikey=apikey, file_type=file_type))
    data = json.loads(x.content)
    return data['seriess']

def get_series_observations(sid, apikey, realtime_start=None, realtime_end=None, file_type='json'):
    url = settings.URL_SERIES_OBSERVATION.format(sid=sid, apikey=apikey, file_type=file_type)
    if realtime_start is not None:
        url += '&realtime_start={}'.format(realtime_start.strftime('%Y-%m-%d'))
    if realtime_end is not None:
        url += '&realtime_end={}'.format(realtime_end.strftime('%Y-%m-%d'))
    x = requests.get(url)
    data = json.loads(x.content)
    return data

if __name__ =="__main__":
    apikey = "75d754e2105704e2fbb857cfc31db71b"
    test1 = get_series_info(sid='NFCI', apikey=apikey)
    test2 = search_series(search_text='PPI Commodity', apikey=apikey)
    test3 = get_series_observations(sid='PPIACO', apikey=apikey, realtime_start=None, realtime_end=dt.date(2024,1,1))
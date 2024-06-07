# -*- coding: utf-8 -*-
"""
Created on Fri May 31 17:45:59 2024

@author: homoi
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import requests
import json

from . import settings


def get_time_series_daily(symbol, apikey, full_size=False, proxies=None):
    url = settings.TIME_SERIES_DAILY_URL.format(symbol=symbol, apikey=apikey)
    if full_size:
        url += '&outputsize=full'
    x = requests.get(url, proxies=proxies)
    data = json.loads(x.content)
    return data

def get_time_series_intraday(symbol, apikey, interval=5, full_size=False, month=None, proxies=None):
    url = settings.TIME_SERIES_INTRADAY_URL.format(symbol=symbol, apikey=apikey)
    if full_size:
        url += '&outputsize=full'
    if month is not None:
        url += 'month={month}'.format(month=month)
    x = requests.get(url, proxies=proxies)
    data = json.loads(x.content)
    return data
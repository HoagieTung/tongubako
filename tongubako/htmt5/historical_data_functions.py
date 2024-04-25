# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 22:56:31 2024

@author: Hogan
"""

import MetaTrader5
import numpy as np
import pandas as pd
import os
import pytz
from ht_tools import settings
from datetime import datetime, timezone, timedelta, date
import random
import os.path
import math


def MDP(ticker: str, field=None):
    symbol_info_dict = MetaTrader5.symbol_info(ticker)._asdict()
    info = {
        'description':symbol_info_dict.get('description'),
        'contract_size':symbol_info_dict.get('trade_contract_size'),
        'tick_size':symbol_info_dict.get('trade_tick_size'),
        'tick_value':symbol_info_dict.get('trade_tick_value'),
        'trade_mode':symbol_info_dict.get('trade_mode'),
        'volume_max':symbol_info_dict.get('volume_max'),
        'volume_min':symbol_info_dict.get('volume_min'),
        "point":symbol_info_dict.get('point'),
        }
    if field is None:
        return info
    else:
        return symbol_info_dict.get(field)


def MDH(ticker: str, n_obs: int, freq: str, end_time=datetime.now(pytz.UTC)+timedelta(hours=mt5_utc_offset), field=['open','high','low','close'], tz_offset=-mt5_utc_offset, start_time=None, timeout=10):

    start = datetime.now()
    while (datetime.now() - start).seconds<timeout:
        temp = MetaTrader5.copy_rates_from(ticker, frequency.get(freq), end_time, n_obs)
        if temp is not None:
            break
    if temp is None:
        return None
    
    rates = pd.DataFrame(temp)
    rates.index = pd.to_datetime(rates['time'], unit='s')
    rates.index += timedelta(hours=tz_offset)
    if start_time is not None:
        rates['Time'] = pd.Series(rates.index).values
        rates = rates[rates.Time>=start_time]
    return rates[field]



def MDS(tickers: list, n_obs: int, freq: str, end_time=datetime.now(pytz.UTC)+timedelta(hours=mt5_utc_offset), tz_offset=-mt5_utc_offset, field='close', start_time=None, timeout=10):
    series = [None for i in ticker_list]
    for i in range(len(tickers)):
        temp = MDH(tickers[i], n_obs, freq, end_time, field, tz_offset, start_time)
        if temp is None or len(temp)==0:
            continue
        series[i] = temp.squeeze().rename(ticker_list[i])
    output = pd.concat(series, axis=1, ignore_index=False)
    return output
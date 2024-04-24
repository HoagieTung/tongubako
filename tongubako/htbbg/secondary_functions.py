# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 20:22:33 2024

@author: Hogan
"""

from . import basic_functions
import datetime as dt
import math
import pandas as pd
import numpy as np
import time


def get_index_members(session, service_opened, index, date):
    if hasattr(date, 'strftime'):
        _date = int(date.strftime('%Y%m%d'))
    elif isinstance(date, str):
        _date = int(date)
    elif isinstance(date, int):
        _date = date
        
    temp = basic_functions.BDS(session=session, service_opened=service_opened, ticker=index, field="INDX_MWEIGHT_HIST", field_overrides={'END_DATE_OVERRIDE':_date}).iloc[:,0].squeeze()
    
    return temp


def BQL(session, service_opened, tickers, fields, start_date=None, end_date=dt.datetime.now().date, field_overrides=None, optional_parameters=None, periods_election='DAILY', all_columns='automatic', cd=None):
    if isinstance(tickers, str):
        tickers = [tickers]
    if isinstance(fields, str):
        fields = [fields]
    
    if start_date is None:
        data = []
        for k in tickers:
            data += [basic_functions.BDP(session, service_opened, k, fields, field_overrides)] 
        result = pd.concat(data,  axis=1).loc[fields, tickers]
    else:
        n = math.ceil(len(tickers)/50)
        data = []
        for j in range(n):
            subset = tickers[j*50:(j+1)*50]
            temp = basic_functions.BDH(session, service_opened, subset, fields, start_date, end_date, field_overrides, optional_parameters, periods_election)
            if isinstance(temp.columns[0], str):
                temp.columns = pd.MultiIndex.from_tuples([(subset[0], fields[0])])
            elif isinstance(temp.columns[0], tuple):
                pass

            data += [temp]
            if cd is not None:
                time.sleep(cd)
        result = pd.concat(data, axis=1).sort_index()
        
        if all_columns.upper() in ['AUTO','AUTOMATIC']:
            return result
        elif all_columns.upper() in ['YES','TRUE']:
            for ticker in tickers:
                for fld in fields:
                    if (ticker, fld) not in result.columns:
                        result[(ticker, fld)] = np.nan
            return result.loc[:, tickers]
        else:
            return None

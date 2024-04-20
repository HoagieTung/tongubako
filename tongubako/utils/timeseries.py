# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 23:05:31 2024

@author: Hogan
"""


import numpy as np
import pandas as pd
import datetime as dt
import calendar

YEAR_FREQ = ['YEAR','ANNUAL','ANNUALLY','A','Y']
MONTH_FREQ = ['M','MONTHLY','MONTH']
QUARTER_FREQ = ['Q','QUARTER','QUARTERLY']
WEEK_FREQ = ['W','WEEK','WEEKLY']
BUSINESS_WEEK_FREQ = ['BW','BUSINESS-WEEK','BUSINESS-WEEKLY']
DAY_FREQ = ['D','DAY','DAILY']


def most_recent_period_end(date, period):
    if isinstance(date, dt.datetime):
        date = date.date()
    if period.upper() in MONTH_FREQ:
        temp = date + dt.timedelta(days=1)
        result = dt.date(temp.year, temp.month, 1) - dt.timedelta(days=1)
    elif period.upper() in QUARTER_FREQ:
        temp = date + dt.timedelta(days=1)
        result = (temp - pd.offsets.QuarterEnd()).date()
    elif  period.upper() in WEEK_FREQ:
        result = date - dt.timedelta(days = date.weekday()+1) if date.weekday()<6 else date
    elif  period.upper() in YEAR_FREQ:
        temp = date + dt.timedelta(days=1)
        result = dt.date(temp.year, 1, 1) - dt.timedelta(days=1)
    return result
    
def period_bound(date, period, bound_type='last', offset=0):
    if isinstance(date, dt.datetime):
        date = date.date()
    if bound_type.upper() in ['LAST','END']:
        if period.upper() in MONTH_FREQ:
            result = dt.date(date.year, date.month, calendar.monthrange(date.year, date.month)[1])
        elif period.upper() in QUARTER_FREQ:
            result = (date - dt.timedelta(days=1) + pd.offsets.QuarterEnd()).date()
        elif  period.upper() in WEEK_FREQ:
            result = date + dt.timedelta(days = 6 - date.weekday())
        elif  period.upper() in BUSINESS_WEEK_FREQ:
            result = date + dt.timedelta(days = 6 - date.weekday())
        elif  period.upper() in YEAR_FREQ:
            result = dt.date(date.year, 12, 31)
    if bound_type.upper() in ['FIRST','START']:
        if period.upper() in MONTH_FREQ:
            result = dt.date(date.year, date.month, 1)
        elif period.upper() in QUARTER_FREQ:
            result = dt.date(date.year, 3 * ((date.month - 1) // 3) + 1, 1)
        elif  period.upper() in WEEK_FREQ:
            result = date - dt.timedelta(days = date.weekday())
        elif  period.upper() in BUSINESS_WEEK_FREQ:
            result = date - dt.timedelta(days = date.weekday())
        elif  period.upper() in YEAR_FREQ:
            result = dt.date(date.year, 1, 1)
    return result + dt.timedelta(days=offset)

def change_frequency(data, freq_from, freq_to, how='last'):
    temp = data.to_frame()
    if freq_to.upper() in MONTH_FREQ:
        if freq_from.upper() in WEEK_FREQ or freq_from.upper() in DAY_FREQ:
            temp['TimeGroup'] = pd.Series(temp.index).apply(lambda x: period_bound(x,'M')).values
        else:
            raise TypeError('Cannot convert {} to monthly freqeuncy'.format(freq_from))
    elif freq_to.upper() in WEEK_FREQ:
        if freq_from.upper() in DAY_FREQ:
            temp['TimeGroup'] = pd.Series(temp.index).apply(lambda x: period_bound(x,'W')).values
        else:
            raise TypeError('Cannot convert {} to monthly freqeuncy'.format(freq_from))
    elif freq_to.upper() in YEAR_FREQ:
        if freq_from.upper() in WEEK_FREQ or freq_from.upper() in DAY_FREQ or freq_from.upper() in MONTH_FREQ:
            temp['TimeGroup'] = pd.Series(temp.index).apply(lambda x: period_bound(x,'Y')).values
        else:
            raise TypeError('Cannot convert {} to monthly freqeuncy'.format(freq_from))
    
    if how.upper() in ['LAST']:
        result = temp.groupby('TimeGroup').last()
    elif how.upper() in ['FIRST']:
        result = temp.groupby('TimeGroup').first()
    elif how.upper() in ['AVERAGE','AVG','MEAN']:
        result = temp.groupby('TimeGroup').mean()
    elif how.upper() in ['MEDIAN','M']:
        result = temp.groupby('TimeGroup').median()
    
    return result


def calculate_change(data, how, freq):
    
    if how.upper() in ['YOY-PERCENTAGE','YOY P','YOY-P','YOY-PCT']:
        if freq.upper() in MONTH_FREQ:
            output = data.diff(12) / data.shift(12) * 100
        elif freq.upper() in QUARTER_FREQ:
            output = data.diff(4) / data.shift(4) * 100
        elif freq.upper() in WEEK_FREQ:
            output = data.diff(52) / data.shift(52) * 100
    elif how.upper() in ['YOY-CHANGE','YOY C','YOY-C','YOY-CHG']:
        if freq.upper() in MONTH_FREQ:
            output = data.diff(12)
        elif freq.upper() in QUARTER_FREQ:
            output = data.diff(4)
        elif freq.upper() in WEEK_FREQ:
            output = data.diff(52)
    elif how.upper() in ['MOM-PERCENTAGE','MOM P','MOM-P','MOM-PCT']:
        if freq.upper() in MONTH_FREQ:
            output = data.diff(1) / data.shift(1) * 100
        elif freq.upper() in QUARTER_FREQ:
            raise TypeError('Month-over-month is not compatible with quarterly frequency')
        elif freq.upper() in WEEK_FREQ:
            output = data.diff(4) / data.shift(4) * 100
    elif how.upper() in ['POP-PERCENTAGE','POP P','POP-P','POP-PCT']:
        output = data.diff(1) / data.shift(1) * 100
    elif how.upper() in ['POP-CHANGE','POP C','POP-C','POP-CHG']:
        output = data.diff(1)

    return output


if __name__ =="__main__":
    
    dates = pd.date_range(dt.date(2010,1,1), dt.date(2024,5,10), freq='D')
    data = pd.Series(index = dates, data=[np.random.rand() for i in dates], name='Test')
    
    test1 = change_frequency(data, freq_from='Day', freq_to='y', how='last')
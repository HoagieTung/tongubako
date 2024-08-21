# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 21:19:32 2024

@author: Hogan
"""
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from tongubako.htfred import FRED

fred = FRED(apikey = "75d754e2105704e2fbb857cfc31db71b")
data = fred.get_series_data(sid='PPIACO', freq='m', aggregate='eop', units='yoy', bound_type='last', start_date=dt.date(1995,1,1))



def bema_filter(data, halflife=None, alpha=None):
    foward = data.ewm(halflife=halflife, alpha=alpha).mean()
    backward = data.sort_index(ascending=False).ewm(halflife=halflife, alpha=alpha).mean()
    return (foward+backward)/2

def find_extrema(data, extrema_type='max', fuzzy_span=None):
    extremas = pd.DataFrame(index=data.index, data=np.nan, columns=['maxima','minima'])
    for i in range(1, len(data)-1):
        if data.iloc[i]>data.iloc[i-1] and data.iloc[i]>data.iloc[i+1]:
            extremas['maxima'].iloc[i] = data.iloc[i]
        elif data.iloc[i]<data.iloc[i-1] and data.iloc[i]<data.iloc[i+1]:
            extremas['minima'].iloc[i] = data.iloc[i]
    return extremas

def cubic_spline_interpolation(extremas, extrapolate=False):
    interpolation = pd.DataFrame(data=np.nan, index=extremas.index, columns=['upper','lower'])
    temp = extremas.copy()
    temp.index = pd.Series(extremas.index).apply(lambda x: (x-extremas.index[0]).days)
    "maxima interpolation"
    maximas = temp['maxima'].dropna()
    cs = CubicSpline(maximas.index, maximas, extrapolate=extrapolate)
    interpolation['upper'] = cs(temp.index)
    "minima interpolation"
    minimas = temp['minima'].dropna()
    cs = CubicSpline(minimas.index, minimas, extrapolate=extrapolate)
    interpolation['lower'] = cs(temp.index)
    
    return interpolation.ffill().bfill()

data.plot()
mean = bema_filter(data, alpha=0.25)
mean.plot()
plt.show()


extremas = find_extrema(data)
envelope = cubic_spline_interpolation(extremas)

envelope.plot()
plt.show()

class EMD:
    def __init__(self, x):
        self.x = x
        self.imf = []
        self.trend = []
    
    def find_extrema(self, data):
        extremas = pd.DataFrame(index=data.index, data=np.nan, columns=['maxima','minima'])
        for i in range(1, len(data)-1):
            if data.iloc[i]>data.iloc[i-1] and data.iloc[i]>data.iloc[i+1]:
                extremas['maxima'].iloc[i] = data.iloc[i]
            elif data.iloc[i]<data.iloc[i-1] and data.iloc[i]<data.iloc[i+1]:
                extremas['minima'].iloc[i] = data.iloc[i]
        return extremas
    
    def cubic_spline_interpolation(extremas, extrapolate=False):
        interpolation = pd.DataFrame(data=np.nan, index=extremas.index, columns=['upper','lower'])
        temp = extremas.copy()
        temp.index = pd.Series(extremas.index).apply(lambda x: (x-extremas.index[0]).days)
        "maxima interpolation"
        maximas = temp['maxima'].dropna()
        cs = CubicSpline(maximas.index, maximas, extrapolate=extrapolate)
        interpolation['upper'] = cs(temp.index)
        "minima interpolation"
        minimas = temp['minima'].dropna()
        cs = CubicSpline(minimas.index, minimas, extrapolate=extrapolate)
        interpolation['lower'] = cs(temp.index)
        
        return interpolation.ffill().bfill()
    
    def fit(self):
        
        return
    
    def is_imf(self, data):
        
        return
    
    def is_monotonic(self, data):
        
        return

    
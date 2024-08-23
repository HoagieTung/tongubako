# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 21:19:32 2024

@author: Hogan
"""
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline, BSpline
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

def cubic_spline_interpolation(extremas, extrapolate=True):
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
        self.x.index = list(self.x.index)
        self.imf = []
        self.residual = []
    
    def interpolate(self, data):
        temp = data.copy()
        temp.index = [i for i in range(len(data))]
        dots = temp.dropna()
        cs = CubicSpline(dots.index, dots, extrapolate=None)
        exrapolation = pd.Series(data=cs(temp.index), index=data.index)
  
        return exrapolation
    
    def find_optima(self, data, include_boundary=True):
        extremas = pd.DataFrame(index=data.index, data=np.nan, columns=['maxima','minima'])
        for i in range(1, len(data)-1):
            if data.iloc[i]>data.iloc[i-1] and data.iloc[i]>data.iloc[i+1]:
                extremas['maxima'].iloc[i] = data.iloc[i]
            elif data.iloc[i]<data.iloc[i-1] and data.iloc[i]<data.iloc[i+1]:
                extremas['minima'].iloc[i] = data.iloc[i]
        if include_boundary:
            if extremas['minima'].dropna().index[0]<extremas['maxima'].dropna().index[0]:
                extremas['maxima'].iloc[0] = data.iloc[0]
            else:
                extremas['minima'].iloc[0] = data.iloc[0]
            if extremas['minima'].dropna().index[-1]<extremas['maxima'].dropna().index[-1]:
                extremas['minima'].iloc[-1] = data.iloc[-1]
            else:
                extremas['maxima'].iloc[-1] = data.iloc[-1]
            
        return extremas
    
    def envelopes(self, extremas, extrapolate=False):
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
        
        return interpolation#.ffill().bfill()
    
    def fit(self):
        g = r = self.x.copy()
        
        while not self.is_monotonic(r):
            
            imf = self.extract_imf(g)
            r = g - imf
            g = r
            
            self.imf += [imf]
            
            imf.plot()
            r.plot()
            plt.show()
            
        self.residual = r
        
        return
    
    def extract_imf(self, data):
        h = data.copy()
        imf_condition = False
        while not imf_condition:
            g = h
            optimas = self.find_optima(g)
            envelopes = self.envelopes(optimas)
            m = envelopes.mean(axis=1, skipna=False)
            mHat = self.interpolate(m)
            h = g - m
            imf_condition = self.is_imf(h)

        return h
    
    def is_imf(self, data):
        optimas = self.find_optima(data)
        optimas = pd.melt(optimas.reset_index(), id_vars='index').dropna().sort_values(by='index').set_index('index')
        sign = np.sign(optimas['value']*optimas['value'].shift())
        return all(x<=0 for x in sign.dropna())
        
    
    def is_monotonic(self, data):
        return all(x<=y for x, y in zip(data, data.iloc[1:])) or all(x>=y for x, y in zip(data, data.iloc[1:]))


test = EMD(x=data)
test1 = test.find_optima(data)
test2 = test.envelopes(test1)

test2.plot()

test3 = test.fit()

    
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 21:13:12 2024

@author: Hogan
"""

from datetime import datetime, timedelta, time, date
import pandas as pd
import numpy as np
from tongubako.utils import ts_shift, guess_frequency
from statsmodels.tsa.ar_model import AR
import matplotlib.pyplot as plt

class IchimokuCloud:
    def __init__(self, short_period=9, long_period=26):
        self.short_period = short_period
        self.long_period = long_period
        return
    
    def fit(self, price):
        freq = guess_frequency(price.index)
        
        self.tenkan_sen = self.tenkan_sen(price)
        self.kijun_sen = self.kijun_sen(price)
        self.senkou_span_a = self.senkou_span_a(self.tenkan_sen, self.kijun_sen, freq)
        self.senkou_span_b = self.senkou_span_b(price, freq)
        self.chikou_span = self.chikou_span(price, freq)
        
        self.ichimoku_cloud = pd.DataFrame(price).join(self.tenkan_sen, how='outer').join(self.kijun_sen, how='outer').join(self.senkou_span_a, how='outer').join(self.senkou_span_b, how='outer').join(self.chikou_span, how='outer')
        
        return self.ichimoku_cloud
    
    def plot(self, start=None, end=None, period=None, figure_size=(16,10), legend=False, title=None, title_size=None):
        plt.style.use('seaborn')
        plt.rcParams['figure.figsize'] = figure_size
        fig=plt.figure()
        ax = fig.add_subplot(1,1,1)
        
        ichimoku_cloud = self.ichimoku_cloud
        if start is not None:
            ichimoku_cloud = self.ichimoku_cloud.loc[self.ichimoku_cloud.index>=start]
        if end is not None:
            ichimoku_cloud = self.ichimoku_cloud.loc[self.ichimoku_cloud.index<=end]
            
        if start is None and period is not None:
            ichimoku_cloud = ichimoku_cloud.iloc[-period:]
        
        x = ichimoku_cloud.index
        price, tenken, kijun, senkouA, senkouB, chikou = ichimoku_cloud.iloc[:,0], ichimoku_cloud['tenkan_sen'], ichimoku_cloud['kijun_sen'], ichimoku_cloud['senkou_span_a'], ichimoku_cloud['senkou_span_b'], ichimoku_cloud['chikou_span']

        ax.plot(x, price, label=price.name, color='black')
        ax.plot(x, tenken, label='Tenkan', color='blue')
        ax.plot(x, kijun, label='Kijun', color='red')
        ax.plot(x, chikou, label='Chikou', color='green')
        ax.fill_between(x, senkouA, senkouB, where=senkouA>=senkouB, color='green', label='Bullish Cloud', alpha=0.2)
        ax.fill_between(x, senkouA, senkouB, where=senkouA<senkouB, color='red', label='Bearish Cloud', alpha=0.2)
        
        if legend:
            ax.legend()
        
        if title is not None:
            plt.title(title, fontsize=title_size)
        
        plt.show()
        return fig
    
    def tenkan_sen(self, data):
        result = data.rolling(self.short_period).apply(lambda x: (max(x)+min(x))/2).squeeze().rename('tenkan_sen')
        return result
    
    def kijun_sen(self, data):
        result = data.rolling(self.long_period).apply(lambda x: (max(x)+min(x))/2).squeeze().rename('kijun_sen')
        return result
    
    def senkou_span_a(self, tenkan_sen, kijun_sen, freq):
        senkou_span_a = ((tenkan_sen+kijun_sen)/2).rename('senkou_span_a')
        result = ts_shift(senkou_span_a, freq, self.long_period)
        return result
    
    def senkou_span_b(self, data, freq):
        result = data.rolling(self.long_period*2).apply(lambda x: (max(x)+min(x))/2).squeeze().rename('senkou_span_b')
        result = ts_shift(result, freq, self.long_period)
        return result
    
    def chikou_span(self, data, freq):
        result = ts_shift(data, freq, -self.long_period)
        return result.rename('chikou_span')


if __name__ == '__main__':
    pass
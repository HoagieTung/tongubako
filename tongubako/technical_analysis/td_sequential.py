# -*- coding: utf-8 -*-
"""
Created on Wed May 29 02:01:57 2024

@author: homoi
"""

from datetime import datetime, timedelta, time, date
import pandas as pd
import numpy as np
from tongubako.utils import ts_shift, guess_frequency
import matplotlib.pyplot as plt

class TDSequential:
    def __init__(self, count_down_period=13):
        self.count_down_period = count_down_period
        return
    
    
    def fit(self, O, H, L, C):
        data0 = self.regulate_data(O, H, L, C)
        data1 = self.find_flip()
        data2 = self.setup()
        return
    
    def find_flip(self):
        for i in range(5, len(self.data.index)):
            if self.data['close'].iloc[i] < self.data['close'].iloc[i-4] and self.data['close'].iloc[i-1] > self.data['close'].iloc[i-5]:
                self.data.loc[self.data.index[i],'bear_flip'] = 1
            if self.data['close'].iloc[i] > self.data['close'].iloc[i-4] and self.data['close'].iloc[i-1] < self.data['close'].iloc[i-5]:
                self.data.loc[self.data.index[i],'bull_flip'] = 1
        return self.data

    
    def setup(self):
        for i in range(5, len(self.data.index)):
            "Buy setup"
            if self.data['bear_flip'].iloc[i]==1:
                self.data.loc[self.data.index[i],'buy_setup'] = 1
            elif self.data['buy_setup'].iloc[i-1]>=1:
                if self.data['close'].iloc[i]<self.data['close'].iloc[i-4]:
                    self.data.loc[self.data.index[i],'buy_setup'] = self.data['buy_setup'].iloc[i-1]+1
            
            "Sell setup"
            if self.data['bull_flip'].iloc[i]==1:
                self.data.loc[self.data.index[i],'sell_setup'] = 1
            elif self.data['sell_setup'].iloc[i-1]>=1:
                if self.data['close'].iloc[i]>self.data['close'].iloc[i-4]:
                    self.data.loc[self.data.index[i],'sell_setup'] = self.data['sell_setup'].iloc[i-1]+1
                    
        return self.data
    
    def find_prior_setup(self, i):
        prior_setup = {'buy':None, 'sell':None}
        
        for setuptype in ['buy_setup','sell_setup']:
            cutoff = i - self.data[setuptype].iloc[i]
            area = self.data
            priors = self.data.iloc[:cutoff+1]
            start = priors[priors[setuptype]==1].index[-1]
            period = priors[priors.index>=start]
            end = period[period[setuptype]==0].index[0]
            prior_setup[setuptype] = [start,end]
        
        return prior_setup
    
    def tdst(self, i):
        
        return
    
    def countdown(self, price, setup):
        if len(price.index) != len(setup.index):
            raise ValueError('Price series and setup series must have the same length')
        countdown = pd.DataFrame(index=self.price.index, data=0, columns=['buy','sell'])
        for i in range(2,len(price.index)):
            if setup['buy'].iloc[i] == 9:
                pass
        return
    
 
    
    def regulate_data(self, O, H, L, C):
        data = pd.DataFrame(O).join(H).join(L).join(C)
        if len(data.index)!=len(O) or len(data.index)!=len(H) or len(data.index)!=len(L) or len(data.index)!=len(C):
            raise ValueError('Open, high, low, close must have the same length')
        else:
            data.columns = ['open','high','low','close']
            self.price = data
        
        data[['bull_flip','bear_flip','buy_setup','sell_setup','buy_countdown','sell_countdown']] = 0
        self.data = data
        return data


if __name__ =="__main__":
    pass
    

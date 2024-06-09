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
        price = self.regulate_data(O, H, L, C)
        setup = self.setup(price)
        return
    
    
    def setup(self, price):

        setup = pd.DataFrame(index=self.price.index, data=0, columns=['buy','sell'])
        
        for i in range(5,len(self.price)):
            if (self.price['close'].iloc[i] > self.price['close'].iloc[i-4]) and (self.price['close'].iloc[i-1] < self.price['close'].iloc[i-5]) and (setup['sell'].iloc[i-1]==0):
                setup['sell'].iloc[i] = 1
            elif (8>=setup['sell'].iloc[i-1] >= 1) and (self.price['close'].iloc[i] > self.price['close'].iloc[i-4]):
                setup['sell'].iloc[i] = setup['sell'].iloc[i-1] + 1
        
        for i in range(5,len(self.price)):
            if self.price['close'].iloc[i] < self.price['close'].iloc[i-4] and self.price['close'].iloc[i-1] > self.price['close'].iloc[i-5] and setup['buy'].iloc[i-1]==0:
                setup['buy'].iloc[i] = 1
            elif 8>=setup['buy'].iloc[i-1] >= 1 and self.price['close'].iloc[i] < self.price['close'].iloc[i-4]:
                setup['buy'].iloc[i] = setup['buy'].iloc[i-1] + 1
        
        fuck = self.price.join(setup)
        
        return setup
    
    def countdown(self, price, setup):
        if len(price.index) != len(setup.index):
            raise ValueError('Price series and setup series must have the same length')
        countdown = pd.DataFrame(index=self.price.index, data=0, columns=['buy','sell'])
        for i in range(2,len(price.index)):
            if setup['buy'].iloc[i] == 9:
                pass
        return
    
    def find_flip(self, setup):
        
        return
    
    def find_entry(self, setup, price):
        if len(setup.index) != len(price.index):
            raise ValueError('Set up and price must have same length')
        return
    
    def regulate_data(self, O, H, L, C):
        data = pd.DataFrame(O).join(H).join(L).join(C)
        if len(data.index)!=len(O) or len(data.index)!=len(H) or len(data.index)!=len(L) or len(data.index)!=len(C):
            raise ValueError('Open, high, low, close must have the same length')
        else:
            data.columns = ['open','high','low','close']
            self.price = data

        return data
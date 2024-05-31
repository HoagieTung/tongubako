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
    def __init__(self, short_period=9, long_period=26):
        self.short_period = short_period
        self.long_period = long_period
        return
    
    
    def fit(self, O, H, L, C):
        price = self.regulate_data(O, H, L, C)
        
        return
    
    
    def set_up(self, price):

        setup = pd.DataFrame(index=self.price.index, data=0, columns=['bull','bear'])
        
        for i in range(5,len(self.price)):
            if self.price['close'].iloc[i]<self.price['close'].iloc[i-4] and self.price['close'].iloc[i-1]>self.price['close'].iloc[i-5] and setup['bear'].iloc[i-1]==0:
                setup['bear'].iloc[i] = 1
            elif 8>=setup['bear'].iloc[i-1]>=1 and self.price['close'].iloc[i]<self.price['close'].iloc[i-4]:
                setup['bear'].iloc[i] = setup['bear'].iloc[i] + 1
        
        for i in range(5,len(self.price)):
            if self.price['close'].iloc[i]>self.price['close'].iloc[i-4] and self.price['close'].iloc[i-1]<self.price['close'].iloc[i-5] and setup['bear'].iloc[i-1]==0:
                setup['bull'].iloc[i] = 1
            elif 8>=setup['bull'].iloc[i-1]>=1 and self.price['close'].iloc[i]<self.price['close'].iloc[i-4]:
                setup['bull'].iloc[i] = setup['bull'].iloc[i] + 1
            
        return setup
    
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
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 22:33:46 2024

@author: Hogan
"""

from datetime import datetime, timedelta, time, date
import pandas as pd
import numpy as np
from statsmodels.tsa.ar_model import AR

class KalmanFilter:
    def __init__(self):
        return
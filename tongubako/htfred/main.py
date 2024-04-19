# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 22:45:20 2024

@author: Hogan
"""


import numpy as np
import pandas as pd
from datetime import datetime, timezone, timedelta, date
import requests
import json

from tongubako.utils import change_frequency, calculate_change

class FRED():
    def __init__(self, api_key = "75d754e2105704e2fbb857cfc31db71b"):
        self.api_key = api_key
        return
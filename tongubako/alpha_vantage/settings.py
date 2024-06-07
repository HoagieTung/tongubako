# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 16:17:02 2024

@author: Hogan
"""



TIME_SERIES_DAILY_URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={apikey}'

TIME_SERIES_INTRADAY_URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}min&apikey={apikey}'
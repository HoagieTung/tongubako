# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 22:48:25 2024

@author: Hogan
"""

URL_SERIES_INFO = "https://api.stlouisfed.org/fred/series?series_id={sid}&api_key={apikey}&file_type={file_type}"
URL_SERIES_SEARCH = 'https://api.stlouisfed.org/fred/series/search?search_text={search_text}&api_key={apikey}&file_type={file_type}'
URL_SERIES_OBSERVATION = "https://api.stlouisfed.org/fred/series/observations?series_id={sid}&api_key={apikey}&file_type=json"
URL_RELEASE = "https://api.stlouisfed.org/fred/release/series?release_id={sid}&api_key={apikey}&file_type={file_type}"

UNITS = {
    'Change':'chg',
    'Change from Year Ago':'ch1',
    'Percent Change':'pch',
    'Percent Change from Year Ago':'pc1',
    'Compounded Annual Rate of Change':'pca',
    }

FREQUENCIES = {
    'Daily':'d',
    'Weekly':'w',
    'Biweekly':'bw',
    'Monthly':'m',
    'Quarterly':'q',
    'Seminannual':'sa',
    'Annual':'a',
    }

AGGREGATION = {
    'Average':'avg',
    'Sum':'sum',
    'End of Period':'eop',
    }
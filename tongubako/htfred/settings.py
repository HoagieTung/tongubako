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
    'yoy-chg':'ch1',
    'yoy-pct':'pc1',
    'ytd_pct':'pca',
    'pop-chg':'chg',
    'pop-pct':'pch'
    }
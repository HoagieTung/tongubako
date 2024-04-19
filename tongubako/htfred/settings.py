# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 22:48:25 2024

@author: Hogan
"""

URL_SERIES = "https://api.stlouisfed.org/fred/series?series_id={sid}&api_key={api}&file_type=json"
URL_RELEASE = "https://api.stlouisfed.org/fred/release/series?release_id={sid}&api_key={api}&file_type=json"
URL_DATA = "https://api.stlouisfed.org/fred/series/observations?series_id={sid}&realtime_start={start}&realtime_end={end}&api_key={api}&file_type=json"
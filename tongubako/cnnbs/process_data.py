# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 23:55:27 2024

@author: Hogan
"""

import numpy as np
import pandas as pd
import datetime as dt
from tongubako.utils import timeseries
from tongubako.utils import change_frequency, calculate_change, period_bound, align_dates, guess_frequency

def process_series_data(raw_data, freq, bound_type):
    # 整理为dataframe
    temp_df = pd.DataFrame(raw_data["returndata"]["datanodes"])
    temp_df["data"] = temp_df["data"].apply(
        lambda x: x["data"] if x["hasdata"] else None
    )

    wdnodes = raw_data["returndata"]["wdnodes"]
    wn_df_list = []
    for wn in wdnodes:
        wn_df_list.append(
            pd.DataFrame(wn["nodes"])
            .assign(
                funit=lambda df: df["unit"].apply(lambda x: "(" + x + ")" if x else x)
            )
            .assign(fname=lambda df: df["cname"] + df["funit"]),
        )

    row_name, column_name = (
        wn_df_list[0]["fname"],
        wn_df_list[1]["fname"],
    )

    data_ndarray = np.reshape(temp_df["data"], (len(row_name), len(column_name)))
    data_df = pd.DataFrame(data=data_ndarray, columns=column_name, index=row_name).T
    data_df.index.name = None
    data_df.columns.name = None
    
    data_df.index = pd.Series(data_df.index).apply(lambda x: transform_date(x, freq=freq))
    data_df = adjust_series_observation_bound(data_df, freq, bound_type)
    
    return data_df.sort_index()


def transform_date(Date, freq='M'):
    if freq.upper() in ['M','MONTHLY','MONTH']:
        try:
            output = dt.datetime.strptime(Date.replace(' ',''), '%b%Y').date()
        except:
            output = dt.datetime.strptime(Date.replace(' ',''), '%B%Y').date()
    elif freq.upper() in ['Q','QUARTER','QUARTERLY']:
        quarter, year = int(Date.replace(' ','').split('Q')[0]), int(Date.replace(' ','').split('Q')[1])
        output = dt.date(year=year, month=quarter*3, day=1)
    return output


def adjust_series_observation_bound(observation, freq, bound_type='last'):
    
    if bound_type.upper() in ['DEFAULT','ORIGINAL']:
        pass
    else:
        observation.index = pd.Series(observation.index).apply(lambda x: period_bound(x, freq, bound_type=bound_type))
    
    return observation
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 20:22:55 2024

@author: Hogan
"""

import blpapi
import datetime as dt

from . import admin, basic_functions, secondary_functions



class BloombergAPI():
    def __init__(self, host='localhost', port=8194):
        self.host = host
        self.port = port
        self.session = admin.initiate_bbg(self.host, self.port)
        self.service_opened = admin.initiate_service(session=self.session, service=["//blp/instruments","//blp/refdata"])
    
    def BDH(self, tickers, fields, start_date, end_date=dt.datetime.now().strftime('%Y%m%d'), periods_election='DAILY', field_overrides=None, optional_parameters=None):
        result = basic_functions.BDH(session=self.session, service_opened=self.service_opened, tickers=tickers, fields=fields, start_date=start_date, end_date=end_date, field_overrides=field_overrides, optional_parameters=optional_parameters, periods_election=periods_election)
        return result
    
    def BDS(self, ticker, field, field_overrides=None):
        result =  basic_functions.BDS(session=self.session, service_opened=self.service_opened, ticker=ticker, field=field, field_overrides=field_overrides)
        return result
    
    def BDP(self, ticker, fields, field_overrides=None):
        result = basic_functions.BDP(session=self.session, service_opened=self.service_opened, ticker=ticker, fields=fields, field_overrides=field_overrides)
        return result
    
    def BQL(self, tickers, fields, start_date=None, end_date=dt.datetime.now().date(), field_overrides=None, optional_parameters=None, periods_election='DAILY', all_columns='auto', cd=None, field_header=True):
        result = secondary_functions.BQL(session=self.session, service_opened=self.service_opened, tickers=tickers, fields=fields, start_date=start_date, end_date=end_date, field_overrides=field_overrides, optional_parameters=optional_parameters, periods_election=periods_election, all_columns=all_columns, cd=cd)
        if not field_header:
            result.columns = result.columns.droplevel(1)
        return result
    
    def get_index_members(self, index, date):
        result = secondary_functions.get_index_members(session=self.session, service_opened=self.service_opened, index=index, date=date)
        return result



if __name__ == '__main__': 
    
    test = BloombergAPI()
    
    test1 = test.BDH(tickers=['AAPL US Equity'], fields=['PX_LAST'], start_date=dt.date(2022,1,1))
    test2 = test.BDP(ticker='AAPL US Equity', fields=['CRNCY','PX_LAST'])
    test3 = test.BDS(ticker='AAPL US Equity', field='PG_REVENUE')
    test4 = test.BQL(tickers=['AAPL US Equity','IBM US Equity'], fields=['PX_LAST','CUR_MKT_CAP'])
    test4 = test.BQL(tickers=['AAPL US Equity','IBM US Equity','ATVI US Equity'], fields='PX_LAST', start_date=dt.date(2023,1,1))
    test5 = test.get_index_members('RIY Index', dt.date(2024,4,1))

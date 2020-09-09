from alpha_vantage.timeseries import TimeSeries
import os
import pickle
import pandas as pd

ts = TimeSeries(key=os.environ.get("ALPHA_VANTAGE_API_KEY"),output_format='pandas', indexing_type='date')

def _parse_meta(meta_data):
    symbol=meta_data.get("2. Symbol")
    last_ref=meta_data.get("3. Last Refreshed").replace(" ","-").replace(":","-")
    return symbol+last_ref

def _scrape_fullsize(ticker_list):
    cnt=0
    for ticker in ticker_list:
        cnt+=1
        try:
            df,meta_data = ts.get_intraday(ticker,interval="1min",outputsize='full')
            filename=_parse_meta(meta_data)+".p"
            with open(filename,"wb") as p:
                pickle.dump(df,p)
        except Exception as e:
            print(e,ticker)
        if cnt%10==0:
            print(cnt,"out of about 9000 finished")

# not checked yet
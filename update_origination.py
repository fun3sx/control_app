# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 00:08:20 2022

@author: User
"""

import api_functions
import requests
from bs4 import BeautifulSoup
import pandas as pd
import io
import datetime as dt
from dateutil.relativedelta import relativedelta


def read_from_bog():
    
    url = "https://www.bankofgreece.gr/RelatedDocuments/Rates_TABLE_1+1a.xls"
    #df = pd.read_excel(url,sheet_name='Loans_Amounts', index_col=0).iloc[7:,6]
    df = pd.read_excel(url,sheet_name='ΠΟΣΑ_ΔΑΝΕΙΩΝ', index_col=0).iloc[7:,6]

    
    #unpl.reset_index(drop=True, inplace = True)
  
    
    return df

def check_for_new(already_indb, df):
    #to put new item in db
    to_enter = []

    if len(already_indb) < len(df):
        to_enter = {'month': dt.datetime.strftime(df.index[-1],'%Y%m'), 'value' : df.iloc[-1]}
    
        df.drop(index=df.index[-1],axis=0,inplace=True)
    
    
    #update items already in db
    to_update = []
    
    #loop below finds the first instance where value is different
    for i in range(len(already_indb)):
        if float(already_indb[i]['value']) != round(df.iloc[i],6):
            #print('edw')
            to_update.append({'month': dt.datetime.strftime(df.index[i],'%Y%m'), 'value' : df.iloc[i]})
            
            #break
            

    return to_enter, to_update


def main(url):
    already_indb = api_functions.get(url)
    df = read_from_bog()
    
    
    #determine what needs update and what is new, if any
    to_enter, to_update = check_for_new(already_indb, df)
    
    #print (to_enter, to_update)
    
    #update data in db
    if len(to_update) > 0:
        print ('here, updating')
        for item in to_update:
            response = api_functions.patch(url, item)
            print (item, response.json(), response.status_code)
    
    
    #put new data to db
    if len(to_enter) > 0:
        print('entering new data')
        response = api_functions.put(url, to_enter)
        print(response.json(), response.status_code)
    
    #return df,already_indb
    return "all good from mortgage origination"

if __name__ == "__main__":

   #For testing locally    
   #url = "http://127.0.0.1:5000/mortgage-origination"
   #df,a = main(url)
   
   #For live use
   url = "https://api.interestingdata.eu/mortgage-origination"
   print (main(url))
   
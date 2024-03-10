# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 00:08:20 2022

@author: User
"""

import api_functions
import requests
import pandas as pd
from proxies import get_proxies
import random
from io import BytesIO
import datetime as dt



def read_from_bog():
    proxies = get_proxies()
    random.shuffle(proxies)
    
    bog_url = "http://www.bankofgreece.gr/RelatedDocuments/Rates_TABLE_1+1a.xls"
    
    #read data from bank of greece via proxy
    i=0
    while i<len(proxies):
        proxy_address = "http://" + proxies[i]['username'] + ":" + proxies[i]['password'] + "@" + proxies[i]['ip'] + ":" + str(proxies[i]['port'])
        print(proxies[i]['ip'])
        proxy_dict = {"http://" : proxy_address,
                      "https://": proxy_address}
        try:
            response = requests.get(bog_url, proxies = proxy_dict)
    
            filedata = BytesIO(response.content)
    
            df = pd.read_excel(filedata,sheet_name='Loans_Amounts', index_col=0).iloc[7:,6]
        except:
            i+=1
            continue
        
        break

    
    
    
    #df = pd.read_excel(url,sheet_name='Loans_Amounts', index_col=0).iloc[7:,6]
    #df = pd.read_excel(url,sheet_name='Loans_Amounts', index_col=0).iloc[7:,6]

    
  
    
    return df

def check_for_new(already_indb, df):
    #to put new item in db
    to_enter = []

    if len(already_indb) < len(df):
        num_items = len(df) - len(already_indb)
        for i in range(num_items):
            to_enter.append({'month': dt.datetime.strftime(df.index[-num_items + i],'%Y%m'), 'value' : df.iloc[-num_items + i]})
    
            df.drop(index=df.index[-num_items + i],axis=0,inplace=True)
    
    
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
    
    #print (to_enter)
    #print ('-'*5)
    #print (to_update)
    
    
    #update data in db
    if len(to_update) > 0:
        print ('here, updating')
        for item in to_update:
            response = api_functions.patch(url, item)
            print (item, response.json(), response.status_code)
    
    
    #put new data to db
    if len(to_enter) > 0:
       for item in to_enter:
           print('new data in db', item)
           response = api_functions.put(url, item)
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
   
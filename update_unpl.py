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


def read_from_elstat():
    url = "https://www.statistics.gr/el/statistics/-/publication/SJO02/2014-M02"
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
    htmltext  = requests.get(url, headers=header).content
    
    soup = BeautifulSoup(htmltext, "html.parser", from_encoding="utf-8")
    
    results = soup.find_all('table')[3].find_all('a')
    
    target = results[0].get('href')
    #target_text = results[0].get_text()
    
    with io.BytesIO(requests.get(target).content) as fh:
        df = pd.io.excel.read_excel(fh)
        
    unpl = df.iloc[2:,8].mask(df.iloc[2:,8]=='Ποσοστό ανεργίας').dropna()/100.0
    
    unpl.reset_index(drop=True, inplace = True)
    
    unpl = unpl.astype(float).round(3)
    
    months = []
    start_date = dt.datetime(2004,1,1)
    for i in range(len(unpl)):
        months.append((start_date + relativedelta(months=i)).strftime('%Y%m'))
        
    q = pd.DataFrame(months)
    
    return pd.concat([q,unpl], axis=1).set_axis(['month','value'], axis=1)

def check_for_new(already_indb, df):
    #to put new item in db
    to_enter = []

    if len(already_indb) < len(df):
        num_items = len(df) - len(already_indb)
        for i in range(num_items):
            to_enter.append({'month': df['month'].iloc[-num_items + i], 'value' : df['value'].iloc[-num_items + i]})
    
            df.drop(index=df.index[-num_items + i],axis=0,inplace=True)
    
    
    #update items already in db
    to_update = []
    
    #loop below finds the first instance where value is different
    for i in range(len(already_indb)):
        if float(already_indb[i]['value']) != df.iloc[i]['value']:
            #print('edw')
            to_update.append({'month': df['month'].iloc[i], 'value' : df['value'].iloc[i]})
            
            #break
            

    return to_enter, to_update


def main(url):
    
    already_indb = api_functions.get(url)
    
    df = read_from_elstat()
    
    #determine what needs update and what is new, if any
    to_enter, to_update = check_for_new(already_indb, df)
    
    #print (to_enter)
    #print('-'*5)
    #print(to_update)
    
    
    #update data in db
    if len(to_update) > 0:
        print ('here, updating')
        for item in to_update:
            response = api_functions.patch(url, item)
            print (item, response.json(), response.status_code)
    
    
    print ('-'*5)
   
    #put new data to db
    if len(to_enter) > 0:
       
       for item in to_enter:     
           print('new data in db', item)
           response = api_functions.put(url, item)
           print(response.json(), response.status_code)
    
    #return df
    return "all good from unpl"

if __name__ == "__main__":

   #url = "http://127.0.0.1:5000/unpl"
   url = "https://api.interestingdata.eu/unpl"
   print (main(url))
   #df = main(url)
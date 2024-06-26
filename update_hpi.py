# -*- coding: utf-8 -*-
"""
Created on Sat May 28 12:32:36 2022

@author: User
"""

import requests
import pandas as pd
import api_functions
#from proxies import get_proxies
#import random
from io import BytesIO
import os
from dotenv import load_dotenv, find_dotenv


def read_from_bog():
    load_dotenv(find_dotenv())
    
    proxy_address = os.environ.get("PROXY_ADDRESS")
    
    bog_url = "https://www.bankofgreece.gr/RelatedDocuments/TE_PRICES_INDICES_HISTORICAL_SERIES.xls"
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    proxy_dict = {"http" : proxy_address,
                  "https": proxy_address}
    
    response = requests.get(bog_url, headers = header, proxies = proxy_dict)
    '''
    #print(response.content)
    print(response.request.headers)
    print("Response Headers:")
    for header, value in response.headers.items():
        print(header, ":", value)
    '''   
        
    filedata = BytesIO(response.content)
    df = pd.read_excel(filedata)

    
    '''
    proxies = get_proxies()
    random.shuffle(proxies)
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
  
    #read data from bank of greece via proxy
    i=0
    while i<len(proxies):
        proxy_address = "http://" + proxies[i]['username'] + ":" + proxies[i]['password'] + "@" + proxies[i]['ip'] + ":" + str(proxies[i]['port'])
        print(proxies[i]['ip'])
        proxy_dict = {"http://" : proxy_address,
                      "https://": proxy_address}

        try:
            response = requests.get(bog_url, headers = header, proxies = proxy_dict)
    
            filedata = BytesIO(response.content)
            
            print("Response Headers:")
            for header, value in response.headers.items():
                print(header, ":", value)
    
            df = pd.read_excel(filedata, engine = 'xlrd')
        except Exception as e:
            print (e)
            i+=1
            continue
        
        break
    
    '''
    #read data from bank of greece
    #df = pd.read_excel("https://www.bankofgreece.gr/RelatedDocuments/TE_PRICES_INDICES_HISTORICAL_SERIES.xls")
    
    
    
    quarters, values = [],[]
    
    for i in range(16,len(df)):
        if len(str(df.iloc[i,0])) <= 5:
            for j in range(1,5):
                if isinstance(df.iloc[i,j],(int,float)):
                    #print (df.iloc[i,0])
                    #print (df.iloc[i,j])
                    #print ("-"*10)
                    quarters.append(str(df.iloc[i,0])+"Q"+str(j))
                    values.append(df.iloc[i,j])
                else:
                    #breakflag = True
                    break
        else:
            break
    return quarters, values

def check_for_new(already_indb, quarters, values):
    
    #to put new item in db
    to_enter = []
    if len(already_indb) < len(quarters):
        num_items = len(quarters) - len(already_indb)
        for i in range(num_items):
            to_enter.append({'quarter': quarters.pop(-num_items + i), 'value' : str(values.pop(-num_items + i))})
 

    #update items already in db
    to_update = []
    #loop below finds the first instance where quarter is different
    breakflag = False
    for i in range(len(already_indb)):
        if already_indb[i]['quarter'] != quarters[i]:
            #print('edw')
            breakflag = True
            break
    #print (i)
    if breakflag :
        for q,v in zip(quarters[i:],values[i:]):
            #print (q,v)
            to_update.append({'quarter':q,'value':str(v)})
    else:
        #print ('here2')
        i = len(list(filter(lambda x: '*' in x, quarters)))
        j=0
        #print (i)
        for q,v in zip(quarters[-i:],values[-i:]):
            if float(already_indb[-i+j]['value']) != v:
                to_update.append({'quarter':q,'value':str(v)})
            else:
                pass
            
            j+=1
        
    return to_enter, to_update

def main(url):
   already_indb = api_functions.get(url)

   quarters, values = read_from_bog()

   #determine what needs update and what is new, if any
   to_enter, to_update = check_for_new(already_indb, quarters, values)
   
   print(to_enter)
   print(to_update)
   
   
   #update data in db
   if len(to_update) > 0:
       print ('updated hpi', to_update)
       for item in to_update:
           response = api_functions.patch(url, item)
           print (response.json(), response.status_code)

   print ('-'*5)
   
   #put new data to db
   if len(to_enter) > 0:
       for item in to_enter:
           print('new data in db', item)
           response = api_functions.put(url, item)
           print(response.json(), response.status_code)
   
   
   
   return 'all good from hpi'    


if __name__ == "__main__":

   #url = "http://127.0.0.1:5000/hpi"
   url = "https://api.interestingdata.eu/hpi"
   
   print(main(url))
   
   #res = main(url)
   
  

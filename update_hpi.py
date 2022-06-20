# -*- coding: utf-8 -*-
"""
Created on Sat May 28 12:32:36 2022

@author: User
"""

import requests
import pandas as pd
import api_functions


def read_from_bog():
    #read data from bank of greece
    df = pd.read_excel("https://www.bankofgreece.gr/RelatedDocuments/TE_PRICES_INDICES_HISTORICAL_SERIES.xls")
    #df = pd.read_excel("TE_PRICES_INDICES_HISTORICAL_SERIES.xls")
    
    
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
        to_enter = {'quarter': quarters.pop(), 'value' : str(values.pop())}
    
    #update items already in db
    to_update = []
    #loop below finds the first instance where quarter is different
    breakflag = False
    for i in range(len(already_indb)):
        if already_indb[i]['quarter'] != quarters[i]:
            print('edw')
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
   
   #print (to_enter, to_update)
   
   #update data in db
   if len(to_update) > 0:
       print ('updated hpi', to_update)
       for item in to_update:
           response = api_functions.patch(url, item)
           print (response.json(), response.status_code)

   
   #put new data to db
   if len(to_enter) > 0:
       print('new data in db', to_enter)
       response = api_functions.put(url, to_enter)
       print(response.json(), response.status_code)
   
   
   return 'all good from hpi'    


if __name__ == "__main__":

   url = "http://127.0.0.1:5000/hpi"
   #url = "https://api.interestingdata.eu/hpi"
   print(main(url))
   #res = main(url)
   
  

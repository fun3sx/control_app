# -*- coding: utf-8 -*-
"""
Created on Sat May 28 12:32:36 2022

@author: User
"""
import api_functions
import requests
from bs4 import BeautifulSoup
import pandas as pd
import io


def read_from_elstat():
    url = "https://www.statistics.gr/el/statistics/-/publication/SEL84/-"

    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    htmltext  = requests.get(url, headers=header).content

    soup = BeautifulSoup(htmltext, "html.parser", from_encoding="utf-8")

    results = soup.find_all('table')[4].find_all('a')

    target = results[1].get('href')
    #target_text = results[1].get_text()

    #df = pd.read_excel(target,engine="xlrd")
    #df = pd.read_excel(open(target,'rb'))

    with io.BytesIO(requests.get(target).content) as fh:
        df = pd.io.excel.read_excel(fh)
        
    gdp = df.iloc[4:,2].dropna()
    gdp.reset_index(drop=True, inplace = True)

    y=1995
    quarters = []
    i=0
    while i< len(gdp): 
        for j in range(1,5):
            #print (y, 'q', j)
            quarters.append(str(y)+'Q'+str(j))
            i+=1
            if i == len(gdp):
               break
        y+=1
    
    q = pd.DataFrame(quarters)
    
    
    return pd.concat([q,gdp], axis=1).set_axis(['quarter','value'], axis=1)



def check_for_new(already_indb, df):
    #to put new item in db
    to_enter = []

    if len(already_indb) < len(df):
        num_items = len(df) - len(already_indb)
        for i in range(num_items):
            to_enter.append({'quarter': df['quarter'].iloc[-num_items + i], 'value' : df['value'].iloc[-num_items + i]})
        
            df.drop(index=df.index[-num_items + i],axis=0,inplace=True)
    
    
    #update items already in db
    to_update = []
    #loop below finds the first instance where value is different
    for i in range(len(already_indb)):
        if float(already_indb[i]['value']) != df.iloc[i]['value']:
            #print('edw')
            to_update.append({'quarter': df['quarter'].iloc[i], 'value' : df['value'].iloc[i]})
            
            #break


    return to_enter, to_update

def main(url):
    already_indb = api_functions.get(url)
    #print(already_indb[-1])
    
    df = read_from_elstat()
    
    #for i in range(104,108):
        #df.iloc[i]['value'] = 123456.0+i
    
    #determine what needs update and what is new, if any
    #to_enter, to_update = check_for_new(already_indb, pd.concat([df,pd.DataFrame({'quarter': ['2022Q1'], 'value': [12431.4664]})],ignore_index=True))
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
    
    
    return 'all good from gdp'
    


    
if __name__ == "__main__":

   #url = "http://127.0.0.1:5000/gdp"
   url = "https://api.interestingdata.eu/gdp"
   print (main(url))

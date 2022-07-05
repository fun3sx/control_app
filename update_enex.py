# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 18:59:51 2022

@author: User
"""
import api_functions
import requests
from bs4 import BeautifulSoup
import pandas as pd
import io
import datetime as dt
from dateutil.relativedelta import relativedelta
import json
import warnings

def main(url):
    date = dt.datetime.strftime(dt.datetime.now(),"%Y%m%d")
    
    print (date)
    
    filename = "https://www.enexgroup.gr/documents/20126/200106/"+date+"_EL-DAM_Results_EN_v01.xlsx"
    
    
    
    print (filename)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        df = pd.read_excel(filename,engine="openpyxl")
        
    df.drop(labels = ['DDAY','DELIVERY_MTU','TARGET', 'BIDDING_ZONE_DESCR','DELIVERY_DURATION', 'PUB_TIME','VER'],axis=1,inplace=True)
    
    mask = df['CLASSIFICATION'].isin(['HV','MV','LV','CRETE LOAD','LOSSES'])
    df1 = df[~mask]
    
    df1.reset_index(drop=True, inplace = True)
    
    al_gr_imports = df[df.ASSET_DESCR == 'AL-GR']
    bg_gr_imports = df[df.ASSET_DESCR == 'BG-GR']
    mk_gr_imports = df[df.ASSET_DESCR == 'MK-GR']
    tr_gr_imports = df[df.ASSET_DESCR == 'TR-GR']
    it_gr_imports = df[df.ASSET_DESCR == 'IT-GR']
    cr_gr_imports = df[df.ASSET_DESCR == 'CR-GR']
    gr_al_exports = df[df.ASSET_DESCR == 'GR-AL']
    gr_bg_exports = df[df.ASSET_DESCR == 'GR-BG']
    gr_mk_exports = df[df.ASSET_DESCR == 'GR-MK']
    gr_it_exports = df[df.ASSET_DESCR == 'GR-IT']
    gr_tr_exports = df[df.ASSET_DESCR == 'GR-TR']
    gr_cr_exports = df[df.ASSET_DESCR == 'GR-CR']
    
    
    pump = df[df.CLASSIFICATION == 'PUMP']
    
    big_hydro = df[df.CLASSIFICATION == 'Big Hydro']
    crete_conventional = df[df.CLASSIFICATION == 'CRETE CONVENTIONAL']
    crete_renewables = df[df.CLASSIFICATION == 'CRETE RENEWABLES']
    lignite = df[df.CLASSIFICATION == 'Lignite']
    natural_gas = df[df.CLASSIFICATION == 'Natural Gas']
    res = df[df.CLASSIFICATION == 'RES']

    #data = requests.get(url, {'day':date})
    
    #date = str(int(date)+1)
    #print (date)
    
    to_enter = {'day':date,
                'al_gr': json.dumps(al_gr_imports.set_index(['SORT'],drop=False).to_dict(orient='index')),
                'bg_gr': json.dumps(bg_gr_imports.set_index(['SORT'],drop=False).to_dict(orient='index')),
                'mk_gr': json.dumps(mk_gr_imports.set_index(['SORT'],drop=False).to_dict(orient='index')),
                'tr_gr': json.dumps(tr_gr_imports.set_index(['SORT'],drop=False).to_dict(orient='index')),
                'it_gr': json.dumps(it_gr_imports.set_index(['SORT'],drop=False).to_dict(orient='index')),
                'cr_gr': json.dumps(cr_gr_imports.set_index(['SORT'],drop=False).to_dict(orient='index')),
                'gr_al': json.dumps(gr_al_exports.set_index(['SORT'],drop=False).to_dict(orient='index')),
                'gr_bg': json.dumps(gr_bg_exports.set_index(['SORT'],drop=False).to_dict(orient='index')),
                'gr_mk': json.dumps(gr_mk_exports.set_index(['SORT'],drop=False).to_dict(orient='index')),
                'gr_tr': json.dumps(gr_it_exports.set_index(['SORT'],drop=False).to_dict(orient='index')),
                'gr_it': json.dumps(gr_tr_exports.set_index(['SORT'],drop=False).to_dict(orient='index')),
                'gr_cr': json.dumps(gr_cr_exports.set_index(['SORT'],drop=False).to_dict(orient='index')),
                'pump': json.dumps(pump.set_index(['SORT'],drop=False).to_dict(orient='index')),
                'crete_conventional': json.dumps(crete_conventional.set_index(['SORT'],drop=False).to_dict(orient='index')),
                'crete_renewables': json.dumps(crete_renewables.set_index(['SORT'],drop=False).to_dict(orient='index')),
                'big_hydro': json.dumps(big_hydro.set_index(['SORT'],drop=False).to_dict(orient='index')),
                'lignite': json.dumps(lignite.set_index(['SORT'],drop=False).to_dict(orient='index')),
                'natural_gas': json.dumps(natural_gas.set_index(['SORT'],drop=False).to_dict(orient='index')),
                'res': json.dumps(res.set_index(['SORT'],drop=False).to_dict(orient='index'))
                }
    
    
    
    #put new data to db
    if len(to_enter) > 0:
        print('entering new data')
        response = api_functions.put(url, to_enter)
        print(response.json(), response.status_code)
    
    #return df
    return "all good from enex"

if __name__ == "__main__":

   url = "http://127.0.0.1:5000/enex"
   #url = "https://api.interestingdata.eu/unpl"
   print (main(url))
   #df = main(url)
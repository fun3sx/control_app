# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 19:25:57 2022

@author: User
"""

import datetime as dt

from update_gdp import main as main_gdp
from update_hpi import main as main_hpi
from update_unpl import main as main_unpl


print (dt.datetime.now().strftime("%Y/%m/%d - %H:%M"))


base_url = "https://api.interestingdata.eu/"
#base_url = "127.0.0.1:5000"

#check and update HPI

print (main_hpi(base_url+'hpi'))

#check and update GDP

print (main_gdp(base_url+'gdp'))

#check and update unemployment

print (main_unpl(base_url+'unpl'))




print ('-'*10)

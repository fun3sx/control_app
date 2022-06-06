# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 19:25:57 2022

@author: User
"""

import datetime as dt

from update_gdp import main as main_gdp
from update_hpi import main as main_hpi


print (dt.datetime.now().strftime("%Y/%m/%d - %H:%M"))


base_url = "https://api.interestingdata.eu/"

#check and update HPI

print (main_hpi(base_url+'hpi'))

#check and update GDP

print (main_gdp(base_url+'gdp'))



print ('-'*10)

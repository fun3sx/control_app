# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 19:25:57 2022

@author: User
"""

import datetime as dt

from update_enex import main as main_enex

print (dt.datetime.now().strftime("%Y/%m/%d - %H:%M"))


base_url = "https://api.interestingdata.eu/"
#base_url = "127.0.0.1:5000"

#check and update enex data

print (main_enex(base_url+'enex'))




print ('-'*10)

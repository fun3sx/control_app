# -*- coding: utf-8 -*-
"""
Created on Sat May 28 12:32:36 2022

@author: User
"""

import requests

def get(url):
    return requests.get(url).json()

#vazw nea grammi
def put(url, data):
    return requests.put(url,json=data)
    
#kanw update ena row
def patch(url, data):
    return requests.patch(url,json=data)
    



   




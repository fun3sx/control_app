# -*- coding: utf-8 -*-


import requests
import os
from dotenv import load_dotenv, find_dotenv


def get_proxies():
    load_dotenv(find_dotenv())
    
    token = os.environ.get("TOKEN")
       
    #get available proxies
    response = requests.get(
        "https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page=1&page_size=25",
        headers={"Authorization": f"Token {token}"}
    ).json()
    
    #get proxies port username pass
    proxies = []
    
    for item in response['results']:
        proxy = {}
        proxy['ip'] = item['proxy_address']
        proxy['port'] = item['port']
        proxy['username'] = item['username']
        proxy['password'] = item['password']
        
        proxies.append(proxy)
        #break
        
    
    site = "http://google.com"
    
    discard = []
    
    for i in range(len(proxies)):
        try:
            #print(f"using {proxies[i]['ip']}")
            res = requests.get(site, proxies = {"http": "http://" + proxies[i]['username'] + ":" + proxies[i]['password'] + "@" + proxies[i]['ip'] + ":" + str(proxies[i]['port']),
                                                "https": "https://" + proxies[i]['username'] + ":" + proxies[i]['password'] + "@" + proxies[i]['ip'] + ":" + str(proxies[i]['port'])
                                                })
            #print (res.status_code)
            if res.status_code != 200:
                discard.append(i)
        except requests.RequestException as e:
            #print ("fail")
            #print (e)
            #print('-')
            discard.append(i)
    
    #print(discard)
    
    proxies = [proxies[i] for i in range(len(proxies)) if i not in discard]
    
    return proxies
            

if __name__ == "__main__":

   proxies = get_proxies()
   
            
            
            
            
            
            
            
            
            
            
            
            
            
            
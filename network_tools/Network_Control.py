'''
Created on Jan 21, 2016

@author: zachary
'''
import urllib
import re
import time
import definition_parser as dp

def check_network_conection():
    '''Sends a url request to google
    this is meant to check network connection'''
    try:
        response=urllib.urlopen('http://www.google.com')
        return True
    except Exception, e:
        print("No Network Connection: "+str(e))
        return False
    
liss = ["work", "with", "me", "Goerge"]

if check_network_conection():
    for item in liss:
        print("Working On: "+item+"\n")
        dp.definition_search(item)
        time.sleep(0.5)
        

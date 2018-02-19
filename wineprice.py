from bs4 import BeautifulSoup
import os
import re
import operator
from itertools import groupby
import requests

class WinePrice:
    def __init__(self, name):
        self.__urlfullpath="https://www.wine-searcher.com/find/{winename}/1/usa/-/x"
        self.__name = name
        self.__urlname = str(name).replace(" ","+")
        
    def getprice(self):
        newurl= self.__urlfullpath.replace("{winename}",self.__urlname)
        r=requests.get(newurl)
        if r.is_redirect == False and r.ok:
            soup = BeautifulSoup(r.content,'html.parser')
            try:
                resulttbl=soup.find('table', {'class':'nltbl'}).find_all('tr',{'class':'wlrwdt'})[0]
                value=resulttbl.find_all('td')[2]
                return value.text
            except:
                pass

        return ""

#myprice=WinePrice("Château Beausejour (Duffau Lagarrosse)")
#value=myprice.getprice()
#print (value)
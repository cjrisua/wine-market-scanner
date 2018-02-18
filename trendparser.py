from bs4 import BeautifulSoup
import urllib2
import re
import argparse
import wineclasslib as wlib
import operator
from itertools import groupby
import requests

#parser = argparse.ArgumentParser()
#parser.add_argument("--input", help='input filename')

#args = parser.parse_args()

url = "https://www.cellartracker.com/list.asp?fInStock=0&Table=List&iUserOverride=0&Wine=Ch%E2teau+Montrose"

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
page = opener.open(url).read()

soup = BeautifulSoup(page,'html.parser')

items = []
parsed_items = []
main_table = soup.find('table', {'id':'main_table'})
for row in main_table.findAll('tr'):
    name = ""
    region = ""
    winetype = ""
    for column in row.findAll('td'):
        if column.has_attr('class') and column['class'] == ['type']:
            winetype = column.find('a').attrs['title']
        elif column.has_attr('class') and column['class'] == ['name']:
            m  = re.search('^(?P<vinatge>[0-9]+)\s+(?P<name>.+?)$', column.find('h3').contents[0])
            vinatge = m.group('vinatge')
            producer = m.group('name')
            items.append(vinatge+"@"+producer)
            items.append(column.find('span', {'class':'el loc'}).contents[0])

            name = "%s %s" % (vinatge, producer)
            region = column.find('span', {'class':'el loc'}).text

        elif column.has_attr('class') and column['class'] == ['dates']:
            m = re.search('[0-9.]+', column.find('span', {'class':'el gty'}).contents[0])
            items.append(m.group(0))
        elif column.has_attr('class') and column['class'] == ['score']:
            m = re.search('[0-9.]+', column.find('a', {'class':'action'}).contents[0])
            score = m.group(0)
            items.append(score)
    if items:
        parsed_items.append(wlib.Wine(name, region, winetype))
        #mywine = wlib.Wine(name, region, winetype)
        #parsed_items.append("@".join(items).replace('\n',''))
        items = []  

parsed_items.sort(key=operator.attrgetter("producer"), reverse=False)

for key, value in groupby(filter(lambda x: x.varaietal == "unknow", parsed_items), key=lambda w: w.producer):
    print (key)
    for wine in value:
        print ("\t %s %s" % (wine.vintage, wine.varaietal))
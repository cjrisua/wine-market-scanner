from bs4 import BeautifulSoup
import os
import re
import operator
from itertools import groupby
import wineclasslib as wlib
#import request

#url = 
#"https://www.cellartracker.com/list.asp?iUserOverride=268253&Table=List&Country=Portugal"
#"https://www.cellartracker.com/list.asp?O=Quantity+DESC&VB=2005&iUserOverride=0&Table=List&Country=France&VT=2005"
#https://www.cellartracker.com/list.asp?O=Quantity+DESC&Country=France&VB=2005&iUserOverride=0&Table=List&VT=2005&Page=2
#https://www.cellartracker.com/list.asp?iUserOverride=268253&Table=List&Country=Portugal"


#content = urllib2.urlopen(url).read()
for root, dirs, files in os.walk("./webpages"):
    for filename in files:
        print ("%s" % (filename))
        htmldoc = open(root+"//"+filename,"r", encoding="ISO-8859-1")
        soup = BeautifulSoup(htmldoc,'html.parser')

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
                    soupresult=column.find('h3')
                    if soupresult is not None:
                        m  = re.search('^(?P<vinatge>([0-9]+|NV))\s+(?P<name>.+?)$', soupresult.contents[0])
                        vinatge = m.group('vinatge')
                        producer = m.group('name')
                        items.append(vinatge+"@"+producer)
                        items.append(column.find('span', {'class':'el loc'}).contents[0])

                        name = "%s %s" % (vinatge, producer)
                        region = column.find('span', {'class':'el loc'}).text

                    else:
                        print ("say what")
                elif column.has_attr('class') and column['class'] == ['dates']:
                    m = re.search('[0-9.]+', column.find('span', {'class':'el gty'}).contents[0])
                    items.append(m.group(0))
                elif column.has_attr('class') and column['class'] == ['score']:
                    soupresult=column.find('a', {'class':'action'})
                    if soupresult is not None:
                        m = re.search('[0-9.]+',soupresult.contents[0])
                        score = m.group(0)
                        items.append(score)
            if items:
                parsed_items.append(wlib.Wine(name, region, winetype))
                #parsed_items.append("@".join(items).replace('\n',''))
                items = []
        htmldoc.close()
        break

parsed_items.sort(key=operator.attrgetter("producer"), reverse=False)

for key, value in groupby(filter(lambda x: x.varaietal == "unknow", parsed_items), key=lambda w: w.producer):
    print (key)
    for wine in value:
        print ("\t %s %s" % (wine.vintage, wine.varaietal))
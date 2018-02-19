from bs4 import BeautifulSoup
import os
import re
import operator
from itertools import groupby
import wineclasslib as wlib
import wineprice as wprice
#import request

#url = 
#"https://www.cellartracker.com/list.asp?iUserOverride=268253&Table=List&Country=Portugal"
#"https://www.cellartracker.com/list.asp?O=Quantity+DESC&VB=2005&iUserOverride=0&Table=List&Country=France&VT=2005"
#https://www.cellartracker.com/list.asp?O=Quantity+DESC&Country=France&VB=2005&iUserOverride=0&Table=List&VT=2005&Page=2
#https://www.cellartracker.com/list.asp?iUserOverride=268253&Table=List&Country=Portugal"


#content = urllib2.urlopen(url).read()
parsed_items = []

for root, dirs, files in os.walk("./webpages"):
    for filename in files:
        print ("%s" % (filename))
        htmldoc = open(root+"//"+filename,"r", encoding="ISO-8859-1")
        soup = BeautifulSoup(htmldoc,'html.parser')

        items = []
        main_table = soup.find('table', {'id':'main_table'})
        for row in main_table.findAll('tr'):
            name ="" 
            region=""
            score=""
            winetype = ""
            bottelcount = 0
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
                    m = re.search('[0-9,]+', column.find('span', {'class':'el gty'}).contents[0])
                    items.append(m.group(0))
                    if m.group(0).replace(",","").isdigit():
                        bottelcount = int(m.group(0).replace(",",""))
                         
                elif column.has_attr('class') and column['class'] == ['score']:
                    soupresult=column.find('a', {'class':'action'})
                    if soupresult is not None:
                        m = re.search('[0-9.]+',soupresult.contents[0])
                        score = m.group(0)
                        items.append(score)
            if items:
                winebottel=wlib.Wine(name, region, winetype) 
                if score != "":
                    winebottel.addscore(float(score))
                winebottel.updatebottlecount(bottelcount)

                parsed_items.append(winebottel)
                #parsed_items.append("@".join(items).replace('\n',''))
                items = []
        htmldoc.close()

parsed_items.sort(key=operator.attrgetter("producer"), reverse=False)

output=open("./output/st-emilion.txt", "wb")
header="Vintage,Château,Type,Score,Bottel Count,Price\n"
output.write(header.encode('utf8'))

for key,value in groupby(parsed_items, lambda w : w.producer):
    wvinatges=list(value)
    scoreless = list(filter(lambda w: w.score != "", wvinatges))
    if len(scoreless) >= 10:
        #avergageprice=wprice.WinePrice(key)
        #value=avergageprice.getprice()
        for bottle in wvinatges:
            try:
                line = "{0},{1},{2},{3},{4},{5}\n".format(
                    bottle.vintage, bottle.producer, 
                    bottle.type, bottle.score, bottle.count, value)
                output.write(line.encode('utf8'))
            except UnicodeEncodeError:
                print ("UnicodeEncodeError wine: {0}".format(key))
    elif not wvinatges:
        print ("No wine found for: {0}".format(key))
    else:
        print ("{0} count {1} of 10".format(key, len(scoreless)))
output.close()  

#for key,value in groupby(filter( lambda w: w. , parsed_items)):
#    try:
#        output.write("%s@%s@%s@%s@%s\n" %(bottle.vintage, bottle.producer, bottle.type, bottle.score, bottle.count))
#    except UnicodeEncodeError:
#        print ("UnicodeEncodeError wine: %s" %(bottle.producer))
#output.close()


#for key, value in groupby(filter(lambda x: x.varaietal == "unknow", parsed_items), key=lambda w: w.producer):
#    for wine in value:
#        print ("\t %s %s" % (wine.vintage, wine.varaietal))

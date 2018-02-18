from bs4 import BeautifulSoup
import os

#pageIndex = "1"
#url = "http://www.cellaraiders.com/bordeaux-wines-online-french-bordeaux-wine-cellaraiders-c-25_35.html?page=\{index\}&sort=1a"
#url = "http://www.cellaraiders.com/burgundy-c-25_36.html?page=\{index\}&sort=1a"
#url = "http://www.cellaraiders.com/spain-south-american-wines-sale-spanish-wines-online-c-23.html?page=\{index\}&sort=1a"
#url ="http://www.cellaraiders.com/blends-merlot-cabernet-sauvignon-merlot-wine-c-26_43.html?page=\{index\}&sort=1a"

file = open("cali-datadump.txt", "w", encoding="utf-8")

for root, dirs, files in os.walk("./webpages"):
    for filename in files:
        htmldoc = open(root+"//"+filename,"r", encoding="utf-8")
        soup = BeautifulSoup(htmldoc.read(), "html.parser")
        
        for s in soup.find_all("span"):
            items = list(enumerate(s.children))
            if len(s.attrs) == 0 and "Display" in items[0][1].string:
                _from = items[1][1].text
                _to = items[3][1].text
                _total = items[5][1].text

                print ("%s %s" % (_from, _to))
                if int(_to) < int(_total):
                    pageIndex = str(int(pageIndex)+1)
                    break
                else:
                    _continue = False

    #cellar raider (productListingData)
#    productTable = soup.find("table", {"class": "productListingData"})
#    for tablerow in productTable.children:
#        if tablerow.name == "tr":
#            line = ""
#            for wineinfo in tablerow.children:
#                if wineinfo.name == "td":
#                    if wineinfo.string is None:
#                        line += "\t"
#                    else:
#                        line += "\t" + wineinfo.string
#            file.write(line +"\n")
file.close()
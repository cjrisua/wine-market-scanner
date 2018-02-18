import mysql.connector
import csv
import glob

from mysql.connector import errorcode
from datetime import date, datetime, timedelta

cnx = mysql.connector.connect(  user='somm', 
                            password='W1ne14Fun', 
                            host='127.0.0.1', 
                            database='vinifera')
cursor = cnx.cursor(named_tuple=True, buffered=True)
trendfiles = glob.glob('*.csv')
for file in trendfiles:
    with open(file,'rt') as csvfile:
        streamreader = csv.reader(csvfile, delimiter='@', quotechar='|')
        for row in streamreader:
            name = row[1].replace("\"","\\\"")
            sql =  'SELECT idwine, name FROM vinifera.wine WHERE name = "%s"' % (name,)
            cursor.execute(sql)
            count = cursor.rowcount
            wineid = -1
            if count == 0:
                add_wine = 'INSERT INTO wine (idwine, name) VALUES (0,"%s")' % (name,)
                cursor.execute(add_wine)
                wineid = cursor.lastrowid
            else:
                result = cursor.fetchall()
                for winerow in result:
                        wineid = "%d" % (winerow[0],)
            
            wineinfo = {
                'vintage' : row[0],
                'score' :  row[4],
                'bottlecount' : row[3],
                'addeddate' : datetime.now().date(),
                'idwine' : wineid,
            }
            
            add_vinatge = 'INSERT INTO vintage (idvintage,year,score,bottlecount,addeddate,idwine) VALUES (0,%(vintage)s,%(score)s,%(bottlecount)s,\'%(addeddate)s\',%(idwine)s)' % (wineinfo)
            cursor.execute(add_vinatge)

            cnx.commit()

cursor.close()
cnx.close()
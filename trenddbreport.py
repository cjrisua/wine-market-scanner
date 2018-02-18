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

sql =  'SELECT name, score, year, bottlecount FROM vinifera.wine AS w INNER JOIN vinifera.vintage AS v on v.idwine = w.idwine ORDER BY name, year'
cursor.execute(sql)

results = cursor.fetchall()
file =  open ('vintagesummary.csv', 'w')
file.write('name\tscore\tyear\tbottlecount\n')
for row in results:
    item = "%s\t%d\t%d\t%s" % (row[0], row[1], row[2], row[3],)    
    file.write(item + '\n')

file.close()
cursor.close()
cnx.close()
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 17:36:58 2020

@author: EmileVDH
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 19:29:09 2020

@author: EmileVDH

This Script goes into each html page and extract some meta data
We want to know how mant varibles are populated in the table 
and what the column names are for our next step
We also store the meta data in a table in SQL

"""

#loop through archive pages and return the column names so we can see how it has changed over time


import requests
from bs4 import BeautifulSoup
import pandas as pd
#

#x=V.fulllink[V.date=='20200129']
#y=V.fulllink[V.date.isin(['20200401'],['20200402'],['20200403'])]
#x = V.fulllink[(V.date=='20200401') |( V.date=='20200402')| (V.date=='20200403')]
##Read WEB PAGE live HTML CODE
#URL = 'https://www.worldometers.info/coronavirus/#countries'

##Read archive page
#URL = 'https://web.archive.org/web/20200412000004/www.worldometers.info/coronavirus/'
#URL = 'https://web.archive.org/web/20200301001656/www.worldometers.info/coronavirus/'
#URL = V.fulllink[56]
#URL = V.fulllink[88]
#print(URL)
#x=V.fulllink[(V.date=='20200403')]

#type(results2)
#type(results1)
#
#isinstance(results1,type(None))
#isinstance(results2,  type(None)  )
#isinstance(results3, bs4)

x=V.fulllink

TheColumnListT=list()
linknameT=list()
counterT=list()
responseT=list()


for link in x :
    print(link)
    page=requests.get(link)
    linknameT.append(link)
    response=page.status_code
    responseT.append(response)
    #print(page.status_code)  
    soup = BeautifulSoup(page.content, 'html.parser')
    results1 = soup.find(id='table3')
    results2 = soup.find(id='main_table_countries')
    results3 = soup.find(id='main_table_countries_today')
    print(results1)
    print(results2)
    print(results3)
    if isinstance(results2,type(None)) & isinstance(results3,type(None)) :
         qu=results1
    elif isinstance(results1,type(None)) & isinstance(results3,type(None)) :
         qu=results2
    elif isinstance(results1,type(None)) & isinstance(results2,type(None)) :
         qu=results3
    else :
         qu=('no result')  ##continue to top 
    if isinstance(results2,type(None)) & isinstance(results3,type(None)) & isinstance(results1,type(None)) :
         continue 
    result=qu
    content = result.find_all('th')
    cnt=0
    TheColumnList=list()
    for data in content:
        if len(data.text)<1 :
            continue 
        TheColumnList.append(data.text.strip())
        cnt=cnt+1
    counterT.append(cnt)
    TheColumnListT.append(TheColumnList)
    
print(linknameT)    
print(TheColumnListT)
print(counterT)
print(responseT)

J=pd.DataFrame(list(zip(linknameT, responseT, counterT,TheColumnListT )),
              columns=['linkfull','Response', 'VariableCount','TheColumns'])


W= pd.merge(V, J, left_on='fulllink', right_on='linkfull')


#CSV FILE
W.to_csv('ColumnsOfWorldoMeters3.csv' ,index=False)

#rename reserved world 

W.rename(columns={'date':'DateEntry'}, inplace=True)

W.DateEntry=W.DateEntry.astype(str)
W.month=W.month.astype(str)
W.fulllink=W.fulllink.astype(str)
W.TheColumns=W.TheColumns.astype(str)
W.timestamp=W.timestamp.astype(str)

H=W[['timestamp', 'DateEntry', 'month', 'fulllink', 'VariableCount', 'TheColumns','length']]

##ADD TO DATABASE FOR METADATATABLE
# DATAFRAME TO SQL 

import sqlite3
from pandas import DataFrame

conn = sqlite3.connect('CovidData.db')
c = conn.cursor()

c.execute('CREATE TABLE CovidMeta (timestamp, DateEntry, month, fulllink, VariableCount, TheColumns,length)')
conn.commit()

H.info()

#Cars = {'Brand': ['Honda Civic','Toyota Corolla','Ford Focus','Audi A4'],
#        'Price': [22000,25000,27000,35000]
#        }

#df = DataFrame(Cars, columns= ['Brand', 'Price'])

H.to_sql('CovidMeta', conn, if_exists='replace', index = False)
 
c.execute('''  
SELECT * FROM CovidMeta
          ''')

for row in c.fetchall():
    print (row)






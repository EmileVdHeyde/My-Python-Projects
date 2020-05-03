# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 19:38:52 2020

@author: EmileVDH


Here we are scraping the actual data for any given date for this same webpage table

We parse the data into lists of list and then into a df 

the df is edited then pushed to Sql 


"""

#import os
#os.getcwd() 
#os.chdir('C:\\Users\\EmileVDH')
#
###Fetch link from database from META DATA Table################33
import sqlite3
from pandas import DataFrame


H=['timestamp', 'DateEntry', 'month', 'fulllink', 'VariableCount', 'TheColumns','length']


conn = sqlite3.connect('CovidData.db')
c = conn.cursor()

c.execute(''' SELECT DateEntry,fulllink FROM CovidMeta ''')


df = DataFrame(c.fetchall(), columns=['DateEntry','fulllink'])    
print (df)

c.execute('''  SELECT * FROM CovidMeta ''')
full = DataFrame(c.fetchall(), columns=H)    
print (full)



###############################################
#full[full.VariableCount==13]

#13 columns
#71 to 90 

############## Extract data from HTML ################################3

import urllib.request, urllib.parse, urllib.error
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#################

import json
import requests
from bs4 import BeautifulSoup
import pandas as pd 

jj=int(input())
url =df.iloc[jj]['fulllink']

MAX_RETRIES = 20
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
session.mount('https://', adapter)

r = session.get(url)
print(r.content)

#raw_data = page.read()
#encoding = page.info().get_content_charset('utf8')  # JSON default
#data = json.loads(page.decode(encoding))

#soup = BeautifulSoup(page.content, 'html.parser')
soup = BeautifulSoup(r.content, 'html.parser')

results1 = soup.find(id='table3')
results2 = soup.find(id='main_table_countries')
results3 = soup.find(id='main_table_countries_today')
    
if isinstance(results2,type(None)) & isinstance(results3,type(None)) :
         qu=results1
elif isinstance(results1,type(None)) & isinstance(results3,type(None)) :
         qu=results2
elif isinstance(results1,type(None)) & isinstance(results2,type(None)) :
         qu=results3
else :
         qu=('no result')

results = qu
print(results)

#sploitting by varibles 
content = results.find_all('td')
print(content)

lister=list()
i = 1
for data in content:
      if data.text==' ' :
          lister.append(0)
      else :
       lister.append(data.text)
print(lister)



#### Create nested lists ################################################

#How many variables
var=full.iloc[jj]["VariableCount"]


#what are the variables remove remove " ,   " make a list 
varstring=full.iloc[jj]['TheColumns'].replace("',", "|")

varlist=list(varstring.replace(",", "_").replace("'", "").replace("]", "").replace("[", "").replace(" ", "").split("|"))
print(varlist)
 
#what are the counties shown  max 
Countries=len(lister[::var])


#make a list of list , innner list is a set for a country
i=0
new_list=[]
while i<len(lister):
  new_list.append(lister[i:i+var])
  i+=var

print(new_list)

######Dataframe creating and edit #######################################


vv=pd.DataFrame(new_list , columns=varlist) #dtype={'Day': str,'Wind':int64}))

#New Column for Day it entered 
vv['ReportingDate']= full.iloc[jj]['DateEntry']

#look at dataframe 
#vv.describe()
#vv.info()  #all onjets not typed  can we bulk text and bulk numbers
#vv.shape()
#vv.dtypes

#convert Data Types??

#1 remove these rows specified in list , they are summary lines 


excl = ["North America" , 'Europe' ,'Asia','South America','Oceania','Africa','World','Total:',' ']

ww = vv[~vv.Country_Other.isin(excl)]
#ww.describe()


#vv.Country_Other.strip()

#2 Create a date variable with reporting date string YYYMMDD

vv['DateTime'] = pd.to_datetime(vv['ReportingDate'].astype(str), format='%Y%m%d')

#3 create a date stamp for when it was created.

from datetime import datetime
# datetime object containing current date and time
now = datetime.now()
print("now =", now)
## dd/mm/YY H:M:S
#dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#print("date and time =", dt_string)	

vv['RunAudit']=now

######################Store into a Database Table(S)###############

import sqlite3
from pandas import DataFrame

conn = sqlite3.connect('CovidData.db', timeout=10)
c = conn.cursor()
#
#c.execute('CREATE TABLE Covid  (   Country , TotalCases   ,NewCases ,TotalDeaths, NewDeaths, Recoverd     ,ActiveCases    ,Critical, CasePerMillion, DeathsPerMillion, TotalTests, TestPerMillion, Continent,ReportingDate,DateTime,RunAudit )')
#conn.commit()

vv.info()

#vv.to_sql('Covid', conn, if_exists='replace', index = False)

vv.to_sql('Covid', conn, if_exists='append', index = False)


c.execute('''  
SELECT distinct ReportingDate FROM Covid
          ''')

conn.commit()
for row in c.fetchall():
    print (row)
    
print('Done')

conn.close()



#pip install django
#from django import db
#db.connection.close_all()






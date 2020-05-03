# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 09:58:18 2020

@author: EmileVDH

This Script looks at the Links archived for this website 
which has a csv of all the links to the snap shot.

We extract from web , filter out some records and the make a Dataframe
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

#URL = 'https://web.archive.org/web/*/http://www.worldometers.info/coronavirus/'
URL= 'http://web.archive.org/cdx/search/cdx?url=worldometers.info/coronavirus/&output=csv'

page = requests.get(URL)
print(page)

#columnNames = ["urlkey","timestamp","original","mimetype","statuscode","digest","length"]

#split by spaces
#
#df=pd.read_csv(URL)
#
#df=pd.read_csv(URL, delimiter=' ')

#F=pd.read_csv(URL, header=None, delimiter=r"\s+")
pull=pd.read_csv(URL, names=["urlkey","timestamp","original","mimetype","statuscode","digest","length"], delimiter=r"\s+")

#to reset df 
F=pull   

##ONLY TAKE STATUS CODE 200 AND TEXT HTLM 

F = F[(F.statuscode=='200') & (F.mimetype=='text/html')]

#REMOVE DUPLICATES
F = F.sort_values('length', ascending=False)
F = F.drop_duplicates(keep='first')

#F=F.drop_duplicates()  #5832
#object types
F.info()
F.timestamp=F.timestamp.astype(str)

#treat duplicates 

#new columnns 
# Daye first 6 characters 
F.insert(2,'date',F.timestamp.str[:8])
F.insert(3,'month',F.timestamp.str[:6])
#count through order 
#using date as partition and order by timestamp asc 

#df['Rank'] = df.groupby(by=['C1'])['C2'].transform(lambda x: x.rank())

F.insert(1,'dayrow',F.groupby(by=['date'])['timestamp'].transform(lambda x: x.rank()))

A =F[(F.dayrow==1)]


#build a list of urls using
#https://web.archive.org/web/20200331235308/https://www.worldometers.info/coronavirus/

snap=A.timestamp

links=list()
timestamp=list()
for row in snap : 
    print('https://web.archive.org/web/'+ row + '/https://www.worldometers.info/coronavirus/')
    links.append('https://web.archive.org/web/'+ row + '/https://www.worldometers.info/coronavirus/')
    timestamp.append(row)

#make dictionary of two lists 

#dictionary6 = dict(zip(timestamp, links))
#c = map(lambda x,y:(x,y),a,b)

atup= list(zip(timestamp, links))

dz=pd.DataFrame(atup,columns=['key','fulllink'])


V= pd.merge(A, dz, left_on='timestamp', right_on='key')
V= V.sort_values('key', ascending=True)
V.reset_index(drop=True, inplace=True)
#type(linksTup)
#dir(linksTup)
   

##add to final table join on linkkey




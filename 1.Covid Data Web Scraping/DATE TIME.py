# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 13:21:53 2020

@author: EmileVDH
"""

from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
 
print("now =", now)

# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("date and time =", dt_string)	



from datetime import date

today = date.today()

# dd/mm/YY
d1 = today.strftime("%d/%m/%Y")
print("d1 =", d1)

# Textual month, day and year	
d2 = today.strftime("%B %d, %Y")
print("d2 =", d2)

# mm/dd/y
d3 = today.strftime("%m/%d/%y")
print("d3 =", d3)

# Month abbreviation, day and year	
d4 = today.strftime("%b-%d-%Y")
print("d4 =", d4)

# using dictionary to convert specific columns 
#convert_dict = {'Country_Other': object }, 
#                'Continent ': object
#               } 
#  
#vv.Country_Other = vv.Country_Other.astype(convert_dict) 
#
#vv = vv.infer_objects() 

# using apply method 
df[['A', 'C']] = df[['A', 'C']].apply(pd.to_numeric) 
#1 remove these rows specified in list , they are summary lines 
excl = ["North America" , 'Europe' ,'Asia','South America','Oceania','Africa','World','Total:',' ']

ww = vv[~vv.Country_Other.isin(excl)]
ww.describe()


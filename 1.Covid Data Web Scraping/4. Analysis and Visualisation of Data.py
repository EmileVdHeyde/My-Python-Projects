# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 11:34:35 2020

@author: EmileVDH


Using a diferent data set from web , analysis and graphing 
"""

import os
os.getcwd() 
os.chdir('C:\\Users\\EmileVDH')
#C:\\Users\\EmileVDH\\OneDrive - FMI\\Desktop\\Phython Project

import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


plt.style.use('ggplot')
plt.style.use("tableau-colorblind10")

sns.reset_defaults()
sns.set(
    rc={'figure.figsize':(7,5)}, 
    style="white" # nicer layout
)

#read in the data from web , format is CSV 

#OWID DATA CSV 
url='''https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'''
df=pd.read_csv(url)

df.info()
df.describe()   ##need this in a nice format 
df.shape()
df.dtypes


##Shape Data frame 


#Change text date to date type
df.date =df.date.astype('datetime64')

w = df[df.location =='World']

df = df[df.location !='World']

#Profile and Subset 
var_maxdate=df.date.max() 
md = df[df.date==var_maxdate]

#May want to set date as index ??? why 
#df.set_index(['date'], drop=True, inplace=True)


#1 line chart of one variable 

   ##Word


plt.figure(figsize = (16,9)) # figure size with ratio 16:9
sns.set(style='darkgrid',) # background darkgrid style of graph 
sns.lineplot(x="date", y="total_cases" , data=w )
#g.fig.autofmt_xdate()
plt.title("Cases World", fontsize = 20)
plt.xlabel("Date", fontsize = 15)
plt.ylabel("Total Reported Cases", fontsize = 15)
plt.show()

   #one country 
za = df[df.location  =='South Africa']
case_za = za.loc[:, ('date' ,'total_cases')]

g=sns.relplot(x="date", y="total_cases", kind="line", data=case_za)
g.fig.autofmt_xdate()

   ##Compare Spain vs Italy in line chart for cases 
two = df[df['location'].isin(['Spain', 'Italy'])] [['date','location' ,'total_cases'] ]

plt.figure(figsize = (16,9)) # figure size with ratio 16:9
sns.set(style='darkgrid',) # background darkgrid style of graph 
 
sns.lineplot(x = "date", y = "total_cases", data = two, hue = "location",
            style = "location", palette = "hot", dashes = False, 
            markers = ["o", "<"],  legend="brief",)
 
plt.title("Case Italy vs Spain", fontsize = 20)
plt.xlabel("Date", fontsize = 15)
plt.ylabel("Total Reported Cases", fontsize = 15)
plt.show()


#3 histogram distribution of cases on a chosent day by county count 

md.total_cases.hist()
sns.distplot(md['total_cases'], kde=False)


bins = [0, 5000, 10000, 50000, 100000, np.inf]
names = ['<5k', '5k-10k', '10k-50k', '50k-100k', '>100k']

df['CaseRange'] = pd.cut(df['total_cases'], bins, labels=names)

sns.countplot(x="CaseRange", data=df)
plt.show()

# Top 10 countries Cases , Deaths and Testing by population 

a=md.nlargest(10,'total_cases')
b=md.nlargest(10,'total_deaths')

#limit the columns similar names

sns.set(style='darkgrid',) # background darkgrid style of graph 
j=sns.catplot(x="location", y="total_cases", kind="bar" ,data=a);
j.fig.autofmt_xdate()
plt.show()

bb=sns.catplot(x="location", y="total_deaths", kind="bar" ,palette="ch:.25" ,data=b);
bb.fig.autofmt_xdate()
plt.show()

#third cat 
#sns.catplot(x="sex", y="survived", hue="class", kind="bar", data=titanic);

# 5  categorical .... show deaths vs cases with continent as colour as at date x   

sns.scatterplot(x='total_cases', y='total_deaths', data=a);
plt.title('Cases vs Deaths of Top 10 countries(Cases)');
plt.show()

sns.jointplot(x='total_cases', y='total_deaths', data=md, kind='scatter');
plt.title('Cases vs Deaths of Top 10 countries(Cases)');
plt.show()

^# A nice Table to show key data 

#print(a)

print(format(aa))

#
#from tabulate import tabulate
#print(tabulate(a))
#print(tabulate(a, headers='keys', tablefmt="grid"))
#
#a.to_html('temp.html')


import plotly.graph_objects as go


aa=a[['location','total_cases','total_deaths']].head(5)
aaa=a[['total_cases_per_million']].head(5)

def place_value(number): 
     return '{value:,}'.format(value=number)
 
 num_format = lambda x: '{:,}'.format(x)
 
def build_formatters(df, format):
    return {
        column:format 
        for column, dtype in df.dtypes.items()
        if dtype in [ np.dtype('int64'), np.dtype('float64') ] 
    }
    
formatters = build_formatters(aa, 'int64')
print(aaa.to_html(formatters=formatters))

print(place_value(aa))
print("{:,}".format(aaa)) 

#aa=a.iloc[:, lambda a: a.columns.str.contains('location|total_cases|total_deaths',
#                                              case=True)].head(10)
#
#

fig = go.Figure(data=[go.Table(
    header=dict(values=list(aa.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[aa.location, aa.total_cases, aa.total_deaths],
               fill_color='lavender',
               align='left'))
])


fig.write_html("file3.html")
print(aa.to_html(float_format=lambda x: '{:,}'.format(x)))

#plotly.offline.plot(fig, filename = 'filename.html', auto_open=False)

#import plotly.express as px
#
#fig =px.scatter(x=range(10), y=range(10))
#fig.write_html("file.html")

###########################################3333

top_categories = md.groupby('location').aggregate(sum).sort_values('total_cases', ascending=False).index
howmany=10

p = sns.countplot(data=df, x = 'location')

md['location'].value_counts()[:10].plot(kind='barh')
x=md.groupby('location').aggregate(sum).sort_values('total_cases', ascending=False).index

df_tips.groupby(by='location').mean()
md.groupby(by='location')['total_cases'].mean()








# -*- coding: utf-8 -*-
"""
Created on Thu May  7 10:11:58 2020

@author: EmileVDH

Hangman Game

"""

pip install requests
pip install BeautifulSoup4
pip install ssl
pip install lxml.html
pip install time
pip install random

##################################################

import urllib.request, urllib.parse, urllib.error
import requests
from bs4 import BeautifulSoup
import pandas as pd 
import ssl
import lxml.html as lh

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
MAX_RETRIES = 20
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
session.mount('https://', adapter)

##############################################################


url='https://en.wikipedia.org/wiki/List_of_national_capitals'

r = session.get(url)
#print(r.content)

soup = BeautifulSoup(r.content, 'html.parser')
my_table = soup.find('table',{'class':'wikitable sortable'})
#print(my_table)

city=list()
for row in my_table.findAll('tr'):
    cells=row.findAll('td')
    if len(cells)==3:
       mlnk=cells[0].findAll('a')
       city.append(mlnk[0].contents[0])



################################################################

url2='https://en.wikipedia.org/wiki/List_of_RuPaul%27s_Drag_Race_contestants'

r2 = session.get(url2)
#print(r2.content)

soup2 = BeautifulSoup(r2.content, 'html.parser')

my_table2 = soup2.find('table',{'class':'wikitable sortable'})
#print(my_table2)

queens=list()
#age=list()
#homecity=list()
#homestate=list()
for row in my_table2.findAll('tr'):
        a=list(filter(len,row.text.split('\n')))
        if len(a)>=3 :
           queens.append(a[0])
#           age.append(a[1])
#           if len(a[2].split(","))>=2 :
#             homecity.append(a[2].split(",")[0])
#             homestate.append(a[2].split(",")[1])
#  
#import pandas as pd     
#data_tuples = list(zip(queens,age,homecity,homestate))
#df=pd.DataFrame(data_tuples, columns=['Queen','Age','Homecity','HomeState'])
#
#gr=df.groupby('HomeState').count() 
#gr.sort_values(by=['Queen'], inplace=True ,ascending=False)
#print(gr)
#######################################################

listoflists=list()

listoflists.append(city)
listoflists.append(queens)

#######################################################333

#importing the time module
import time
import random
#import unicodedata
#welcoming the user
cat = input('''What is your Category Choice?  
             select 1 or 2 
               1.Capital Cities   
               2.Drag Queens       ''')

catorder= int(cat)-1

cat_selected=listoflists[catorder]

print("Time to play hangman!" )

print("   ")

#wait for 1 second
time.sleep(1)

print ("Start guessing...")
time.sleep(0.5)

#here we set the secret #passed a list 
##word = 'Stockholm'.casefold()
word = random.choice(cat_selected).casefold()

#creates an variable with an empty value
guesses = ''

#determine the number of turns
turns = 10

# Create a while loop

#check if the turns are more than zero
while turns > 0:         

    # make a counter that starts with zero
    failed = 0             

    # for every character in secret_word    
    for char in word:      

    # see if the character is in the players guess
        if char in guesses:    
    
        # print then out the character
            
            print( char,    )
            

        else:
    
        # if not found, print a dash
            print ("_")  
            
        # and increase the failed counter with one
            failed += 1    

    # if failed is equal to zero

    # print You Won
    if failed == 0:        
        print( "You won"  )

    # exit the script
        break              

    print()
    print ("You have", + turns, 'more guesses')
    # ask the user go guess a character
    guess = input("guess a character:").casefold()

    # set the players guess to guesses
    guesses += guess                    
    
    if guess in word:
        
        print('Yasss Queen!!')
    
    # if the guess is not found in the secret word
    if guess not in word:  
 
     # turns counter decreases with 1 (now 9)
        turns -= 1        
 
    # print wrong
        print ("Wrong")
        
     
    # how many turns are left
   ##     print ("You have", + turns, 'more guesses')
 
    # if the turns are equal to zero
        if turns == 0:           
    
        # print "You Lose"
            print ("You Lose , Answer was:", word )
            
        if guess in word:
        
            print('Yasss Queen!!')
            
        
# -*- coding: utf-8 -*-
"""
Created on Sun May 21 00:03:13 2017

@author: HP
"""

import os
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

driver = webdriver.Firefox()
driver.get('http://www.cricket-stats.net/genp/captains.shtml')
#assert "Cricinfo" in driver.title

team = [item.text for item in driver.find_elements_by_class_name('MainTitle')]
teams = ['India','Pakistan','Sri Lanka','New Zealand','Australia','South Africa','West Indies','Zimbabwe','Bangladesh','England']
tables = driver.find_elements_by_class_name('RecordTable')
dict = {}
for i in range(len(team)):
    if team[i] in teams:
        dict[team[i]] = tables[i].text
    
def cleanser(team,stats):
    pat = '([a-zA-Z]+\s*[a-zA-Z]*)\s\(*\d*\)*\s([\d+\s+\-\.\*]*)'
    table = [item.strip() for item in stats.split('\n')]
    captain = []
    data = []
    for row in table[2:]:
        match = re.search(pat,row)
        captain.append(match.group(1))
        data.append(match.group(2))
        
    data = [item.split(' ') for item in data]
    data = [[word or '0' for word in item] for item in data]  
        
    df_test = pd.DataFrame(0,index=captain,columns=['Tenure','Mat','W','L','D','W%'])
    df_ODI = pd.DataFrame(0,index=captain,columns=['Tenure','Mat','W','L','T','NR','W%'])
    df_T20 = pd.DataFrame(0,index=captain,columns=['Tenure','Mat','W','L','NR','W%'])
    
    for i in range(len(data)):
        item = data[i]
        if item[0] == '0':
            if item[1] == '0':
                df_T20.iloc[i] = item[3:]
            else:
                df_ODI.iloc[i] = item[1:8]
                if len(item) > 8:
                    df_T20.iloc[i] = item[8:]
        else:
            df_test.iloc[i] = data[i][:6]
            if len(data[i]) > 7:
                df_ODI.iloc[i] = data[i][6:13]
            if len(data[i]) > 14:
                df_T20.iloc[i] = data[i][13:]
         
    df_test = remove_null(df_test)
    df_ODI = remove_null(df_ODI)
    df_T20 = remove_null(df_T20)
    
    path = 'data/{}/'.format(team)
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    df_test.to_csv(path+'test.csv',index_label='Captain')
    df_ODI.to_csv(path+'ODI.csv',index_label='Captain')
    df_T20.to_csv(path+'T20.csv',index_label='Captain')

def remove_null(df):
    df =  df[df != 0].dropna()
    return df[df['Tenure'] > '2000']
    
for item in dict.keys():
    cleanser(item,dict[item])
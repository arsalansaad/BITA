# -*- coding: utf-8 -*-
"""
Created on Mon May 22 20:09:52 2017

@author: HP
"""

import matplotlib.pyplot as plt
import pandas as pd

teams = ['India','Pakistan','Sri Lanka','New Zealand','Australia','South Africa','West Indies','Zimbabwe','Bangladesh','England']
formats = ['test','ODI','T20']

def plotter(team,form):
    df = pd.read_csv('data/{}/{}.csv'.format(team,form))

    #df.set_index('Captain',drop=True,inplace=True)
    if form == 'ODI' or form == 'test':
        df = df[df['Mat'] > 5]
        df.reset_index(inplace=True,drop=True)
    ax = plt.gca()
    plt.plot(df['W%'])
    plt.xlim([0,len(df)])
    plt.title('{} in {}s'.format(team,form))
    plt.xlabel('Captains')
    plt.ylabel('Win Percentage')
    plt.ylim([0,100])
    ax.set_xticklabels(df['Captain'],rotation=45,ha='right')
    return plt.show()
    
for team in teams:
    for form in formats:
        plotter(team,form)
        plt.clf()
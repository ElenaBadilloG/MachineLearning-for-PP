#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 21:36:04 2018

@author: elenabg

"""

import sys
import time
import pickle
import numpy as np
import pandas as pd
from pandas.plotting import table
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import re
import csv

def get_ca_map(filename):
    '''
    Construct a dictionary that maps community area codes to their names
    '''
    d = {}
    with open(filename, mode='r') as infile:
        reader = csv.reader(infile)
        zip_map = {rows[1]:rows[0] for rows in reader}  
    for z, n in zip_map.items():
        z = int(z)
        d[z] = n
    return d

def add_mnth_and_resp(df, date_req_label='Creation_Date', date_comp_label = ''):
    '''
    Add a column for month of request date and a column for response time (in days)
    to dataframe
    '''
    df[date_req_label] = pd.to_datetime(df[date_req_label])
    
    df['Month_Req'] = df[date_req_label].apply(lambda x: pd.to_datetime(x.strftime('%B-%Y')))
    if date_comp_label:
        df[date_comp_label] = pd.to_datetime(df[date_comp_label], errors='coerce')
        df['Response_Time'] = [float(td.days) for td in df[date_comp_label] - df[date_req_label]]
    else:
        df['Response_Time'] = 0.0
        
    return df


############### Data Augmentation and API

import census_api # program for getting census data based on coordinates

df_augm = df[(df['Month_Req']=='2017-12-01') | (df['Month_Req']=='2017-11-01')] # only include data from Nov-Dec
df_augm = df_augm.dropna()

# Augment dataframe with census variables using the ACS API

df_augm['Whites'] = list(map(get_whites, df_augm['Location']))
df_augm['Poverty'] = list(map(get_pov, df_augm['Location']))
df_augm['Educ'] = list(map(get_educ, df_augm['Location'])) #next

df_augm['Whites']=pd.to_numeric(df_augm['Whites'], errors='coerce').fillna(0)
df_augm['Poverty'] = pd.to_numeric(df_augm['Poverty'], errors='coerce').fillna(0)
df_augm['Educ'] = pd.to_numeric(df_augm['Educ'], errors='coerce').fillna(0)

pickle.dump(df_augm,open("df_wpe.p", "wb"))
df_augm.to_csv('df_augm.csv')























